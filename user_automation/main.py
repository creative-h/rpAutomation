# Main entry point for user automation
from utils.browser import BrowserManager
from pages.login_page import LoginPage
from pages.source_request_page import SourceRequestPage
from pages.target_user_page import TargetUserPage
from models.user import User
from utils.logger import setup_logger
from utils.screenshots import take_error_screenshot
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

        # Login to source system
        logger.info("Navigating to source system...")
        browser.page.goto(SOURCE_URL)
        logger.info("Logging into source system...")
        login_page = LoginPage(browser.page)
        login_page.login(SOURCE_USERNAME, SOURCE_PASSWORD)
        logger.info("Logged into source system")

        # Navigate to source request page and read single user
        logger.info("Navigating to source request page...")
        source_page = SourceRequestPage(browser.page)
        source_page.open_request()
        logger.info("Selecting SELF filter...")
        source_page.select_self()
        logger.info("Reading user data...")
        user = source_page.read_user()
        logger.info(f"Retrieved user: {user.email}")

        # Login to target system
        logger.info("Navigating to target system...")
        browser.page.goto(TARGET_URL)
        logger.info("Logging into target system...")
        target_page = TargetUserPage(browser.page)
        target_page.login(TARGET_USERNAME, TARGET_PASSWORD)
        logger.info("Logged into target system")

        # Create user in target system
        logger.info("Creating user in target system...")
        logger.info(f"Creating user: {user.email}")
        target_page.create_user(user)
        logger.info(f"Created user: {user.email}")

        # Approve request only after successful user creation
        logger.info("Approving request in source system...")
        browser.page.goto(SOURCE_URL)
        login_page.login(SOURCE_USERNAME, SOURCE_PASSWORD)
        source_page = SourceRequestPage(browser.page)
        source_page.open_request()
        source_page.select_self()
        source_page.approve()
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
        # Only wait for input if stdin is available (not in windowed mode)
        if sys.stdin is not None:
            logger.error("Browser will remain open for inspection. Press Enter to close...")
            input()
        raise
    finally:
        if browser:
            browser.close()

if __name__ == "__main__":
    main()
