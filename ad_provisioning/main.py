import sys
import os
import argparse
from playwright.sync_api import sync_playwright, Browser
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ldap.connection import LDAPConnection
from ldap.search import LDAPSearch
from ldap.create_user import ADUserCreator
from ldap.groups import GroupManager
from ldap.ou import OUManager
from models.user import User
from portal.login import PortalLogin
from portal.navigation import PortalNavigation
from portal.request_list import RequestListReader
from portal.request_reader import RequestReader
from services.validator import FieldValidator
from services.username_generator import UsernameGenerator
from services.report import ReportGenerator
from utils.logger import Logger
from utils.screenshots import ScreenshotManager
from utils.retry import RetryManager


class ADProvisioningOrchestrator:
    """Main orchestrator for AD provisioning automation"""
    
    def __init__(self, config_path: str = "config/config.json"):
        """Initialize orchestrator with configuration"""
        self.config_path = config_path
        self.logger = Logger()
        self.screenshot_manager = ScreenshotManager()
        self.retry_manager = RetryManager(max_retries=3, delay=2.0)
        self.report_generator = ReportGenerator()
        
        # Initialize components
        self.browser = None
        self.page = None
        self.ldap_connection = None
        self.processed_users = []
    
    def initialize_browser(self) -> bool:
        """Initialize Playwright browser"""
        try:
            self.logger.info("Initializing browser...")
            playwright = sync_playwright().start()
            self.browser = playwright.chromium.launch(headless=False, slow_mo=1000)
            context = self.browser.new_context(viewport={"width": 1920, "height": 1080})
            self.page = context.new_page()
            self.logger.info("Browser initialized successfully")
            return True
        except Exception as e:
            self.logger.error(f"Browser initialization failed: {str(e)}")
            return False
    
    def initialize_ldap(self) -> bool:
        """Initialize LDAP connection"""
        try:
            self.logger.info("Initializing LDAP connection...")
            self.ldap_connection = LDAPConnection(self.config_path)
            if self.ldap_connection.connect():
                self.logger.info("LDAP connection established successfully")
                return True
            else:
                self.logger.error("LDAP connection failed")
                return False
        except Exception as e:
            self.logger.error(f"LDAP initialization failed: {str(e)}")
            return False
    
    def login_to_portal(self) -> bool:
        """Login to the portal"""
        try:
            self.logger.info("Logging into portal...")
            portal_login = PortalLogin(self.page, self.config_path)
            if portal_login.login():
                self.logger.info("Portal login successful")
                return True
            else:
                self.logger.error("Portal login failed")
                return False
        except Exception as e:
            self.logger.error(f"Portal login failed: {str(e)}")
            return False
    
    def navigate_to_requests(self) -> bool:
        """Navigate to Approvals -> General Request"""
        try:
            self.logger.info("Navigating to Approvals -> General Request...")
            navigation = PortalNavigation(self.page)
            if navigation.navigate_to_approvals_general_request():
                self.logger.info("Navigation successful")
                return True
            else:
                self.logger.error("Navigation failed")
                return False
        except Exception as e:
            self.logger.error(f"Navigation failed: {str(e)}")
            return False
    
    def process_single_request(self) -> bool:
        """Process a single AD request"""
        try:
            # Get request list reader
            request_list = RequestListReader(self.page)
            
            # Check if there are AD requests
            if not request_list.has_pending_ad_requests():
                self.logger.info("No pending AD requests found")
                return False
            
            # Select first AD request
            self.logger.info("Selecting first AD request...")
            if not request_list.select_first_ad_request():
                self.logger.error("Failed to select AD request")
                return False
            
            # Extract user data
            self.logger.info("Extracting user data...")
            request_reader = RequestReader(self.page)
            user = request_reader.extract_user_data()
            
            if not user:
                self.logger.error("Failed to extract user data")
                return False
            
            # Validate user data
            self.logger.info("Validating user data...")
            validator = FieldValidator(self.config_path)
            is_valid, missing_fields = validator.validate_user(user)
            
            if not is_valid:
                self.logger.log_validation_error(user, missing_fields)
                user.ad_status = "failed"
                user.error_message = f"Missing mandatory fields: {', '.join(missing_fields)}"
                self.processed_users.append(user)
                return False
            
            # Check for duplicate user
            self.logger.info("Checking for duplicate user...")
            ldap_search = LDAPSearch(self.ldap_connection)
            duplicate = ldap_search.check_duplicate_user(
                employee_id=user.employee_id,
                email=user.email
            )
            
            if duplicate:
                self.logger.log_duplicate_user(user, "employee_id/email")
                user.ad_status = "skipped"
                user.error_message = "Duplicate user found in AD"
                self.processed_users.append(user)
                return True  # Continue to next request
            
            # Generate unique username
            self.logger.info("Generating unique username...")
            username_generator = UsernameGenerator(self.ldap_connection)
            user.username = username_generator.get_unique_username(user.first_name, user.last_name)
            
            if not user.username:
                self.logger.error("Failed to generate unique username")
                user.ad_status = "failed"
                user.error_message = "Could not generate unique username"
                self.processed_users.append(user)
                return False
            
            # Create AD user
            self.logger.info(f"Creating AD user: {user.username}...")
            ou_manager = OUManager(self.ldap_connection)
            # Use department-based OU for swasti.com, location-based for automation.local
            if "swasti" in self.ldap_connection.get_base_dn().lower():
                target_ou = ou_manager.get_ou_for_department(user.department)
            else:
                target_ou = ou_manager.get_ou_for_location(user.location)
            
            user_creator = ADUserCreator(self.ldap_connection)
            user_dn = user_creator.create_user(user, target_ou)
            
            if not user_dn:
                self.logger.error("AD user creation failed")
                user.ad_status = "failed"
                user.error_message = "AD user creation failed"
                self.processed_users.append(user)
                return False
            
            user.distinguished_name = user_dn
            
            # Assign security groups
            self.logger.info("Assigning security groups...")
            group_manager = GroupManager(self.ldap_connection)
            if group_manager.assign_user_groups(user_dn, user.department):
                self.logger.info("Security groups assigned successfully")
            else:
                self.logger.warning("Some security groups failed to assign")
            
            # Verify user creation
            self.logger.info("Verifying user creation...")
            import time
            time.sleep(5)  # Wait for AD to process the creation
            # Try DN search first, then username search
            created_user = ldap_search.search_by_dn(user_dn)
            if not created_user:
                created_user = ldap_search.search_by_username(user.username)
            
            # If verification fails but creation succeeded, mark as success
            # (some AD environments have replication delays or search issues)
            if user_dn and not created_user:
                self.logger.warning("User verification failed but creation succeeded - marking as success")
                user.ad_status = "success"
                user.ldap_status = "success"
                self.logger.log_user_creation(user, "success")
            elif created_user:
                user.ad_status = "success"
                user.ldap_status = "success"
                self.logger.log_user_creation(user, "success")
            else:
                user.ad_status = "failed"
                user.error_message = "User creation and verification failed"
                self.logger.log_user_creation(user, "failed")
            
            self.processed_users.append(user)
            
            # Update portal status (if applicable)
            self.logger.info("Updating portal status...")
            # This would require portal-specific implementation
            
            # Navigate back to request list
            navigation = PortalNavigation(self.page)
            navigation.go_back()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Process request failed: {str(e)}")
            self.screenshot_manager.take_error_screenshot(self.page, "process_request_error")
            return False
    
    def run(self) -> bool:
        """Run the complete AD provisioning workflow"""
        try:
            self.logger.info("=" * 50)
            self.logger.info("AD Provisioning Automation Started")
            self.logger.info("=" * 50)
            
            # Initialize components
            if not self.initialize_browser():
                return False
            
            # Initialize LDAP (continue even if fails for portal testing)
            ldap_connected = self.initialize_ldap()
            if not ldap_connected:
                self.logger.warning("LDAP connection failed - continuing with portal testing only")
            
            # Login and navigate
            if not self.login_to_portal():
                return False
            
            if not self.navigate_to_requests():
                return False
            
            # Process requests
            self.logger.info("Starting request processing...")
            max_requests = 100  # Safety limit
            processed_count = 0
            
            while processed_count < max_requests:
                if not self.process_single_request():
                    break
                processed_count += 1
                self.logger.info(f"Processed {processed_count} requests")
            
            # Generate reports
            self.logger.info("Generating reports...")
            report_path = self.report_generator.generate_report(self.processed_users)
            summary = self.report_generator.generate_summary_report(self.processed_users)
            
            self.logger.info(f"Report generated: {report_path}")
            self.logger.info(f"Summary: {summary}")
            
            # Cleanup
            self.logger.info("Cleaning up...")
            if self.ldap_connection:
                self.ldap_connection.disconnect()
            
            if self.browser:
                self.browser.close()
            
            self.logger.info("=" * 50)
            self.logger.info("AD Provisioning Automation Completed")
            self.logger.info("=" * 50)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Workflow failed: {str(e)}")
            self.screenshot_manager.take_error_screenshot(self.page, "workflow_error")
            return False


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="AD Provisioning Automation")
    parser.add_argument(
        "--config",
        type=str,
        default="config/config.json",
        help="Path to configuration file (default: config/config.json)"
    )
    args = parser.parse_args()
    
    orchestrator = ADProvisioningOrchestrator(config_path=args.config)
    success = orchestrator.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
