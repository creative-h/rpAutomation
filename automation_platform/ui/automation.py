"""
Automation Page
Displays automation controls, workflow, and live execution
"""

import streamlit as st
import time
import threading
from datetime import datetime


def show_automation():
    """Display the automation control page"""
    
    # Automation Status Section
    st.markdown("### 🎯 Automation Status")
    st.markdown("---")
    
    status_col1, status_col2 = st.columns(2)
    
    with status_col1:
        if st.session_state.automation_running:
            st.markdown("""
            <div class="metric-card" style="background: #ecfdf5; border-color: #10b981;">
                <h4 style="margin: 0; color: #10b981;">Status: Running</h4>
                <p style="margin: 0.5rem 0; color: #64748b;">Automation in progress...</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="metric-card" style="background: #f8fafc; border-color: #3b82f6;">
                <h4 style="margin: 0; color: #3b82f6;">Status: Ready</h4>
                <p style="margin: 0.5rem 0; color: #64748b;">Ready to start automation</p>
            </div>
            """, unsafe_allow_html=True)
    
    with status_col2:
        st.markdown("""
        <div class="metric-card">
            <h4 style="margin: 0; color: #1e3a8a;">Last Execution</h4>
            <p style="margin: 0.5rem 0; color: #64748b;">Today at 14:31:25</p>
            <p style="margin: 0; color: #10b981; font-weight: 600;">✓ Successful</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Configuration Display
    st.markdown("### ⚙️ Configuration")
    
    config_col1, config_col2 = st.columns(2)
    
    with config_col1:
        st.markdown("**Source Portal**")
        st.json({
            "URL": "http://185.131.55.105:8057/Login",
            "Username": "amit.mishra",
            "Password": "***"
        })
    
    with config_col2:
        st.markdown("**Target Systems**")
        st.markdown("☑ Active Directory")
        st.markdown("☑ ELMS")
        st.markdown("☐ Microsoft 365")
        st.markdown("☐ Exchange")
    
    st.markdown("---")
    
    # Workflow Visualization
    st.markdown("### 🔄 Automation Workflow")
    
    workflow_steps = [
        "Read Request",
        "Validate",
        "Create AD User",
        "Verify AD",
        "Create ELMS User",
        "Verify ELMS",
        "Approve Request",
        "Generate Report"
    ]
    
    # Display workflow steps with status
    for i, step in enumerate(workflow_steps):
        status = get_workflow_step_status(step)
        status_class = get_status_class(status)
        
        st.markdown(f"""
        <div class="workflow-step {status_class}">
            <strong>{i + 1}. {step}</strong>
            <span style="float: right;">{status}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Progress Bar
    st.markdown("### 📊 Progress")
    
    progress_bar = st.progress(st.session_state.automation_progress / 100)
    st.markdown(f"**Progress:** {st.session_state.automation_progress}%")
    
    st.markdown("---")
    
    # Start Automation Button
    if not st.session_state.automation_running:
        if st.button("🚀 Start Automation", key="start_automation", use_container_width=True, type="primary"):
            start_automation()
    else:
        if st.button("⏹️ Stop Automation", key="stop_automation", use_container_width=True):
            st.session_state.automation_running = False
            st.session_state.automation_progress = 0
            st.rerun()
    
    st.markdown("---")
    
    # Live Log Window
    st.markdown("### 📜 Live Logs")
    
    log_container = st.container()
    
    with log_container:
        st.markdown('<div class="log-window">', unsafe_allow_html=True)
        
        if st.session_state.automation_logs:
            for log_entry in st.session_state.automation_logs[-20:]:  # Show last 20 entries
                st.markdown(f"""
                <div class="log-entry">
                    <span class="log-timestamp">{log_entry['timestamp']}</span>
                    <span>{log_entry['message']}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="log-entry"><span class="log-timestamp">--:--:--</span><span>Waiting for automation to start...</span></div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Current Request Panel
    st.markdown("### 📋 Current Request")
    
    if st.session_state.current_request:
        request = st.session_state.current_request
        
        st.markdown(f"""
        <div class="metric-card">
            <p><strong>Request Type:</strong> {request.get('type', 'N/A')}</p>
            <p><strong>Request Category:</strong> {request.get('category', 'N/A')}</p>
            <p><strong>Employee:</strong> {request.get('employee', 'N/A')}</p>
            <p><strong>AD ID:</strong> {request.get('ad_id', 'N/A')}</p>
            <p><strong>Department:</strong> {request.get('department', 'N/A')}</p>
            <p><strong>Location:</strong> {request.get('location', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("No request currently being processed")


def get_workflow_step_status(step):
    """Get the status of a workflow step"""
    if st.session_state.automation_running:
        # In a real implementation, this would check actual workflow state
        # For demo, return running/pending based on progress
        step_index = {
            "Read Request": 0,
            "Validate": 1,
            "Create AD User": 2,
            "Verify AD": 3,
            "Create ELMS User": 4,
            "Verify ELMS": 5,
            "Approve Request": 6,
            "Generate Report": 7
        }.get(step, 0)
        
        progress_threshold = (step_index + 1) * 12.5  # Each step is ~12.5%
        
        if st.session_state.automation_progress >= progress_threshold + 12.5:
            return "✓ Completed"
        elif st.session_state.automation_progress >= progress_threshold:
            return "⏳ Running"
        else:
            return "⏳ Pending"
    else:
        return "⏳ Pending"


def get_status_class(status):
    """Get CSS class based on status"""
    if "Completed" in status:
        return "completed"
    elif "Running" in status:
        return "running"
    else:
        return "pending"


def start_automation():
    """Start the automation process"""
    st.session_state.automation_running = True
    st.session_state.automation_progress = 0
    st.session_state.automation_logs = []
    
    # Simulate automation in a separate thread
    def run_automation():
        steps = [
            (10, "Browser initialized"),
            (20, "Logging into Source Portal"),
            (25, "Reading Request"),
            (30, "Employee: Amit Mishra"),
            (40, "Creating Active Directory User"),
            (65, "AD User Created"),
            (70, "Opening ELMS"),
            (75, "Creating ELMS User"),
            (85, "User Created Successfully"),
            (90, "Approving Request"),
            (100, "Automation Completed")
        ]
        
        for progress, message in steps:
            time.sleep(2)  # Simulate processing time
            st.session_state.automation_progress = progress
            st.session_state.automation_logs.append({
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "message": message
            })
            
            # Update current request
            if progress == 30:
                st.session_state.current_request = {
                    "type": "Creation",
                    "category": "Create User on ELMS",
                    "employee": "Amit Mishra",
                    "ad_id": "amit.mishra",
                    "department": "IT",
                    "location": "INDORE"
                }
        
        st.session_state.automation_running = False
    
    # Start automation in background thread
    thread = threading.Thread(target=run_automation)
    thread.daemon = True
    thread.start()
    
    st.rerun()
