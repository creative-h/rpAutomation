# Login page automation
class LoginPage:

    def __init__(self, page):
        self.page = page

    def login(self, username, password):
        self.page.get_by_role(
            "textbox",
            name="Enter Your AD ID"
        ).fill(username)

        self.page.get_by_role(
            "textbox",
            name="Password"
        ).fill(password)

        login_button = self.page.locator("#btn_llogin")
        login_button.click()
        
        # Wait for navigation with timeout
        try:
            self.page.wait_for_load_state("networkidle", timeout=30000)
        except:
            self.page.wait_for_timeout(3000)