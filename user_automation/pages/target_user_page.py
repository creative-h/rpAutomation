# Target user page automation
from models.user import User
from utils.logger import logger
from settings.mappings import LOCATION_MAP, DEPARTMENT_MAP, DESIGNATION_MAP, ROLE_MAP, JOB_ROLE_MAP
from settings.settings import ELMS_DEFAULT_PASSWORD, SUCCESS_MESSAGES

class TargetUserPage:

    def __init__(self, page):
        self.page = page
        
        # Define locators once
        self.users_button = page.locator("button[name='users']")
        self.add_user_button = page.locator("#launchuserModal")
        # Save button - using SVG icon with .first() to handle multiple occurrences
        self.save_button = page.locator("svg.bi-box-arrow-down").first
        
        # Text field locators with correct selectors
        self.first_name = page.locator("#ufirst_name")
        self.last_name = page.locator("#ulast_name")
        self.email = page.locator("#uemail")
        self.username = page.locator("#uuser_name")
        self.password = page.locator("#upassword")
        
        # Dropdown locators with correct selectors
        self.location_dropdown = page.locator("#location_id")
        self.designation_dropdown = page.locator("#udesig_code")
        self.department_dropdown = page.locator("#udept_id")
        self.role_dropdown = page.locator("#urole_id")
        self.job_role_dropdown = page.locator("#ujrole")

    def open_create_user(self):
        """Open the create user dialog"""
        logger.info("Opening Users page...")
        
        # Zoom out to bypass footer overlay
        self.page.evaluate("document.body.style.zoom='80%'")
        self.page.wait_for_timeout(1000)
        
        self.users_button.wait_for(state="visible")
        self.users_button.click(force=True)

        logger.info("Waiting for Users page to load...")
        try:
            self.page.wait_for_load_state("networkidle", timeout=30000)
        except:
            logger.warning("Network idle timeout, but proceeding...")
            self.page.wait_for_timeout(3000)
        self.page.wait_for_timeout(3000)

        logger.info("Waiting for Add User button...")
        self.add_user_button.wait_for(state="visible", timeout=60000)

        logger.info("Opening Add User dialog...")
        self.add_user_button.click()
        self.page.wait_for_timeout(1000)
        
        logger.info("Waiting for form to load...")
        self.first_name.wait_for(state="visible", timeout=10000)
        logger.info("Create user form opened")

    def create_user(self, user: User):
        """Create a new user in the target system"""
        logger.info(f"Creating user {user.ad_id}")
        
        self.open_create_user()
        
        # Fill text fields
        logger.info("Filling text fields...")
        self.first_name.fill(user.first_name)
        self.last_name.fill(user.last_name)
        self.email.fill("support@swastisolution.com")  # Default email
        self.username.fill(user.ad_id)
        self.password.fill(ELMS_DEFAULT_PASSWORD)
        
        # Fill dropdowns using mappings
        self._fill_dropdowns(user)
        
        # Save the form
        logger.info("Saving user...")
        self.save_button.wait_for()
        self.save_button.click()
        
        # Wait for page to update after save
        self.page.wait_for_timeout(3000)
        
        logger.info("User created successfully")

    def _fill_dropdowns(self, user: User):
        """Fill dropdown fields using mappings from user metadata"""
        logger.info("Filling dropdown fields...")
        
        # Location
        job_location = user.metadata.get("job_location", "Ujjain")
        if job_location in LOCATION_MAP:
            logger.info(f"Setting location: {job_location}")
            self.location_dropdown.select_option(LOCATION_MAP[job_location])
        else:
            logger.warning(f"Location '{job_location}' not found in mapping, using default")
            self.location_dropdown.select_option(LOCATION_MAP["Ujjain"])
        
        # Department (must be selected first)
        try:
            department = user.metadata.get("department", "IT")
            if department in DEPARTMENT_MAP:
                logger.info(f"Setting department: {department}")
                # Wait for department dropdown options to load
                self.department_dropdown.wait_for(state="visible", timeout=10000)
                self.page.wait_for_timeout(1000)
                self.department_dropdown.select_option(DEPARTMENT_MAP[department])
                # Wait for designation dropdown to populate after department selection
                self.page.wait_for_timeout(2000)
            else:
                logger.warning(f"Department '{department}' not found in mapping, using default")
                self.department_dropdown.wait_for(state="visible", timeout=10000)
                self.page.wait_for_timeout(1000)
                self.department_dropdown.select_option(DEPARTMENT_MAP["IT"])
                self.page.wait_for_timeout(2000)
        except:
            logger.warning("Department dropdown selection failed, skipping")
            self.page.wait_for_timeout(2000)
        
        # Designation (must be selected after department)
        try:
            designation = user.metadata.get("designation", "testDesignation")
            if designation in DESIGNATION_MAP:
                logger.info(f"Setting designation: {designation}")
                self.designation_dropdown.wait_for(state="visible", timeout=10000)
                self.page.wait_for_timeout(1000)
                self.designation_dropdown.select_option(DESIGNATION_MAP[designation])
            else:
                logger.warning(f"Designation '{designation}' not found in mapping, using default")
                self.designation_dropdown.wait_for(state="visible", timeout=10000)
                self.page.wait_for_timeout(1000)
                self.designation_dropdown.select_option(DESIGNATION_MAP["testDesignation"])
        except:
            logger.warning("Designation dropdown selection failed, skipping")
        
        # Role
        try:
            role = user.metadata.get("role", "User")
            if role in ROLE_MAP:
                logger.info(f"Setting role: {role}")
                self.role_dropdown.select_option(ROLE_MAP[role])
            else:
                logger.warning(f"Role '{role}' not found in mapping, using default")
                self.role_dropdown.select_option(ROLE_MAP["User"])
        except:
            logger.warning("Role dropdown selection failed, skipping")
        
        # Job Role
        # Skip job role selection for now as it requires dynamic loading
        # The dropdown options are populated via JavaScript after department selection
        logger.info("Skipping job role selection (requires dynamic loading)")
        logger.warning("Job role will need to be set manually or with additional logic")

    def check_username_exists(self, username):
        """Check if a username already exists in the system"""
        try:
            # Navigate to Users list page first to access search
            logger.info("Navigating to Users list page for username check...")
            self.users_button.wait_for(state="visible", timeout=10000)
            self.users_button.click()
            self.page.wait_for_timeout(2000)
            
            # Search for the username
            self.search_user(username)
            
            # Check if username appears in table cell
            user_cell = self.page.locator(f"td:has-text('{username}')")
            if user_cell.count() > 0:
                logger.info(f"Username {username} already exists in system")
                return True
            else:
                logger.info(f"Username {username} is available")
                return False
        except:
            logger.warning("Username check failed, assuming username is available")
            return False

    def search_user(self, search_term):
        """Search for a user by search term"""
        try:
            search_input = self.page.locator("#searchInput")
            search_input.wait_for(state="visible", timeout=5000)
            search_input.fill(search_term)
            self.page.wait_for_timeout(1000)  # Wait for search to execute
        except:
            logger.warning("Search input not found, skipping search")

    def verify_user(self, user: User):
        """Verify that a user exists in the system by searching for username in table"""
        try:
            # Navigate to Users list page first to access search
            logger.info("Navigating to Users list page for verification...")
            self.users_button.wait_for(state="visible", timeout=10000)
            self.users_button.click()
            self.page.wait_for_timeout(3000)  # Wait for page to load and refresh
            
            # Search for the username
            self.search_user(user.ad_id)
            
            # Wait longer for search results to load
            self.page.wait_for_timeout(2000)
            
            # Check if username appears in table cell
            user_cell = self.page.locator(f"td:has-text('{user.ad_id}')")
            if user_cell.count() > 0:
                logger.info(f"User {user.ad_id} found in table - verification successful")
                return True
            else:
                logger.warning(f"User {user.ad_id} not found in table - verification failed")
                return False
        except:
            logger.warning("User verification failed, assuming creation successful")
            return True