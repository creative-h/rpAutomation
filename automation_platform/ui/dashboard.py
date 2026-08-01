"""
Dashboard Page
Displays KPI cards and system status
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def show_dashboard():
    """Display the dashboard with KPI cards and system status"""
    
    # KPI Cards Section
    st.markdown("### 📊 Performance Metrics")
    st.markdown("---")
    
    # Create KPI cards
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        pending_requests = get_pending_requests_count()
        st.metric(
            label="Pending Requests",
            value=pending_requests,
            delta="New requests",
            delta_color="normal"
        )
    
    with col2:
        processed_today = get_processed_today_count()
        st.metric(
            label="Processed Today",
            value=processed_today,
            delta=f"+{processed_today}",
            delta_color="normal"
        )
    
    with col3:
        success_rate = get_success_rate()
        st.metric(
            label="Success Rate",
            value=f"{success_rate:.1f}%",
            delta=f"{success_rate - 95:.1f}%",
            delta_color="normal" if success_rate >= 95 else "inverse"
        )
    
    with col4:
        failed_count = get_failed_count()
        st.metric(
            label="Failed",
            value=failed_count,
            delta="Errors",
            delta_color="inverse" if failed_count > 0 else "normal"
        )
    
    with col5:
        avg_execution_time = get_avg_execution_time()
        st.metric(
            label="Avg Execution Time",
            value=avg_execution_time,
            delta="Performance",
            delta_color="normal"
        )
    
    st.markdown("---")
    
    # System Status Section
    st.markdown("### 🔌 Connected Systems")
    
    system_col1, system_col2, system_col3 = st.columns(3)
    
    with system_col1:
        st.markdown("""
        <div class="metric-card">
            <h4 style="margin: 0; color: #1e3a8a;">Source Portal</h4>
            <p style="margin: 0.5rem 0; color: #10b981; font-weight: 600;">✓ Connected</p>
            <p style="margin: 0; color: #64748b; font-size: 0.9rem;">Last sync: Just now</p>
        </div>
        """, unsafe_allow_html=True)
    
    with system_col2:
        st.markdown("""
        <div class="metric-card">
            <h4 style="margin: 0; color: #1e3a8a;">Active Directory</h4>
            <p style="margin: 0.5rem 0; color: #10b981; font-weight: 600;">✓ Connected</p>
            <p style="margin: 0; color: #64748b; font-size: 0.9rem;">Domain: swasti.com</p>
        </div>
        """, unsafe_allow_html=True)
    
    with system_col3:
        st.markdown("""
        <div class="metric-card">
            <h4 style="margin: 0; color: #1e3a8a;">ELMS System</h4>
            <p style="margin: 0.5rem 0; color: #f59e0b; font-weight: 600;">⚠ Pending</p>
            <p style="margin: 0; color: #64748b; font-size: 0.9rem;">Integration in progress</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Recent Activity Section
    st.markdown("### 📋 Recent Activity")
    
    recent_activity = get_recent_activity()
    
    if recent_activity:
        df_activity = pd.DataFrame(recent_activity)
        st.dataframe(
            df_activity,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No recent activity to display. Run automation to see activity.")
    
    st.markdown("---")
    
    # Quick Actions Section
    st.markdown("### ⚡ Quick Actions")
    
    action_col1, action_col2, action_col3 = st.columns(3)
    
    with action_col1:
        if st.button("🚀 Start Automation", key="quick_start", use_container_width=True):
            st.session_state.page = "Automation"
            st.rerun()
    
    with action_col2:
        if st.button("📄 View Reports", key="quick_reports", use_container_width=True):
            st.session_state.page = "Reports"
            st.rerun()
    
    with action_col3:
        if st.button("⚙️ Configure", key="quick_config", use_container_width=True):
            st.session_state.page = "Configuration"
            st.rerun()


# Helper functions for dashboard data
def get_pending_requests_count():
    """Get count of pending requests"""
    # In production, this would query the portal or database
    # For demo, return a realistic number
    return 12


def get_processed_today_count():
    """Get count of requests processed today"""
    # In production, this would query the reports
    # For demo, return a realistic number
    return 8


def get_success_rate():
    """Get success rate percentage"""
    # In production, this would calculate from reports
    # For demo, return a realistic percentage
    return 100.0


def get_failed_count():
    """Get count of failed requests"""
    # In production, this would query the reports
    # For demo, return a realistic number
    return 0


def get_avg_execution_time():
    """Get average execution time"""
    # In production, this would calculate from logs
    # For demo, return a realistic time
    return "00:01:34"


def get_recent_activity():
    """Get recent activity data"""
    # In production, this would query the logs or database
    # For demo, return sample data
    return [
        {
            "Time": "14:31:25",
            "Action": "Automation Completed",
            "User": "joshi.joshiji",
            "Status": "✓ Success"
        },
        {
            "Time": "14:31:18",
            "Action": "Request Approved",
            "User": "joshi.joshiji",
            "Status": "✓ Success"
        },
        {
            "Time": "14:31:12",
            "Action": "ELMS User Created",
            "User": "joshi.joshiji",
            "Status": "✓ Success"
        },
        {
            "Time": "14:31:01",
            "Action": "ELMS Connection",
            "User": "System",
            "Status": "✓ Success"
        },
        {
            "Time": "14:30:52",
            "Action": "Opening ELMS",
            "User": "System",
            "Status": "✓ Success"
        },
        {
            "Time": "14:30:46",
            "Action": "AD User Created",
            "User": "joshi.joshiji",
            "Status": "✓ Success"
        },
        {
            "Time": "14:30:38",
            "Action": "Creating AD User",
            "User": "joshi.joshiji",
            "Status": "⏳ Running"
        },
        {
            "Time": "14:30:33",
            "Action": "Employee Validated",
            "User": "Amit Mishra",
            "Status": "✓ Success"
        },
        {
            "Time": "14:30:31",
            "Action": "Reading Request",
            "User": "System",
            "Status": "✓ Success"
        },
        {
            "Time": "14:30:27",
            "Action": "Logging into Portal",
            "User": "System",
            "Status": "✓ Success"
        }
    ]
