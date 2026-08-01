from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from typing import List, Dict, Optional


class RequestListReader:
    """Read and filter requests from the portal request list"""
    
    def __init__(self, page: Page):
        """Initialize request list reader with page"""
        self.page = page
    
    def get_request_table_rows(self) -> List[Dict]:
        """Get all rows from the request table"""
        try:
            # Wait for table to be visible
            table = self.page.locator("table").first
            table.wait_for(state="visible", timeout=10000)
            
            # Get all rows
            rows = table.locator("tr").all()
            
            request_data = []
            
            # Skip header row (index 0)
            for row in rows[1:]:
                cells = row.locator("td").all()
                if len(cells) > 0:
                    row_data = {}
                    for i, cell in enumerate(cells):
                        row_data[f"column_{i}"] = cell.inner_text().strip()
                    request_data.append(row_data)
            
            return request_data
        except PlaywrightTimeoutError:
            print("Request table not found or not visible")
            return []
        except Exception as e:
            print(f"Get request table rows failed: {str(e)}")
            return []
    
    def filter_ad_requests(self, requests: List[Dict]) -> List[Dict]:
        """Filter requests where Request Access For = ACTIVE DIRECTORY"""
        ad_requests = []
        
        for request in requests:
            # Check if any column contains "ACTIVE DIRECTORY"
            for key, value in request.items():
                if "ACTIVE DIRECTORY" in value.upper():
                    ad_requests.append(request)
                    break
        
        return ad_requests
    
    def get_ad_request_count(self) -> int:
        """Get count of Active Directory requests"""
        requests = self.get_request_table_rows()
        ad_requests = self.filter_ad_requests(requests)
        return len(ad_requests)
    
    def get_first_ad_request(self) -> Optional[Dict]:
        """Get the first Active Directory request from the list"""
        requests = self.get_request_table_rows()
        ad_requests = self.filter_ad_requests(requests)
        
        if ad_requests:
            return ad_requests[0]
        return None
    
    def select_first_ad_request(self) -> bool:
        """Select and click the first Active Directory request"""
        try:
            # Click on the cell with "ACTIVE DIRECTORY" text (matching codegen)
            ad_cell = self.page.get_by_role("cell", name="ACTIVE DIRECTORY")
            ad_cell.wait_for(state="visible", timeout=10000)
            ad_cell.click()
            self.page.wait_for_load_state("networkidle")
            
            # Click the delete link to open detail page (matching codegen)
            delete_link = self.page.locator("#ctl00_ContentPlaceHolder1_grid_data_ctl04_lnkDelete")
            delete_link.wait_for(state="visible", timeout=10000)
            delete_link.click()
            self.page.wait_for_load_state("networkidle")
            
            return True
        except PlaywrightTimeoutError:
            print("ACTIVE DIRECTORY cell or delete link not found")
            return False
        except Exception as e:
            print(f"Select first AD request failed: {str(e)}")
            return False
    
    def get_request_by_id(self, request_id: str) -> Optional[Dict]:
        """Find a specific request by ID"""
        requests = self.get_request_table_rows()
        
        for request in requests:
            for key, value in request.items():
                if request_id in value:
                    return request
        
        return None
    
    def has_pending_ad_requests(self) -> bool:
        """Check if there are pending Active Directory requests"""
        return self.get_ad_request_count() > 0
