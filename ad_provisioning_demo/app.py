import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Page configuration
st.set_page_config(
    page_title="AD Provisioning Automation",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeeba;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🔐 AD Provisioning Demo")
st.sidebar.markdown("---")

# Environment selection
st.sidebar.subheader("Environment")
environment = st.sidebar.radio(
    "Select Environment",
    ["Test Server (automation.local)", "Production (swasti.com)"],
    index=0
)

# Load config based on environment
config_path = os.path.join(os.path.dirname(__file__), '..', 'ad_provisioning', 'config')
if "Test Server" in environment:
    config_file = os.path.join(config_path, 'config_test.json')
else:
    config_file = os.path.join(config_path, 'config_swasti.json')

# Load configuration
try:
    with open(config_file, 'r') as f:
        config = json.load(f)
except:
    st.error("Configuration file not found")
    st.stop()

# Main content
st.markdown('<div class="main-header">Active Directory Provisioning Automation</div>', unsafe_allow_html=True)

# Overview section
st.markdown('<div class="sub-header">📋 Overview</div>', unsafe_allow_html=True)
st.markdown("""
This automated system provisions Active Directory users by:
1. **Portal Integration**: Automatically logs into the approval portal
2. **Request Processing**: Extracts user details from AD requests
3. **LDAP Integration**: Creates users in Active Directory
4. **Security Management**: Sets passwords, enables accounts, assigns groups
""")

# Configuration display
st.markdown('<div class="sub-header">⚙️ Current Configuration</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("**LDAP Configuration**")
    ldap_config = config.get('ldap', {})
    st.json({
        "Server": ldap_config.get('server', 'N/A'),
        "Domain": ldap_config.get('domain', 'N/A'),
        "Port": ldap_config.get('port', 389),
        "SSL": ldap_config.get('use_ssl', False),
        "Base DN": ldap_config.get('base_dn', 'N/A')
    })

with col2:
    st.markdown("**AD Configuration**")
    ad_config = config.get('ad', {})
    st.json({
        "Default Password": "***",
        "Force Password Change": ad_config.get('force_password_change', True),
        "Default OU": ad_config.get('default_ou', 'N/A')
    })

# Workflow steps
st.markdown('<div class="sub-header">🔄 Workflow Steps</div>', unsafe_allow_html=True)

steps = [
    {
        "step": 1,
        "name": "Portal Login",
        "description": "Authenticate to the approval portal using credentials",
        "status": "✅"
    },
    {
        "step": 2,
        "name": "Navigation",
        "description": "Navigate to Approvals → General Request section",
        "status": "✅"
    },
    {
        "step": 3,
        "name": "Request Selection",
        "description": "Filter and select ACTIVE DIRECTORY requests",
        "status": "✅"
    },
    {
        "step": 4,
        "name": "Data Extraction",
        "description": "Extract user details (name, email, department, etc.)",
        "status": "✅"
    },
    {
        "step": 5,
        "name": "LDAP Connection",
        "description": "Connect to Active Directory server",
        "status": "✅"
    },
    {
        "step": 6,
        "name": "User Creation",
        "description": "Create user object in AD with all attributes",
        "status": "✅"
    },
    {
        "step": 7,
        "name": "Password Management",
        "description": "Set default password and force change on first login",
        "status": "✅"
    },
    {
        "step": 8,
        "name": "Account Enablement",
        "description": "Enable account and assign security groups",
        "status": "✅"
    },
    {
        "step": 9,
        "name": "Verification",
        "description": "Verify user creation in Active Directory",
        "status": "✅"
    },
    {
        "step": 10,
        "name": "Reporting",
        "description": "Generate detailed reports with status and metrics",
        "status": "✅"
    }
]

# Display workflow as a table
df_steps = pd.DataFrame(steps)
st.table(df_steps[['step', 'name', 'description', 'status']])

# Features section
st.markdown('<div class="sub-header">✨ Key Features</div>', unsafe_allow_html=True)

feature_col1, feature_col2, feature_col3 = st.columns(3)

with feature_col1:
    st.markdown("""
    <div class="info-box">
    <h4>🚀 Automation</h4>
    <ul>
        <li>Fully automated workflow</li>
        <li>No manual intervention required</li>
        <li>Processes multiple requests</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with feature_col2:
    st.markdown("""
    <div class="info-box">
    <h4>🔒 Security</h4>
    <ul>
        <li>Secure password handling</li>
        <li>Force password change policy</li>
        <li>Group-based access control</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with feature_col3:
    st.markdown("""
    <div class="info-box">
    <h4>📊 Reporting</h4>
    <ul>
        <li>Detailed CSV reports</li>
        <li>Success/failure metrics</li>
        <li>Audit trail logging</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# Recent results section
st.markdown('<div class="sub-header">📈 Recent Results</div>', unsafe_allow_html=True)

# Check for recent reports
reports_dir = os.path.join(os.path.dirname(__file__), '..', 'ad_provisioning', 'reports')
if os.path.exists(reports_dir):
    report_files = [f for f in os.listdir(reports_dir) if f.endswith('.csv')]
    if report_files:
        # Get the most recent report
        latest_report = sorted(report_files)[-1]
        report_path = os.path.join(reports_dir, latest_report)
        
        try:
            df_report = pd.read_csv(report_path)
            st.markdown(f"**Latest Report:** {latest_report}")
            
            # Show summary metrics
            if not df_report.empty:
                total = len(df_report)
                successful = len(df_report[df_report['status'] == 'success'])
                failed = len(df_report[df_report['status'] == 'failed'])
                success_rate = (successful / total * 100) if total > 0 else 0
                
                metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                
                with metric_col1:
                    st.metric("Total Requests", total)
                
                with metric_col2:
                    st.metric("Successful", successful, delta_color="normal")
                
                with metric_col3:
                    st.metric("Failed", failed, delta_color="inverse")
                
                with metric_col4:
                    st.metric("Success Rate", f"{success_rate:.1f}%")
                
                # Show recent requests table
                st.markdown("**Recent Requests:**")
                st.dataframe(df_report.head(10), use_container_width=True)
        except Exception as e:
            st.warning(f"Could not load report: {str(e)}")
    else:
        st.info("No reports generated yet. Run the automation to see results.")
else:
    st.info("Reports directory not found. Run the automation to generate reports.")

# How to run section
st.markdown('<div class="sub-header">🚀 How to Run</div>', unsafe_allow_html=True)

st.markdown("""
<div class="warning-box">
<h4>Command Line Execution</h4>
<code>python ad_provisioning/main.py --config ad_provisioning/config/config_test.json</code>

<h4>For Production Environment</h4>
<code>python ad_provisioning/main.py --config ad_provisioning/config/config_swasti.json</code>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
<p>AD Provisioning Automation System | Version 1.0</p>
<p>For support, contact the system administrator</p>
</div>
""", unsafe_allow_html=True)
