# Browser utility
from playwright.sync_api import sync_playwright
import os
import sys

class BrowserManager:

    def __init__(self):
        self.playwright = sync_playwright().start()

        try:
            # Try to find system Playwright chromium installation
            # This is needed because PyInstaller runs from temp directory
            import playwright.sync_api
            from pathlib import Path
            
            # Try common Playwright installation paths
            possible_paths = [
                Path.home() / "AppData" / "Local" / "ms-playwright" / "chromium-1228" / "chrome-win64" / "chrome.exe",
                Path.home() / ".cache" / "ms-playwright" / "chromium-1228" / "chrome-win64" / "chrome.exe",
            ]
            
            executable_path = None
            for path in possible_paths:
                if path.exists():
                    executable_path = str(path)
                    break
            
            launch_args = {
                "headless": False,
                "slow_mo": 300
            }
            
            if executable_path:
                launch_args["executable_path"] = executable_path
            
            self.browser = self.playwright.chromium.launch(**launch_args)
            
        except Exception as e:
            if "Executable doesn't exist" in str(e) or "playwright install" in str(e):
                print("\n" + "="*70)
                print("ERROR: Playwright browsers are not installed!")
                print("="*70)
                print("\nTo fix this issue, run the following command:")
                print("\n    playwright install chromium")
                print("\nOr install all browsers:")
                print("\n    playwright install")
                print("\n" + "="*70 + "\n")
                sys.exit(1)
            raise

        self.context = self.browser.new_context()

        self.page = self.context.new_page()

    def new_page(self):
        """Create a new page/tab in the same context"""
        return self.context.new_page()

    def close(self):
        self.context.close()
        self.browser.close()
        self.playwright.stop()