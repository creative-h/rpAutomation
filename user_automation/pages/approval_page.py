# Approval page automation
from models.user_request import UserRequest
from utils.logger import logger

class ApprovalPage:

    def __init__(self, page):
        self.page = page
        
        # Define locators once with correct selectors
        self.approvals = page.get_by_text("Approvals")
        self.general_request = page.get_by_text("General Request")
        self.request_type = page.locator("#ctl00_ContentPlaceHolder1_drpRequestType")
        self.system_name = page.locator("#ctl00_ContentPlaceHolder1_drpSystemName")
        self.show_button = page.locator("#ctl00_ContentPlaceHolder1_btnShow")
        self.select_button = page.locator("#ctl00_ContentPlaceHolder1_grid_data_ctl02_lnkDelete")
        
        # Request detail locators with correct selectors
        self.request_type_field = page.locator("#ctl00_ContentPlaceHolder1_txtRequestType")
        self.first_name = page.locator("#ctl00_ContentPlaceHolder1_txt_app_fn")
        self.last_name = page.locator("#ctl00_ContentPlaceHolder1_txt_app_ln")
        self.request_category = page.locator("#ctl00_ContentPlaceHolder1_txt_app_reqcat")
        self.ad_id = page.locator("#ctl00_ContentPlaceHolder1_txt_app_empntid")
        self.job_location = page.locator("#ctl00_ContentPlaceHolder1_txt_app_jobloc")
        self.approve_button = page.get_by_role("button", name="Approve")
        self.reject_button = page.get_by_role("button", name="Reject")

    def open_general_requests(self):
        """Navigate to general requests page"""
        logger.info("Opening Approvals page...")
        self.approvals.wait_for(state="visible", timeout=10000)
        self.approvals.click()
        
        logger.info("Opening General Request...")
        self.general_request.wait_for(state="visible", timeout=10000)
        self.general_request.click()
        
        self.page.wait_for_load_state("networkidle")
        logger.info("General Requests page loaded")

    def filter_creation_requests(self):
        """Apply filters for creation requests for Swasti/LMS system"""
        logger.info("Filtering for Creation requests...")
        self.request_type.wait_for(state="visible", timeout=10000)
        self.request_type.select_option("Creation")
        
        logger.info("Filtering for Swasti/LMS-Learning Management System...")
        self.system_name.wait_for(state="visible", timeout=10000)
        self.system_name.select_option(" Swasti/LMS-Learning Management System")
        
        logger.info("Clicking Show button...")
        self.show_button.wait_for(state="visible", timeout=10000)
        self.show_button.click()
        
        self.page.wait_for_load_state("networkidle")
        logger.info("Filters applied")

    def select_first_request(self):
        """Select the first request in the list"""
        logger.info("Selecting first request...")
        self.select_button.wait_for(state="visible", timeout=10000)
        self.select_button.click()
        self.page.wait_for_load_state("networkidle")
        logger.info("Request details opened")

    def read_request(self):
        """Read request details from the current page"""
        logger.info("Reading request details...")
        
        # Wait for request details to be visible
        self.request_type_field.wait_for(state="visible", timeout=10000)
        
        request = UserRequest(
            request_type=self.request_type_field.input_value().strip(),
            first_name=self.first_name.input_value().strip(),
            last_name=self.last_name.input_value().strip(),
            request_category=self.request_category.input_value().strip(),
            ad_id=self.ad_id.input_value().strip(),
            job_location=self.job_location.input_value().strip(),
            metadata={}
        )
        
        # Log request details
        logger.info("=" * 50)
        logger.info("REQUEST DETAILS")
        logger.info("=" * 50)
        logger.info(f"Request Type     : {request.request_type}")
        logger.info(f"Request Category : {request.request_category}")
        logger.info(f"First Name       : {request.first_name}")
        logger.info(f"Last Name        : {request.last_name}")
        logger.info(f"Employee AD ID   : {request.ad_id}")
        logger.info(f"Job Location     : {request.job_location}")
        logger.info("=" * 50)
        
        return request

    def verify_request(self, request: UserRequest):
        """Verify if the request matches approval criteria"""
        logger.info("Verifying request criteria...")
        
        if (
            request.request_type == "Creation"
            and request.request_category == "APPLICATIONS"
        ):
            logger.info("Request matches approval criteria")
            return True
        else:
            logger.warning(f"Request does not match criteria")
            logger.warning(f"  Expected Request Type: Creation, Got: {request.request_type}")
            logger.warning(f"  Expected Request Category: APPLICATIONS, Got: {request.request_category}")
            return False

    def approve(self):
        """Approve the current request"""
        logger.info("Approving request...")
        try:
            self.approve_button.wait_for(state="visible", timeout=10000)
            self.approve_button.click()
            self.page.wait_for_load_state("networkidle")
            logger.info("Request approved successfully")
        except:
            logger.warning("Approve button not found, skipping approval")
            # For now, skip approval step

    def reject(self):
        """Reject the current request"""
        logger.info("Rejecting request...")
        self.reject_button.click()
        self.page.wait_for_load_state("networkidle")
        logger.info("Request rejected successfully")
