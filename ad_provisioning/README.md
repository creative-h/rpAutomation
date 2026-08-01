# AD Provisioning Automation

A production-ready Python automation that reads pending Active Directory user creation requests from a web portal and automatically provisions users in Microsoft Active Directory via LDAP.

## Features

- **Automated User Provisioning**: Reads AD requests from portal and creates users in Active Directory
- **Duplicate Detection**: Checks for existing users by employee ID, email, or username
- **Unique Username Generation**: Automatically generates unique usernames (firstname.lastname, firstname.lastname1, etc.)
- **Security Group Assignment**: Automatically assigns users to department-specific security groups
- **OU Management**: Places users in location-based Organizational Units
- **Validation**: Validates mandatory fields before user creation
- **Comprehensive Logging**: Detailed logs for all operations with timestamps
- **Error Handling**: Retry logic for transient failures with screenshot capture
- **Reporting**: Generates CSV/JSON reports with execution summary

## Project Structure

```
ad_provisioning/
│
├── config/
│   ├── config.json          # Main configuration file
│   └── groups.json          # Security group and OU mappings
│
├── portal/
│   ├── login.py             # Portal login operations
│   ├── navigation.py        # Portal navigation
│   ├── request_list.py      # Request list reader
│   └── request_reader.py    # Request data extractor
│
├── ldap/
│   ├── connection.py        # LDAP connection management
│   ├── search.py            # LDAP search operations
│   ├── create_user.py       # AD user creation
│   ├── groups.py            # Security group management
│   └── ou.py               # Organizational Unit management
│
├── models/
│   └── user.py             # User dataclass model
│
├── services/
│   ├── validator.py         # Field validation
│   ├── username_generator.py # Username generation
│   └── report.py            # Report generation
│
├── utils/
│   ├── logger.py            # Logging utility
│   ├── screenshots.py       # Screenshot capture
│   └── retry.py             # Retry logic
│
├── logs/
│   ├── ad_provisioning.log # Log file
│   └── screenshots/        # Error screenshots
│
├── reports/
│   └── *.csv               # Execution reports
│
├── main.py                 # Main workflow orchestrator
└── requirements.txt        # Python dependencies
```

## Prerequisites

- Python 3.11+
- Active Directory domain with LDAP access
- Portal account with access to Approvals section
- Network connectivity to both portal and AD server

## Installation

1. Clone the repository:
```bash
cd ad_provisioning
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Playwright browsers:
```bash
playwright install chromium
```

## Configuration

### Portal Configuration

Edit `config/config.json` to set portal credentials:

```json
{
  "portal": {
    "login_url": "http://185.131.55.105:8057/Login",
    "username": "your_username",
    "password": "your_password"
  }
}
```

### LDAP Configuration

Edit `config/config.json` to set LDAP connection details:

```json
{
  "ldap": {
    "server": "192.168.56.101",
    "domain": "automation.local",
    "bind_user": "AUTOMATION\\svc_automation",
    "bind_password": "your_ldap_password",
    "port": 389,
    "use_ssl": false,
    "base_dn": "DC=automation,DC=local"
  }
}
```

### Security Group Mapping

Edit `config/groups.json` to customize department-to-group mappings:

```json
{
  "department_group_mapping": {
    "IT": "IT Users",
    "HR": "HR Users",
    "Finance": "Finance Users"
  }
}
```

### OU Mapping

Edit `config/groups.json` to customize location-to-OU mappings:

```json
{
  "location_ou_mapping": {
    "INDORE": "OU=Indore,OU=Users,OU=Automation,DC=automation,DC=local",
    "MUMBAI": "OU=Mumbai,OU=Users,OU=Automation,DC=automation,DC=local"
  }
}
```

## Usage

Run the automation:

```bash
python main.py
```

## Workflow

1. **Login to Portal**: Authenticates to the request portal
2. **Navigate to Requests**: Goes to Approvals → General Request
3. **Filter AD Requests**: Identifies requests where Request Access For = ACTIVE DIRECTORY
4. **Extract User Data**: Reads all user information from request
5. **Validate Fields**: Checks mandatory fields (first name, last name, email, department, employee ID)
6. **Check Duplicates**: Searches AD for existing users by employee ID, email, or username
7. **Generate Username**: Creates unique username (firstname.lastname, firstname.lastname1, etc.)
8. **Create AD User**: Provisions user in Active Directory with all attributes
9. **Set Password**: Sets temporary password and forces change on first login
10. **Move to OU**: Places user in location-specific Organizational Unit
11. **Assign Groups**: Adds user to department-specific security groups
12. **Verify Creation**: Confirms user was created successfully
13. **Update Portal**: Updates request status (if applicable)
14. **Generate Report**: Creates execution report with all details

## Mandatory Fields

The following fields are mandatory for user creation:

- First Name
- Last Name
- Email
- Department
- Employee ID

If any mandatory field is missing, the request will be skipped and logged.

## Logging

Logs are written to:
- Console output
- `logs/ad_provisioning.log` file

Log levels:
- INFO: Normal operations
- WARNING: Non-critical issues (duplicates, missing fields)
- ERROR: Critical failures

## Error Handling

The automation includes:

- **Retry Logic**: Transient failures are retried with exponential backoff
- **Screenshot Capture**: Screenshots are taken on errors for debugging
- **Graceful Degradation**: Continues processing next request on individual failures
- **Detailed Error Messages**: All errors are logged with context

## Reports

Reports are generated in `reports/` directory:

- CSV format with all user details and status
- JSON format with summary statistics
- Includes: success rate, failure rate, skipped duplicates

## Security Considerations

- Store credentials securely (consider environment variables or secret management)
- Use SSL/TLS for LDAP connections in production
- Implement proper password policies
- Regularly rotate service account passwords
- Review and audit security group assignments

## Troubleshooting

### LDAP Connection Failed
- Verify server address and port
- Check bind user credentials
- Ensure network connectivity to AD server
- Verify firewall rules

### Portal Login Failed
- Verify portal URL is correct
- Check username and password
- Ensure portal is accessible
- Check for CAPTCHA or MFA requirements

### User Creation Failed
- Check mandatory fields are present
- Verify username doesn't already exist
- Ensure OU exists in AD
- Check service account has sufficient permissions

### Selectors Not Found
- Portal HTML structure may have changed
- Update selectors in portal/*.py files
- Use browser DevTools to inspect elements

## Development

### Adding New Field Mappings

Edit the relevant configuration files:
- `config/groups.json` for group and OU mappings
- `config/config.json` for validation rules

### Extending Functionality

The modular architecture allows easy extension:
- Add new services in `services/`
- Extend models in `models/`
- Add new LDAP operations in `ldap/`
- Extend portal interactions in `portal/`

## License

This project is provided as-is for internal automation purposes.

## Support

For issues or questions:
1. Check logs in `logs/ad_provisioning.log`
2. Review screenshots in `logs/screenshots/`
3. Examine reports in `reports/`
4. Verify configuration files are correct
