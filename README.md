# RP Automation - User Synchronization Tool

An automated solution for extracting user data from a source system and creating users in a target system using Playwright browser automation.

## 📋 Overview

This automation tool streamlines the user creation process by:
- Extracting user details (AD ID, name, email, department, role) from a source request system
- Creating corresponding users in a target LMS system
- Automatically approving requests after successful user creation
- Generating CSV reports of processed users

## 🏗️ Architecture

The project follows the **Page Object Model (POM)** design pattern for maintainable and scalable automation:

```
user_automation/
├── main.py              # Entry point and workflow orchestration
├── config.py            # Environment configuration
├── models/
│   └── user.py          # User data model
├── pages/
│   ├── login_page.py    # Login page interactions
│   ├── source_request_page.py  # Source system page interactions
│   └── target_user_page.py     # Target system page interactions
├── utils/
│   ├── browser.py       # Browser management
│   ├── logger.py        # Logging configuration
│   └── screenshots.py    # Error screenshot capture
└── .env                 # Environment variables (credentials)
```

## 🚀 Features

- **Automated User Extraction**: Reads user data from source request forms
- **Intelligent Field Mapping**: Handles dropdowns and text fields correctly
- **Robust Error Handling**: Screenshots on failure, detailed logging
- **Configuration Management**: Environment-based configuration
- **Executable Distribution**: Can be packaged as standalone EXE
- **Success Verification**: Confirms user creation with validation

## 📦 Installation

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Step 1: Clone the Repository

```bash
git clone https://github.com/creative-h/rpAutomation.git
cd rpAutomation
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

Or install individual packages:

```bash
pip install playwright
pip install pandas
pip install python-dotenv
pip install loguru
```

### Step 3: Install Playwright Browsers

```bash
playwright install chromium
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root:

```ini
# Source System Configuration
SOURCE_URL=http://185.131.55.105:8058/Login
SOURCE_USERNAME=your_username
SOURCE_PASSWORD=your_password

# Target System Configuration
TARGET_URL=https://elms.swastisolutions.co.in/lms/views/login_new.php
TARGET_USERNAME=your_username
TARGET_PASSWORD=your_password
```

## 🎯 Usage

### Running from Source

```bash
cd user_automation
python main.py
```

### Running the Executable

The project can be packaged as a standalone EXE for distribution:

```bash
# Build the EXE
pyinstaller --onefile --add-data "user_automation/.env;." user_automation/main.py

# Run the EXE
cd dist
main.exe
```

**Note**: The target machine must have Playwright browsers installed:
```bash
playwright install chromium
```

## 📊 Project Workflow

```
1. Login to Source System
   ↓
2. Navigate to Request Page
   ↓
3. Select SELF Filter
   ↓
4. Extract User Data
   - AD ID
   - First Name
   - Last Name
   - Email
   - Department
   - Role
   ↓
5. Login to Target System
   ↓
6. Navigate to Users Page
   ↓
7. Open Add User Dialog
   ↓
8. Fill User Form
   - First Name
   - Last Name
   - Email
   - Username (AD ID)
   ↓
9. Save User
   ↓
10. Verify Success
   ↓
11. Approve Source Request
   ↓
12. Generate CSV Report
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SOURCE_URL` | Source system login URL | Yes |
| `SOURCE_USERNAME` | Source system username | Yes |
| `SOURCE_PASSWORD` | Source system password | Yes |
| `TARGET_URL` | Target system login URL | Yes |
| `TARGET_USERNAME` | Target system username | Yes |
| `TARGET_PASSWORD` | Target system password | Yes |

### Browser Settings

Browser behavior can be modified in `utils/browser.py`:

- **Headless Mode**: Set `headless=True` for background execution
- **Slow Motion**: Adjust `slow_mo` parameter for debugging (in milliseconds)

## 📝 User Model

The `User` dataclass includes the following fields:

```python
@dataclass
class User:
    ad_id: str           # Active Directory ID
    first_name: str      # User's first name
    last_name: str       # User's last name
    email: str           # User's email address
    employee_id: str     # Employee ID
    department: str      # Department name
    role: str            # Job title/role
    metadata: Dict       # Additional flexible data
```

## 🐛 Troubleshooting

### Common Issues

**1. Playwright Browser Not Found**
```
ERROR: Playwright browsers are not installed!
```
**Solution**: Run `playwright install chromium`

**2. Configuration Missing**
```
ValueError: SOURCE_URL is missing. Check your .env file.
```
**Solution**: Ensure `.env` file exists in the project root with all required variables

**3. Element Timeout**
```
TimeoutError: Element not visible within timeout
```
**Solution**: Check if the page has loaded completely, adjust timeout values in page classes

**4. Footer Overlay Blocking Clicks**
```
Element is not clickable at point
```
**Solution**: The automation uses `force=True` and zoom out to bypass UI overlays

## 📂 Output Files

- **CSV Report**: `data/results.csv` - Contains processed user data
- **Logs**: `reports/logs/automation_YYYY-MM-DD.log` - Detailed execution logs
- **Screenshots**: `screenshots/` - Error screenshots for debugging

## 🔒 Security Considerations

- **Never commit** `.env` file to version control
- **Use strong passwords** for system credentials
- **Rotate credentials** regularly
- **Limit access** to the executable distribution

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is proprietary software. All rights reserved.

## 📞 Support

For issues or questions, please contact the development team.

## 🔄 Version History

- **v1.0.0** - Initial release
  - Basic user extraction and creation
  - Source and target system integration
  - CSV reporting
  - EXE packaging support
  - AD ID field support
  - Success verification
