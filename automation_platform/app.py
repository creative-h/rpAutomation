"""
Enterprise Identity Provisioning Platform
Main Streamlit Application
"""

import streamlit as st
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Page configuration
st.set_page_config(
    page_title="Enterprise Identity Provisioning Platform",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enterprise theme
st.markdown("""
<style>
    /* Main theme colors - Dark Blue + White */
    :root {
        --primary-color: #1e3a8a;
        --secondary-color: #3b82f6;
        --accent-color: #60a5fa;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --danger-color: #ef4444;
        --background-color: #f8fafc;
        --card-background: #ffffff;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
    }
    
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Header styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    
    .sub-header {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--text-secondary);
        margin-bottom: 2rem;
    }
    
    /* Card styling */
    .metric-card {
        background: var(--card-background);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0;
        transition: all 0.2s ease;
    }
    
    .metric-card:hover {
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    
    /* Status indicators */
    .status-success {
        color: var(--success-color);
        font-weight: 600;
    }
    
    .status-warning {
        color: var(--warning-color);
        font-weight: 600;
    }
    
    .status-danger {
        color: var(--danger-color);
        font-weight: 600;
    }
    
    /* Workflow step styling */
    .workflow-step {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        background: var(--card-background);
        border-left: 4px solid var(--secondary-color);
    }
    
    .workflow-step.completed {
        border-left-color: var(--success-color);
        background: #ecfdf5;
    }
    
    .workflow-step.running {
        border-left-color: var(--warning-color);
        background: #fffbeb;
    }
    
    .workflow-step.pending {
        border-left-color: var(--text-secondary);
        background: #f1f5f9;
    }
    
    /* Log window styling */
    .log-window {
        background: #1e293b;
        color: #e2e8f0;
        padding: 1rem;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        max-height: 400px;
        overflow-y: auto;
    }
    
    .log-entry {
        margin: 0.25rem 0;
        padding: 0.25rem 0;
        border-bottom: 1px solid #334155;
    }
    
    .log-timestamp {
        color: #94a3b8;
        margin-right: 0.5rem;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, var(--primary-color) 0%, var(--secondary-color) 100%);
    }
    
    /* Button styling */
    .stButton > button {
        background: var(--primary-color);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: var(--secondary-color);
        transform: translateY(-1px);
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
    }
</style>
""", unsafe_allow_html=True)

# Import page modules
from ui.dashboard import show_dashboard
from ui.automation import show_automation
from ui.reports import show_reports
from ui.logs import show_logs
from ui.screenshots import show_screenshots
from ui.settings import show_settings
from ui.about import show_about
from ui.demo import show_demo

# Session state initialization
if 'page' not in st.session_state:
    st.session_state.page = 'Dashboard'
if 'automation_running' not in st.session_state:
    st.session_state.automation_running = False
if 'automation_progress' not in st.session_state:
    st.session_state.automation_progress = 0
if 'automation_logs' not in st.session_state:
    st.session_state.automation_logs = []
if 'current_request' not in st.session_state:
    st.session_state.current_request = None
if 'workflow_status' not in st.session_state:
    st.session_state.workflow_status = {}

# Sidebar navigation
st.sidebar.title("🔐 Identity Provisioning")
st.sidebar.markdown("---")

# Navigation menu
page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "🎬 Demo",
        "🚀 Automation",
        "⚙️ Configuration",
        "📄 Reports",
        "📸 Screenshots",
        "📜 Logs",
        "ℹ️ About"
    ],
    index=0,
    label_visibility="collapsed"
)

# Map menu to page names
page_mapping = {
    "🏠 Dashboard": "Dashboard",
    "🎬 Demo": "Demo",
    "🚀 Automation": "Automation",
    "⚙️ Configuration": "Configuration",
    "📄 Reports": "Reports",
    "📸 Screenshots": "Screenshots",
    "📜 Logs": "Logs",
    "ℹ️ About": "About"
}

st.session_state.page = page_mapping[page]

# Sidebar footer
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="text-align: center; color: rgba(255,255,255,0.7); font-size: 0.8rem;">
<p>Enterprise Identity<br>Provisioning Platform</p>
<p style="margin-top: 0.5rem;">Version 1.0</p>
</div>
""", unsafe_allow_html=True)

# Main content area
st.markdown('<div class="main-header">Enterprise Identity Provisioning Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Automated Employee Onboarding & Identity Management</div>', unsafe_allow_html=True)

# Route to appropriate page
if st.session_state.page == "Dashboard":
    show_dashboard()
elif st.session_state.page == "Demo":
    show_demo()
elif st.session_state.page == "Automation":
    show_automation()
elif st.session_state.page == "Configuration":
    show_settings()
elif st.session_state.page == "Reports":
    show_reports()
elif st.session_state.page == "Screenshots":
    show_screenshots()
elif st.session_state.page == "Logs":
    show_logs()
elif st.session_state.page == "About":
    show_about()
