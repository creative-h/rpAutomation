"""
Demo Page
ASCII-style layout with simulated execution flow
"""

import streamlit as st
import time
import threading
from datetime import datetime


def show_demo():
    """Display the demo page with ASCII-style layout"""
    
    # Custom CSS for ASCII-style layout
    st.markdown("""
<style>
    .ascii-container {
        background: #1e293b;
        color: #e2e8f0;
        padding: 2rem;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        line-height: 1.6;
        border: 2px solid #3b82f6;
    }
    
    .ascii-header {
        color: #60a5fa;
        font-weight: bold;
        font-size: 1.1rem;
        margin-bottom: 1rem;
        border-bottom: 1px solid #3b82f6;
        padding-bottom: 0.5rem;
    }
    
    .ascii-section {
        margin: 1rem 0;
        padding: 0.5rem 0;
    }
    
    .ascii-label {
        color: #94a3b8;
        font-weight: bold;
    }
    
    .status-ready {
        color: #10b981;
        font-weight: bold;
    }
    
    .status-running {
        color: #f59e0b;
        font-weight: bold;
    }
    
    .status-completed {
        color: #10b981;
        font-weight: bold;
    }
    
    .system-connected {
        color: #10b98b;
    }
    
    .system-pending {
        color: #f59e0b;
    }
    
    .system-not-connected {
        color: #64748b;
    }
    
    .progress-bar {
        background: #334155;
        border-radius: 4px;
        padding: 0.5rem;
        margin: 0.5rem 0;
    }
    
    .progress-fill {
        background: linear-gradient(90deg, #3b82f6, #60a5fa);
        height: 20px;
        border-radius: 4px;
        transition: width 0.3s ease;
    }
    
    .log-entry {
        margin: 0.25rem 0;
        padding: 0.25rem 0;
    }
    
    .log-success {
        color: #10b981;
    }
    
    .log-running {
        color: #f59e0b;
    }
    
    .log-pending {
        color: #64748b;
    }
    
    .request-detail {
        color: #60a5fa;
        margin: 0.25rem 0;
    }
    
    .start-button {
        background: linear-gradient(135deg, #3b82f6, #1e3a8a);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 8px;
        font-weight: bold;
        font-size: 1.1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        margin: 1rem 0;
    }
    
    .start-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }
    
    .start-button:disabled {
        background: #64748b;
        cursor: not-allowed;
        transform: none;
    }
</style>
""", unsafe_allow_html=True)
    
    # Initialize session state
    if 'demo_running' not in st.session_state:
        st.session_state.demo_running = False
    if 'demo_progress' not in st.session_state:
        st.session_state.demo_progress = 0
    if 'demo_current_step' not in st.session_state:
        st.session_state.demo_current_step = "Ready to start"
    if 'demo_logs' not in st.session_state:
        st.session_state.demo_logs = []
    if 'demo_request' not in st.session_state:
        st.session_state.demo_request = None
    
    # ASCII-style container
    st.markdown('<div class="ascii-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="ascii-header">
    ┌─────────────────────────────────────────────────────────────────────┐<br>
    │        Enterprise Identity Provisioning Platform                    │<br>
    ├─────────────────────────────────────────────────────────────────────┤
    """, unsafe_allow_html=True)
    
    # Status
    if st.session_state.demo_running:
        status_icon = "🟡"
        status_text = "Running"
        status_class = "status-running"
    else:
        status_icon = "🟢"
        status_text = "Ready"
        status_class = "status-ready"
    
    st.markdown(f"""
    <div class="ascii-section">
    <span class="ascii-label">Status :</span> 
    <span class="{status_class}">{status_icon} {status_text}</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("│                                                                     │", unsafe_allow_html=True)
    
    # Connected Systems
    st.markdown('<div class="ascii-section"><span class="ascii-label">Connected Systems</span></div>', unsafe_allow_html=True)
    st.markdown("""
    │ 🟢 Request Portal   🟢 Active Directory (swasti.com)   ⚪ ELMS   ⚪ Microsoft 365 │
    """, unsafe_allow_html=True)
    
    st.markdown("│                                                                     │", unsafe_allow_html=True)
    
    # Start Button
    st.markdown("│                 ", unsafe_allow_html=True)
    
    if not st.session_state.demo_running:
        if st.button("🚀 Start Provisioning Automation", key="demo_start", use_container_width=True):
            start_demo()
    else:
        st.markdown('<button disabled style="background: #64748b; color: white; border: none; padding: 1rem 2rem; border-radius: 8px; font-weight: bold; cursor: not-allowed;">⏳ Automation Running...</button>', unsafe_allow_html=True)
    
    st.markdown("                 │", unsafe_allow_html=True)
    
    # Progress Bar
    st.markdown("├─────────────────────────────────────────────────────────────────────┤", unsafe_allow_html=True)
    st.markdown('<div class="ascii-section"><span class="ascii-label">Progress</span></div>', unsafe_allow_html=True)
    
    progress_percentage = st.session_state.demo_progress
    filled_width = progress_percentage
    empty_width = 100 - progress_percentage
    
    progress_bar_visual = "█" * (filled_width // 2) + "░" * (empty_width // 2)
    st.markdown(f"""
    │ {progress_bar_visual} {progress_percentage}%                         │
    """, unsafe_allow_html=True)
    
    # Current Step
    st.markdown("├─────────────────────────────────────────────────────────────────────┤", unsafe_allow_html=True)
    st.markdown('<div class="ascii-section"><span class="ascii-label">Current Step</span></div>', unsafe_allow_html=True)
    
    if st.session_state.demo_running:
        current_step_icon = "🔄"
    else:
        current_step_icon = "⏳"
    
    st.markdown(f"""
    │ {current_step_icon} {st.session_state.demo_current_step}                                   │
    """, unsafe_allow_html=True)
    
    # Live Execution Log
    st.markdown("├─────────────────────────────────────────────────────────────────────┤", unsafe_allow_html=True)
    st.markdown('<div class="ascii-section"><span class="ascii-label">Live Execution Log</span></div>', unsafe_allow_html=True)
    
    if st.session_state.demo_logs:
        for log in st.session_state.demo_logs:
            log_class = "log-success" if log['status'] == "completed" else "log-running" if log['status'] == "running" else "log-pending"
            log_icon = "✔" if log['status'] == "completed" else "⏳" if log['status'] == "running" else "⏸"
            st.markdown(f"""
            <div class="log-entry {log_class}">
            │ {log_icon} {log['message']}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="log-entry log-pending">
        │ ⏸ Waiting to start...
        </div>
        """, unsafe_allow_html=True)
    
    # Current Request
    st.markdown("├─────────────────────────────────────────────────────────────────────┤", unsafe_allow_html=True)
    st.markdown('<div class="ascii-section"><span class="ascii-label">Current Request</span></div>', unsafe_allow_html=True)
    
    if st.session_state.demo_request:
        request = st.session_state.demo_request
        st.markdown(f"""
        <div class="request-detail">│ Employee   : {request['employee']}</div>
        <div class="request-detail">│ AD ID      : {request['ad_id']}</div>
        <div class="request-detail">│ Department : {request['department']}</div>
        <div class="request-detail">│ Location   : {request['location']}</div>
        <div class="request-detail">│ Target OU  : {request['ou']}</div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="request-detail">│ Employee   : --</div>
        <div class="request-detail">│ AD ID      : --</div>
        <div class="request-detail">│ Department : --</div>
        <div class="request-detail">│ Location   : --</div>
        <div class="request-detail">│ Target OU  : --</div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("└─────────────────────────────────────────────────────────────────────┘", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Auto-refresh if running
    if st.session_state.demo_running:
        time.sleep(0.5)
        st.rerun()


def start_demo():
    """Start the demo automation flow"""
    st.session_state.demo_running = True
    st.session_state.demo_progress = 0
    st.session_state.demo_logs = []
    st.session_state.demo_request = None
    
    # Define workflow steps (AD Provisioning only for swasti.com)
    workflow_steps = [
        (0, "Browser Started", "Ready to start"),
        (10, "Logged into Portal", "Logging into Source Portal..."),
        (20, "Request Retrieved", "Retrieving request from portal..."),
        (25, "Employee Data Validated", "Validating employee data..."),
        (30, "Connecting to AD (swasti.com)", "Connecting to Active Directory..."),
        (40, "AD Connection Established", "Creating AD user in swasti.com..."),
        (60, "AD User Created (OU=IT_DEPT)", "Setting user password..."),
        (70, "Password Set", "Enabling account..."),
        (80, "Account Enabled", "Forcing password change..."),
        (90, "Password Change Forced", "Verifying user in AD..."),
        (95, "User Verified in AD", "Approving request in portal..."),
        (100, "Request Approved", "Generating report..."),
        (100, "AD Provisioning Completed", "Completed successfully")
    ]
    
    # Set current request
    st.session_state.demo_request = {
        "employee": "Amit Mishra",
        "ad_id": "amit.mishra",
        "location": "Indore",
        "department": "IT",
        "ou": "OU=IT_DEPT,OU=swastisolutions,DC=swasti,DC=com"
    }
    
    # Run demo in background thread
    def run_demo_flow():
        for progress, log_message, current_step in workflow_steps:
            time.sleep(1.5)  # Simulate processing time
            st.session_state.demo_progress = progress
            st.session_state.demo_current_step = current_step
            st.session_state.demo_logs.append({
                "message": log_message,
                "status": "completed" if progress > 0 else "running"
            })
        
        st.session_state.demo_running = False
        st.session_state.demo_current_step = "Ready to start"
    
    thread = threading.Thread(target=run_demo_flow)
    thread.daemon = True
    thread.start()
