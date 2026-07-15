# Main entry point for user automation
from utils.browser import BrowserManager
from pages.login_page import LoginPage
from pages.approval_page import ApprovalPage
from pages.target_login_page import TargetLoginPage
from pages.target_user_page import TargetUserPage
from models.user_request import UserRequest
from utils.logger import setup_logger
from utils.screenshots import take_error_screenshot
from utils.counter import generate_unique_username
import pandas as pd
import os
import sys
from config import *

logger = setup_logger()

def main():
    browser = None
    try:
        # Validate configuration
        if not SOURCE_URL:
            raise ValueError("SOURCE_URL is missing. Check your .env file.")
        if not TARGET_URL:
            raise ValueError("TARGET_URL is missing. Check your .env file.")
        if not SOURCE_USERNAME:
            raise ValueError("SOURCE_USERNAME is missing. Check your .env file.")
        if not TARGET_USERNAME:
            raise ValueError("TARGET_USERNAME is missing. Check your .env file.")
        
        logger.info(f"Source URL: {SOURCE_URL}")
        logger.info(f"Target URL: {TARGET_URL}")
        
        # Initialize browser
        browser = BrowserManager()
        logger.info("Browser initialized")

        # ===== WEBSITE 1: Source System =====
        logger.info("=" * 50)
        logger.info("WEBSITE 1: Source System")
        logger.info("=" * 50)
        
        # Create source page
        source_page = browser.page
        logger.info("Navigating to source system...")
        source_page.goto(SOURCE_URL)
        logger.info("Logging into source system...")
        login_page = LoginPage(source_page)
        login_page.login(SOURCE_USERNAME, SOURCE_PASSWORD)
        logger.info("Logged into source system")

        # Navigate to approvals and read request
        logger.info("Opening Approvals page...")
        approval_page = ApprovalPage(source_page)
        approval_page.open_general_requests()
        
        logger.info("Filtering for Creation requests...")
        approval_page.filter_creation_requests()
        
        logger.info("Selecting first request...")
        approval_page.select_first_request()
        
        logger.info("Reading request data...")
        request = approval_page.read_request()
        
        # Validate request before proceeding
        if not approval_page.verify_request(request):
            logger.error("Request does not match approval criteria. Aborting automation.")
            return

        # ===== WEBSITE 2: ELMS (New Tab) =====
        logger.info("=" * 50)
        logger.info("WEBSITE 2: ELMS (New Tab)")
        logger.info("=" * 50)
        
        # Create new tab for ELMS
        logger.info("Opening new tab for ELMS...")
        target_page = browser.new_page()
        logger.info("Navigating to target system...")
        target_page.goto(TARGET_URL)
        logger.info("Logging into target system...")
        target_login = TargetLoginPage(target_page)
        target_login.login(TARGET_PASSWORD)
        logger.info("Logged into target system")

        # Create user in target system
        logger.info("Creating user in target system...")
        logger.info(f"Creating user: {request.ad_id}")
        target_user_page = TargetUserPage(target_page)
        
        # Convert UserRequest to User for target system
        from models.user import User
        unique_username = generate_unique_username(request.ad_id)
        user = User(
            ad_id=unique_username,
            first_name=request.first_name,
            last_name=request.last_name,
            email=f"{request.first_name.lower()}.{request.last_name.lower()}@swastisolutions.com",
            employee_id="NA",
            department="Information Technology",
            role="Executive - IT",
            metadata={"job_location": request.job_location, "designation": "Executive"}
        )
        
        target_user_page.create_user(user)
        
        # Verify user creation
        logger.info("Verifying user creation...")
        user_created = target_user_page.verify_user(user)
        
        if not user_created:
            logger.error("User creation verification failed. Aborting automation.")
            return
        
        logger.info("User successfully created and verified")

        # ===== WEBSITE 1: Approve Request =====
        logger.info("=" * 50)
        logger.info("WEBSITE 1: Approve Request")
        logger.info("=" * 50)
        
        # Bring source page to front (session remains active)
        logger.info("Bringing source page to front...")
        source_page.bring_to_front()
        
        # Approve request only after successful user creation
        logger.info("Approving request...")
        approval_page.approve()
        logger.info("Request approved successfully")

        # Save results to CSV
        logger.info("Saving results to CSV...")
        os.makedirs("data", exist_ok=True)
        user_data = [user.__dict__]
        df = pd.DataFrame(user_data)
        df.to_csv("data/results.csv", index=False)
        logger.info("Results saved to data/results.csv")

        logger.info("Automation completed successfully")

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        if browser:
            take_error_screenshot(browser.page)
        raise
    finally:
        if browser:
            browser.close()

if __name__ == "__main__":
    main()
