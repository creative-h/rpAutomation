# Source request page automation
from models.user import User
from utils.logger import logger

FIELD_MAP = {
    "ad_id": "#ctl00_ContentPlaceHolder1_TxtAdDocID",
    "first_name": "#ctl00_ContentPlaceHolder1_Txtfname",
    "last_name": "#ctl00_ContentPlaceHolder1_TxtLname",
    "email": "#ctl00_ContentPlaceHolder1_Txtemail",
    "employee_id": "#ctl00_ContentPlaceHolder1_TxtEmpID",
    "department": "#ctl00_ContentPlaceHolder1_Drp_Department",
    "role": "#ctl00_ContentPlaceHolder1_txtRole",
}

class SourceRequestPage:

    def __init__(self, page):
        self.page = page
        
        # Define locators once
        self.ad_id = page.locator("#ctl00_ContentPlaceHolder1_TxtAdDocID")
        self.first_name = page.locator("#ctl00_ContentPlaceHolder1_Txtfname")
        self.last_name = page.locator("#ctl00_ContentPlaceHolder1_TxtLname")
        self.email = page.locator("#ctl00_ContentPlaceHolder1_Txtemail")
        self.employee_code = page.locator("#ctl00_ContentPlaceHolder1_TxtEmpID")
        self.department = page.locator("#ctl00_ContentPlaceHolder1_Drp_Department")
        self.job_title = page.locator("#ctl00_ContentPlaceHolder1_TxtJobTitle")

    def open_request(self):
        """Navigate to the request page"""
        self.page.get_by_role("link", name=" Request").click ()
        self.page.wait_for_load_state("networkidle")

    def select_self(self):
        """Filter requests to show only self-assigned"""
        self.page.get_by_role("link", name=" Single User Request").click()
        self.page.wait_for_load_state("networkidle")
        self.page.locator("#ctl00_ContentPlaceHolder1_DropRequestFor").select_option("SELF")
        self.page.wait_for_load_state("networkidle")

    def read_user(self):
        """Read user details from the current request"""
        # Wait for fields to be visible
        self.first_name.wait_for(state="visible", timeout=10000)
        
        # Read user data using locators
        # For dropdown, get the selected option's text instead of value
        department_value = self.department.input_value().strip()
        department_text = self.department.locator("option:checked").text_content() if department_value else ""
        
        user = User(
            ad_id=self.ad_id.input_value().strip(),
            first_name=self.first_name.input_value().strip(),
            last_name=self.last_name.input_value().strip(),
            email=self.email.input_value().strip(),
            employee_id=self.employee_code.input_value().strip(),
            department=department_text.strip() if department_text else department_value,
            role=self.job_title.input_value().strip() if self.job_title.is_visible() else "",
            metadata={}
        )
        
        # Log user details
        logger.info("=" * 50)
        logger.info("USER DETAILS")
        logger.info("=" * 50)
        logger.info(f"AD ID      : {user.ad_id}")
        logger.info(f"First Name : {user.first_name}")
        logger.info(f"Last Name  : {user.last_name}")
        logger.info(f"Email      : {user.email}")
        logger.info(f"Department : {user.department}")
        logger.info(f"EmployeeID : {user.employee_id}")
        logger.info(f"Role       : {user.role}")
        logger.info("=" * 50)
        
        return user

    def approve(self):
        """Approve the current request"""
        self.page.click("button[name='approve']")
        self.page.wait_for_load_state("networkidle")

    def reject(self):
        """Reject the current request"""
        self.page.click("button[name='reject']")
        self.page.wait_for_load_state("networkidle")