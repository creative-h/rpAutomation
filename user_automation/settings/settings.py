# Application settings and constants

# Browser Settings
BROWSER_SETTINGS = {
    "headless": False,
    "slow_mo": 300,  # milliseconds
    "timeout": 30000,  # milliseconds
}

# ELMS Default Password
ELMS_DEFAULT_PASSWORD = "12345"

# Approval Criteria
APPROVAL_CRITERIA = {
    "system": "Swasti/LMS-Learning Management System",
    "category": "Create User on ELMS",
}

# Success Messages
SUCCESS_MESSAGES = {
    "user_created": "User created successfully",
    "request_approved": "Request approved successfully",
}
