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

        self.page.get_by_role(
            "button",
            name="Login"
        ).click()

        self.page.wait_for_load_state("networkidle")