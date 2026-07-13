# Screenshots utility
import os
from datetime import datetime

def take_screenshot(page, name="screenshot"):
    """Take a screenshot and save it to the screenshots directory"""
    os.makedirs("reports/screenshots", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reports/screenshots/{name}_{timestamp}.png"
    page.screenshot(path=filename)
    return filename

def take_error_screenshot(page):
    """Take a screenshot when an error occurs"""
    return take_screenshot(page, "error")