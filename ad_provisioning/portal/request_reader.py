from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from typing import Optional
from models.user import User


class RequestReader:
    """Extract user data from request detail page"""
    
    def __init__(self, page: Page):
        """Initialize request reader with page"""
        self.page = page
    
    def extract_user_data(self) -> Optional[User]:
        """Extract all user information from the request detail page"""
        try:
            # Wait for page to load
            self.page.wait_for_load_state("networkidle")
            
            # Extract fields using actual ASP.NET control IDs from inspect code
            user_data = User(
                employee_id=self._get_input_value("ctl00_ContentPlaceHolder1_txt_ad_empntid"),
                first_name=self._get_input_value("ctl00_ContentPlaceHolder1_txt_ad_fn"),
                last_name=self._get_input_value("ctl00_ContentPlaceHolder1_txt_ad_ln"),
                email=self._get_input_value("ctl00_ContentPlaceHolder1_txt_ad_email") or self._generate_email_from_username(),
                department=self._get_input_value("ctl00_ContentPlaceHolder1_txt_ad_jobloc") or "IT_DEPT",
                request_id=self._get_request_id_from_url(),
                requested_by=self._get_input_value("ctl00_ContentPlaceHolder1_txt_ad_userhodname"),
                requested_date=None
            )
            
            # Optional fields
            user_data.display_name = f"{user_data.first_name} {user_data.last_name}"
            user_data.designation = self._get_input_value("ctl00_ContentPlaceHolder1_txt_ad_designation")
            user_data.manager = self._get_input_value("ctl00_ContentPlaceHolder1_txt_ad_userhodname")
            user_data.company = "swasti"
            user_data.location = self._get_input_value("ctl00_ContentPlaceHolder1_txt_ad_jobloc")
            
            return user_data
            
        except Exception as e:
            print(f"Extract user data failed: {str(e)}")
            return None
    
    def _generate_email_from_username(self) -> str:
        """Generate email from username if email field is not available"""
        try:
            username = self._get_input_value("ctl00_ContentPlaceHolder1_txt_ad_empntid")
            if username:
                # Clean up username (remove spaces) and append domain
                clean_username = username.strip()
                return f"{clean_username}@swasti.com"
            return None
        except:
            return None
    
    def _get_text_value(self, label_text: str) -> Optional[str]:
        """Get value for a field by finding text label and extracting adjacent text"""
        try:
            # Find the label text
            label = self.page.get_by_text(label_text).first
            if label.is_visible():
                # Get the parent element and find the value (usually in a span or next element)
                parent = label.locator("..")
                # Try to find a sibling element that contains the value
                siblings = parent.locator("xpath=following-sibling::*").all()
                for sibling in siblings:
                    text = sibling.inner_text().strip()
                    if text and text != label_text:
                        return text
                # If no sibling, try to get text from parent after the label
                full_text = parent.inner_text()
                if label_text in full_text:
                    parts = full_text.split(label_text)
                    if len(parts) > 1:
                        return parts[1].strip()
            return None
        except:
            return None
    
    def _get_field_value(self, field_label: str) -> Optional[str]:
        """Get value for a field by its label"""
        try:
            # Try to find label and get corresponding input value
            label = self.page.get_by_text(field_label).first
            if label.is_visible():
                # Look for input field near the label
                parent = label.locator("..")
                input_field = parent.locator("input").or_(parent.locator("select")).or_(parent.locator("textarea"))
                if input_field.count() > 0:
                    return input_field.first.input_value() or input_field.first.inner_text()
            return None
        except:
            return None
    
    def _get_input_value(self, input_id: str) -> Optional[str]:
        """Get value from input field by ID"""
        try:
            input_field = self.page.locator(f"#{input_id}")
            if input_field.count() > 0:
                return input_field.input_value()
            return None
        except:
            return None
    
    def _get_request_id_from_url(self) -> Optional[str]:
        """Get request ID from URL"""
        try:
            url = self.page.url
            if "data=" in url:
                # Extract the data parameter
                import re
                match = re.search(r'data=([^&]+)', url)
                if match:
                    return match.group(1)
            return None
        except:
            return None
    
    def get_request_access_type(self) -> Optional[str]:
        """Get the request access type (e.g., ACTIVE DIRECTORY)"""
        try:
            access_type = self._get_field_value("Request Access For") or self._get_field_value("RequestAccessFor")
            return access_type
        except:
            return None
    
    def is_ad_request(self) -> bool:
        """Check if this is an Active Directory request"""
        access_type = self.get_request_access_type()
        return access_type and "ACTIVE DIRECTORY" in access_type.upper()
