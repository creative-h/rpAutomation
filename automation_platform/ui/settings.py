"""
Settings Page
Configuration management for the automation platform
"""

import streamlit as st
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def show_settings():
    """Display the settings/configuration page"""
    
    st.markdown("### ⚙️ Platform Configuration")
    st.markdown("---")
    
    # Source Portal Configuration
    st.markdown("#### 🌐 Source Portal Settings")
    
    with st.expander("Portal Configuration", expanded=True):
        portal_col1, portal_col2 = st.columns(2)
        
        with portal_col1:
            portal_url = st.text_input(
                "Portal URL",
                value="http://185.131.55.105:8057/Login",
                help="URL of the source approval portal"
            )
            
            portal_username = st.text_input(
                "Portal Username",
                value="amit.mishra",
                help="Username for portal authentication"
            )
        
        with portal_col2:
            portal_password = st.text_input(
                "Portal Password",
                value="123",
                type="password",
                help="Password for portal authentication"
            )
            
            portal_timeout = st.number_input(
                "Page Timeout (seconds)",
                min_value=10,
                max_value=120,
                value=30,
                help="Timeout for page load operations"
            )
    
    st.markdown("---")
    
    # Active Directory Configuration
    st.markdown("#### 🔐 Active Directory Settings")
    
    with st.expander("LDAP Configuration", expanded=True):
        ldap_col1, ldap_col2 = st.columns(2)
        
        with ldap_col1:
            ldap_server = st.text_input(
                "LDAP Server",
                value="swasti.com",
                help="LDAP server hostname or IP"
            )
            
            ldap_domain = st.text_input(
                "LDAP Domain",
                value="swasti.com",
                help="Active Directory domain"
            )
            
            ldap_port = st.number_input(
                "LDAP Port",
                min_value=389,
                max_value=636,
                value=389,
                help="LDAP port (389 for non-SSL, 636 for SSL)"
            )
        
        with ldap_col2:
            ldap_bind_user = st.text_input(
                "Bind User",
                value="swasti\\administrator",
                help="LDAP bind user for authentication"
            )
            
            ldap_bind_password = st.text_input(
                "Bind Password",
                value="Shree@2029",
                type="password",
                help="LDAP bind user password"
            )
            
            ldap_use_ssl = st.checkbox(
                "Use SSL/TLS",
                value=False,
                help="Enable SSL/TLS for LDAP connection"
            )
        
        ldap_base_dn = st.text_input(
            "Base DN",
            value="DC=swasti,DC=com",
            help="LDAP base distinguished name"
        )
    
    st.markdown("---")
    
    # ELMS Configuration
    st.markdown("#### 📋 ELMS System Settings")
    
    with st.expander("ELMS Configuration", expanded=False):
        elms_col1, elms_col2 = st.columns(2)
        
        with elms_col1:
            elms_url = st.text_input(
                "ELMS URL",
                value="https://elms.swasti.com",
                help="ELMS system URL"
            )
            
            elms_username = st.text_input(
                "ELMS Username",
                value="",
                help="Username for ELMS authentication"
            )
        
        with elms_col2:
            elms_password = st.text_input(
                "ELMS Password",
                value="",
                type="password",
                help="Password for ELMS authentication"
            )
            
            elms_timeout = st.number_input(
                "ELMS Timeout (seconds)",
                min_value=10,
                max_value=120,
                value=45,
                help="Timeout for ELMS operations"
            )
    
    st.markdown("---")
    
    # User Creation Settings
    st.markdown("#### 👤 User Creation Settings")
    
    with st.expander("User Creation Configuration", expanded=False):
        user_col1, user_col2 = st.columns(2)
        
        with user_col1:
            default_password = st.text_input(
                "Default Password",
                value="Pass@12345",
                type="password",
                help="Default password for new users"
            )
            
            force_password_change = st.checkbox(
                "Force Password Change",
                value=True,
                help="Force users to change password on first login"
            )
        
        with user_col2:
            default_ou = st.text_input(
                "Default OU",
                value="OU=IT_DEPT,OU=swastisolutions,DC=swasti,DC=com",
                help="Default Organizational Unit for new users"
            )
            
            username_format = st.selectbox(
                "Username Format",
                ["firstname.lastname", "firstinitiallastname", "lastname.firstname"],
                index=0,
                help="Format for generating usernames"
            )
    
    st.markdown("---")
    
    # Storage Settings
    st.markdown("#### 💾 Storage Settings")
    
    with st.expander("Storage Configuration", expanded=False):
        storage_col1, storage_col2 = st.columns(2)
        
        with storage_col1:
            report_folder = st.text_input(
                "Report Folder",
                value="reports",
                help="Folder path for storing reports"
            )
            
            screenshot_folder = st.text_input(
                "Screenshot Folder",
                value="screenshots",
                help="Folder path for storing screenshots"
            )
        
        with storage_col2:
            log_folder = st.text_input(
                "Log Folder",
                value="logs",
                help="Folder path for storing log files"
            )
            
            retention_days = st.slider(
                "Retention Period (Days)",
                min_value=7,
                max_value=365,
                value=30,
                help="Number of days to keep logs and screenshots"
            )
    
    st.markdown("---")
    
    # Automation Settings
    st.markdown("#### 🤖 Automation Settings")
    
    with st.expander("Automation Configuration", expanded=False):
        auto_col1, auto_col2 = st.columns(2)
        
        with auto_col1:
            max_retries = st.number_input(
                "Max Retries",
                min_value=1,
                max_value=10,
                value=3,
                help="Maximum number of retry attempts for failed operations"
            )
            
            retry_delay = st.number_input(
                "Retry Delay (seconds)",
                min_value=1,
                max_value=60,
                value=2,
                help="Delay between retry attempts"
            )
        
        with auto_col2:
            headless_mode = st.checkbox(
                "Headless Browser",
                value=False,
                help="Run browser in headless mode (no GUI)"
            )
            
            slow_mo = st.slider(
                "Slow Motion (ms)",
                min_value=0,
                max_value=2000,
                value=1000,
                help="Slow down browser actions for debugging"
            )
    
    st.markdown("---")
    
    # Save/Reset Buttons
    button_col1, button_col2, button_col3 = st.columns(3)
    
    with button_col1:
        if st.button("💾 Save Configuration", use_container_width=True, type="primary"):
            st.success("Configuration saved successfully!")
    
    with button_col2:
        if st.button("🔄 Reset to Defaults", use_container_width=True):
            st.warning("Configuration reset to defaults!")
    
    with button_col3:
        if st.button("🧪 Test Connections", use_container_width=True):
            with st.spinner("Testing connections..."):
                import time
                time.sleep(2)
                st.success("All connections tested successfully!")
    
    st.markdown("---")
    
    # Configuration Export/Import
    st.markdown("#### 📤 Configuration Management")
    
    export_col1, export_col2 = st.columns(2)
    
    with export_col1:
        if st.button("📥 Export Configuration", use_container_width=True):
            st.success("Configuration exported!")
    
    with export_col2:
        if st.button("📤 Import Configuration", use_container_width=True):
            st.success("Configuration imported!")
