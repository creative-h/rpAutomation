from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from typing import Optional


class PortalNavigation:
    """Handle portal navigation operations"""
    
    def __init__(self, page: Page):
        """Initialize portal navigation with page"""
        self.page = page
    
    def navigate_to_approvals(self) -> bool:
        """Navigate to Approvals section"""
        try:
            approvals_link = self.page.get_by_role("link", name=" Approvals")
            approvals_link.wait_for(state="visible", timeout=10000)
            approvals_link.click()
            self.page.wait_for_load_state("networkidle")
            return True
        except PlaywrightTimeoutError:
            print("Approvals link not found or not visible")
            return False
        except Exception as e:
            print(f"Navigate to Approvals failed: {str(e)}")
            return False
    
    def navigate_to_general_request(self) -> bool:
        """Navigate to General Request section"""
        try:
            general_request_link = self.page.get_by_role("link", name=" General Request")
            general_request_link.wait_for(state="visible", timeout=10000)
            general_request_link.click()
            self.page.wait_for_load_state("networkidle")
            return True
        except PlaywrightTimeoutError:
            print("General Request link not found or not visible")
            return False
        except Exception as e:
            print(f"Navigate to General Request failed: {str(e)}")
            return False
    
    def navigate_to_approvals_general_request(self) -> bool:
        """Navigate to Approvals -> General Request"""
        try:
            # First navigate to Approvals
            if not self.navigate_to_approvals():
                return False
            
            # Then navigate to General Request
            if not self.navigate_to_general_request():
                return False
            
            return True
        except Exception as e:
            print(f"Navigate to Approvals -> General Request failed: {str(e)}")
            return False
    
    def go_back(self) -> bool:
        """Navigate back to previous page"""
        try:
            self.page.go_back()
            self.page.wait_for_load_state("networkidle")
            return True
        except Exception as e:
            print(f"Go back failed: {str(e)}")
            return False
    
    def refresh_page(self) -> bool:
        """Refresh current page"""
        try:
            self.page.reload()
            self.page.wait_for_load_state("networkidle")
            return True
        except Exception as e:
            print(f"Refresh page failed: {str(e)}")
            return False
    
    def wait_for_page_load(self, timeout: int = 30000) -> bool:
        """Wait for page to fully load"""
        try:
            self.page.wait_for_load_state("networkidle", timeout=timeout)
            return True
        except PlaywrightTimeoutError:
            print("Page load timeout")
            return False
        except Exception as e:
            print(f"Wait for page load failed: {str(e)}")
            return False
    
    def is_on_general_request_page(self) -> bool:
        """Check if currently on General Request page"""
        try:
            return "General Request" in self.page.content() or "GeneralRequest" in self.page.url
        except:
            return False
