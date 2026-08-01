"""
Logs Page
Displays system logs with filtering and search
"""

import streamlit as st
import os
import sys
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def show_logs():
    """Display the logs page"""
    
    # Log Controls Section
    st.markdown("### 📜 Log Controls")
    st.markdown("---")
    
    control_col1, control_col2, control_col3, control_col4 = st.columns(4)
    
    with control_col1:
        log_level = st.selectbox(
            "Log Level",
            ["All", "INFO", "WARNING", "ERROR", "DEBUG"],
            index=0
        )
    
    with control_col2:
        time_range = st.selectbox(
            "Time Range",
            ["Last Hour", "Last 6 Hours", "Last 24 Hours", "Last 7 Days", "All Time"],
            index=2
        )
    
    with control_col3:
        search_term = st.text_input(
            "Search",
            placeholder="Search logs..."
        )
    
    with control_col4:
        if st.button("🔄 Refresh Logs", use_container_width=True):
            st.success("Logs refreshed!")
    
    st.markdown("---")
    
    # Log Statistics
    st.markdown("### 📊 Log Statistics")
    
    stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
    
    with stats_col1:
        st.metric(
            label="Total Entries",
            value=15420,
            delta="+234 today",
            delta_color="normal"
        )
    
    with stats_col2:
        st.metric(
            label="INFO",
            value=14250,
            delta="+220 today",
            delta_color="normal"
        )
    
    with stats_col3:
        st.metric(
            label="WARNING",
            value=980,
            delta="+12 today",
            delta_color="normal"
        )
    
    with stats_col4:
        st.metric(
            label="ERROR",
            value=190,
            delta="+2 today",
            delta_color="inverse"
        )
    
    st.markdown("---")
    
    # Log Display
    st.markdown("### 📋 Log Entries")
    
    # Sample log data
    log_entries = get_sample_logs()
    
    # Apply filters
    if log_level != "All":
        log_entries = [log for log in log_entries if log['level'] == log_level]
    
    if search_term:
        log_entries = [log for log in log_entries if search_term.lower() in log['message'].lower()]
    
    # Display logs
    st.markdown('<div class="log-window">', unsafe_allow_html=True)
    
    for log_entry in log_entries[:50]:  # Show first 50 entries
        level_color = get_level_color(log_entry['level'])
        
        st.markdown(f"""
        <div class="log-entry">
            <span class="log-timestamp">{log_entry['timestamp']}</span>
            <span style="color: {level_color}; font-weight: 600; margin-right: 0.5rem;">[{log_entry['level']}]</span>
            <span>{log_entry['message']}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown(f"**Showing {min(50, len(log_entries))} of {len(log_entries)} entries**")
    
    st.markdown("---")
    
    # Download Options
    st.markdown("### 📥 Download Logs")
    
    download_col1, download_col2 = st.columns(2)
    
    with download_col1:
        if st.button("📄 Download as Text", use_container_width=True):
            st.success("Log file downloaded!")
    
    with download_col2:
        if st.button("📊 Download as CSV", use_container_width=True):
            st.success("Log CSV downloaded!")


def get_level_color(level):
    """Get color for log level"""
    colors = {
        "INFO": "#3b82f6",
        "WARNING": "#f59e0b",
        "ERROR": "#ef4444",
        "DEBUG": "#8b5cf6"
    }
    return colors.get(level, "#64748b")


def get_sample_logs():
    """Generate sample log entries for demonstration"""
    return [
        {
            "timestamp": "14:31:25",
            "level": "INFO",
            "message": "Automation completed successfully"
        },
        {
            "timestamp": "14:31:18",
            "level": "INFO",
            "message": "Request approved in portal"
        },
        {
            "timestamp": "14:31:12",
            "level": "INFO",
            "message": "ELMS user created successfully"
        },
        {
            "timestamp": "14:31:01",
            "level": "INFO",
            "message": "Connected to ELMS system"
        },
        {
            "timestamp": "14:30:52",
            "level": "INFO",
            "message": "Opening ELMS portal"
        },
        {
            "timestamp": "14:30:46",
            "level": "INFO",
            "message": "AD user created: joshi.joshiji"
        },
        {
            "timestamp": "14:30:38",
            "level": "INFO",
            "message": "Creating Active Directory user"
        },
        {
            "timestamp": "14:30:33",
            "level": "INFO",
            "message": "Employee data validated: Amit Mishra"
        },
        {
            "timestamp": "14:30:31",
            "level": "INFO",
            "message": "Reading request from portal"
        },
        {
            "timestamp": "14:30:27",
            "level": "INFO",
            "message": "Logged into source portal successfully"
        },
        {
            "timestamp": "14:30:22",
            "level": "INFO",
            "message": "Browser initialized"
        },
        {
            "timestamp": "14:30:15",
            "level": "INFO",
            "message": "Starting automation workflow"
        },
        {
            "timestamp": "14:29:45",
            "level": "WARNING",
            "message": "Portal response time slower than usual (3.2s)"
        },
        {
            "timestamp": "14:28:30",
            "level": "INFO",
            "message": "Configuration loaded successfully"
        },
        {
            "timestamp": "14:28:15",
            "level": "INFO",
            "message": "Application started"
        },
        {
            "timestamp": "13:45:12",
            "level": "INFO",
            "message": "Previous automation completed"
        },
        {
            "timestamp": "13:44:45",
            "level": "ERROR",
            "message": "LDAP connection timeout - retrying..."
        },
        {
            "timestamp": "13:44:30",
            "level": "WARNING",
            "message": "LDAP server response time elevated"
        },
        {
            "timestamp": "13:44:15",
            "level": "INFO",
            "message": "Connecting to LDAP server"
        },
        {
            "timestamp": "13:43:50",
            "level": "DEBUG",
            "message": "Request data: employee_id=joshi1, department=INDORE"
        }
    ]
