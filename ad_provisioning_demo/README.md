# AD Provisioning Automation Demo

A Streamlit-based demo application for the AD Provisioning Automation system.

## Features

- **Environment Selection**: Switch between Test Server and Production environments
- **Configuration Display**: View current LDAP and AD settings
- **Workflow Visualization**: See the complete automation workflow steps
- **Key Features**: Overview of automation capabilities
- **Recent Results**: Display latest report metrics and data
- **How to Run**: Instructions for command-line execution

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Streamlit app:
```bash
streamlit run app.py
```

## Usage

1. Select the environment from the sidebar (Test Server or Production)
2. View the current configuration
3. Review the workflow steps
4. Check recent results from automation runs
5. Follow the instructions to run the actual automation

## Screenshots

The demo provides a visual overview of:
- Portal integration workflow
- LDAP connection process
- User creation steps
- Security management features
- Reporting capabilities

## Note

This is a demo application. For actual user provisioning, run the main automation script:
```bash
python ../ad_provisioning/main.py --config ../ad_provisioning/config/config_test.json
```
