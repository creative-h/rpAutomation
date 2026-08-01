from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from typing import Optional
import json
import os


class PortalLogin:
    """Handle portal login operations"""
    
    def __init__(self, page: Page, config_path: str = "config/config.json"):
        """Initialize portal login with page and configuration"""
        self.page = page
        self.config = self._load_config(config_path)
        self.login_url = self.config['portal']['login_url']
        self.username = self.config['portal']['username']
        self.password = self.config['portal']['password']
    
    def _load_config(self, config_path: str) -> dict:
        """Load portal configuration from JSON file"""
        full_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), config_path)
        with open(full_path, 'r') as f:
            config = json.load(f)
        return config
    
    def navigate_to_login(self) -> bool:
        """Navigate to the login page"""
        try:
            self.page.goto(self.login_url)
            self.page.wait_for_load_state("networkidle", timeout=30000)
            # Wait a bit more for any dynamic content
            self.page.wait_for_timeout(2000)
            
            # Check if page loaded successfully
            if self.page.url == "about:blank":
                print("Page loaded as blank - possible network issue")
                return False
            
            print(f"Successfully navigated to: {self.page.url}")
            return True
        except Exception as e:
            print(f"Navigation to login page failed: {str(e)}")
            return False
    
    def fill_username(self, username: str = None) -> bool:
        """Fill username field"""
        try:
            username_to_use = username or self.username
            # Try ID selector first
            username_field = self.page.locator("#txtluid")
            if username_field.count() == 0:
                username_field = self.page.get_by_role("textbox", name="Enter Your AD ID")
            username_field.wait_for(state="visible", timeout=10000)
            username_field.fill(username_to_use)
            return True
        except PlaywrightTimeoutError:
            print("Username field not found or not visible")
            return False
        except Exception as e:
            print(f"Fill username failed: {str(e)}")
            return False
    
    def fill_password(self, password: str = None) -> bool:
        """Fill password field"""
        try:
            password_to_use = password or self.password
            # Try multiple selectors for password field
            password_field = self.page.locator("#txtlpwd")
            if password_field.count() == 0:
                password_field = self.page.get_by_role("textbox", name="Password")
            password_field.wait_for(state="visible", timeout=10000)
            password_field.fill(password_to_use)
            return True
        except PlaywrightTimeoutError:
            print("Password field not found or not visible")
            return False
        except Exception as e:
            print(f"Fill password failed: {str(e)}")
            return False
    
    def click_login_button(self) -> bool:
        """Click login button"""
        try:
            # Use the actual button ID from inspect code
            login_button = self.page.locator("#btn_llogin")
            login_button.wait_for(state="visible", timeout=10000)
            login_button.click()
            self.page.wait_for_load_state("networkidle")
            return True
        except PlaywrightTimeoutError:
            print("Login button not found or not visible")
            return False
        except Exception as e:
            print(f"Click login button failed: {str(e)}")
            return False
    
    def login(self, username: str = None, password: str = None) -> bool:
        """Perform complete login process"""
        try:
            # Navigate to login page
            if not self.navigate_to_login():
                return False
            
            # Fill username
            if not self.fill_username(username):
                return False
            
            # Press Tab to move to password field
            username_field = self.page.locator("#txtluid")
            if username_field.count() > 0:
                username_field.press("Tab")
            else:
                username_field = self.page.get_by_role("textbox", name="Enter Your AD ID")
                username_field.press("Tab")
            
            # Fill password
            if not self.fill_password(password):
                return False
            
            # Wait a moment for the button to be ready
            self.page.wait_for_timeout(1000)
            
            # Click login button directly (matching codegen)
            if not self.click_login_button():
                return False
            
            # Verify login success (check if we're redirected)
            self.page.wait_for_timeout(2000)
            return True
            
        except Exception as e:
            print(f"Login process failed: {str(e)}")
            return False
    
    def is_logged_in(self) -> bool:
        """Check if user is logged in"""
        try:
            # Check if we're not on login page anymore
            current_url = self.page.url
            return "Login" not in current_url and self.login_url != current_url
        except:
            return False
    
    def logout(self) -> bool:
        """Logout from portal"""
        try:
            # Look for logout button/link
            logout_button = self.page.get_by_role("button", name="Logout")
            if logout_button.is_visible():
                logout_button.click()
                self.page.wait_for_load_state("networkidle")
                return True
            return False
        except Exception as e:
            print(f"Logout failed: {str(e)}")
            return False
