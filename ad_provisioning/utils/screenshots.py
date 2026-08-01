import os
from datetime import datetime
from typing import Optional


class ScreenshotManager:
    """Screenshot utility for capturing browser states during automation"""
    
    def __init__(self, screenshot_dir: str = "logs/screenshots"):
        """Initialize screenshot manager with directory"""
        self.screenshot_dir = screenshot_dir
        self._ensure_directory_exists()
    
    def _ensure_directory_exists(self):
        """Create screenshot directory if it doesn't exist"""
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)
    
    def take_screenshot(self, page, prefix: str = "screenshot") -> Optional[str]:
        """Take a screenshot of the current page state"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{prefix}_{timestamp}.png"
            filepath = os.path.join(self.screenshot_dir, filename)
            
            page.screenshot(path=filepath)
            return filepath
        except Exception as e:
            print(f"Screenshot failed: {str(e)}")
            return None
    
    def take_error_screenshot(self, page, error_context: str) -> Optional[str]:
        """Take a screenshot with error context in filename"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_context = error_context.replace(" ", "_").replace("/", "_")[:50]
            filename = f"error_{safe_context}_{timestamp}.png"
            filepath = os.path.join(self.screenshot_dir, filename)
            
            page.screenshot(path=filepath)
            return filepath
        except Exception as e:
            print(f"Error screenshot failed: {str(e)}")
            return None
    
    def take_request_screenshot(self, page, request_id: str) -> Optional[str]:
        """Take a screenshot for a specific request"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"request_{request_id}_{timestamp}.png"
            filepath = os.path.join(self.screenshot_dir, filename)
            
            page.screenshot(path=filepath)
            return filepath
        except Exception as e:
            print(f"Request screenshot failed: {str(e)}")
            return None
    
    def cleanup_old_screenshots(self, days: int = 7):
        """Remove screenshots older than specified days"""
        try:
            current_time = datetime.now()
            for filename in os.listdir(self.screenshot_dir):
                filepath = os.path.join(self.screenshot_dir, filename)
                if os.path.isfile(filepath):
                    file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                    if (current_time - file_time).days > days:
                        os.remove(filepath)
        except Exception as e:
            print(f"Screenshot cleanup failed: {str(e)}")
