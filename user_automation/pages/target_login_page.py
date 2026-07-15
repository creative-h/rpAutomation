# Target login page automation
from utils.logger import logger
from settings.settings import ELMS_DEFAULT_PASSWORD

class TargetLoginPage:

    def __init__(self, page):
        self.page = page

    def login(self, password=ELMS_DEFAULT_PASSWORD):
        """Login to ELMS target system"""
        logger.info("Clicking Super Admin Login link...")
        super_admin_link = self.page.get_by_role("link", name="Super Admin Login")
        super_admin_link.wait_for(state="visible", timeout=10000)
        super_admin_link.click()
        
        logger.info("Waiting for password field...")
        password_field = self.page.locator("#userPassword")
        password_field.wait_for(state="visible", timeout=10000)
        
        logger.info("Entering password...")
        password_field.fill(password)
        
        logger.info("Clicking Login button...")
        login_button = self.page.locator("button[name='admin_submit']")
        login_button.wait_for(state="visible", timeout=10000)
        login_button.click()
        
        self.page.wait_for_load_state("networkidle", timeout=30000)
        logger.info("Successfully logged into ELMS")
