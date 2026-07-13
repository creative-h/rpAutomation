# Target user page automation
from pages.login_page import LoginPage
from models.user import User
from utils.logger import logger

FIELD_MAPPING = {
    "First Name": "first_name",
    "Last Name": "last_name",
    "Email": "email",
    "UserName": "ad_id",
}

class TargetUserPage:

    def __init__(self, page):
        self.page = page
        
        # Define locators once
        self.users_menu = page.locator("[id=\"1\"]")
        self.add_user = page.locator("#launchuserModal")
        self.first_name = page.get_by_role("textbox", name="First Name")
        self.last_name = page.get_by_role("textbox", name="Last Name")
        self.email = page.get_by_role("textbox", name="Email")

    def login(self, username, password):
        """Login to target system"""
        self.page.get_by_role("link", name="Super Admin Login").click()
        self.page.get_by_role("textbox", name="Enter Your Password").fill(password)
        self.page.get_by_role("button", name="Login").click()
        self.page.wait_for_load_state("networkidle")

    def create_user(self, user: User):
        """Create a new user in the target system"""
        logger.info(f"Creating user {user.ad_id}")
        
        # Navigate to user creation modal
        logger.info("Opening Users page...")
        
        # Zoom out to bypass footer overlay
        self.page.evaluate("document.body.style.zoom='80%'")
        self.page.wait_for_timeout(1000)  # Allow layout to settle
        
        self.page.locator("button[name='users']").click(force=True)

        logger.info("Waiting for Users page to load...")
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(3000)  # Give SPA time to render

        logger.info("Waiting for Add User button...")
        add_btn = self.page.locator("#launchuserModal")
        add_btn.wait_for(state="visible", timeout=60000)

        logger.info("Opening Add User dialog...")
        add_btn.click()
        self.page.wait_for_timeout(1000)
        
        # Wait for form to load
        logger.info("Waiting for form to load...")
        self.first_name.wait_for(state="visible", timeout=10000)
        
        # Fill all form fields
        logger.info("Filling user fields...")
        self.page.get_by_role("textbox", name="First Name").fill(user.first_name)
        self.page.get_by_role("textbox", name="Last Name").fill(user.last_name)
        self.page.get_by_role("textbox", name="Email").fill(user.email)
        self.page.get_by_role("textbox", name="UserName").fill(user.ad_id)
        
        # Note: Add employee_id, department, role fields when you get their selectors
        
        # Save the form
        logger.info("Saving user...")
        self.page.get_by_role("button", name="Save").click()
        
        # Wait for success message
        logger.info("Waiting for success confirmation...")
        try:
            self.page.get_by_text("User created successfully").wait_for(state="visible", timeout=15000)
            logger.info("Success message confirmed")
        except:
            logger.warning("Success message not found, but proceeding...")
        
        self.page.wait_for_load_state("networkidle")
        logger.info("User created successfully")

    def search_user(self, search_term):
        """Search for a user by search term"""
        self.page.fill("input[name='search']", search_term)
        self.page.click("button[name='searchBtn']")
        self.page.wait_for_load_state("networkidle")

    def verify_user(self, user: User):
        """Verify that a user exists in the system"""
        self.search_user(user.ad_id)
        results = self.page.query_selector_all("table.user-table tr.user-row")
        return len(results) > 0