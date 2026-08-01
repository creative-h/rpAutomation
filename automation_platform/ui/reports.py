"""
Reports Page
Displays automation reports and metrics
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def show_reports():
    """Display the reports page"""
    
    # Report Summary Section
    st.markdown("### 📊 Report Summary")
    st.markdown("---")
    
    summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
    
    with summary_col1:
        st.metric(
            label="Total Runs",
            value=156,
            delta="+12 this week",
            delta_color="normal"
        )
    
    with summary_col2:
        st.metric(
            label="Total Processed",
            value=1248,
            delta="+89 this week",
            delta_color="normal"
        )
    
    with summary_col3:
        st.metric(
            label="Successful",
            value=1235,
            delta="+88 this week",
            delta_color="normal"
        )
    
    with summary_col4:
        st.metric(
            label="Failed",
            value=13,
            delta="+1 this week",
            delta_color="inverse"
        )
    
    st.markdown("---")
    
    # Report Generation Controls
    st.markdown("### 🔧 Generate Report")
    
    control_col1, control_col2, control_col3 = st.columns(3)
    
    with control_col1:
        date_range = st.selectbox(
            "Date Range",
            ["Last 24 Hours", "Last 7 Days", "Last 30 Days", "Custom Range"]
        )
    
    with control_col2:
        report_type = st.selectbox(
            "Report Type",
            ["Full Report", "Success Only", "Failures Only", "By Department"]
        )
    
    with control_col3:
        format_type = st.selectbox(
            "Format",
            ["CSV", "PDF", "Excel"]
        )
    
    generate_col1, generate_col2 = st.columns(2)
    
    with generate_col1:
        if st.button("📄 Generate Report", use_container_width=True):
            st.success("Report generated successfully!")
    
    with generate_col2:
        if st.button("📥 Download Sample", use_container_width=True):
            # Generate sample data
            sample_data = get_sample_report_data()
            df = pd.DataFrame(sample_data)
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"automation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    st.markdown("---")
    
    # Detailed Report Table
    st.markdown("### 📋 Detailed Report")
    
    report_data = get_sample_report_data()
    df_report = pd.DataFrame(report_data)
    
    # Add filters
    col_filter1, col_filter2 = st.columns(2)
    
    with col_filter1:
        status_filter = st.multiselect(
            "Filter by Status",
            ["Success", "Failed", "Skipped"],
            default=["Success", "Failed", "Skipped"]
        )
    
    with col_filter2:
        department_filter = st.multiselect(
            "Filter by Department",
            ["IT", "HR", "Finance", "Operations", "Sales"],
            default=["IT", "HR", "Finance", "Operations", "Sales"]
        )
    
    # Apply filters
    if status_filter:
        df_report = df_report[df_report['Status'].isin(status_filter)]
    
    if department_filter:
        df_report = df_report[df_report['Department'].isin(department_filter)]
    
    # Display table
    st.dataframe(
        df_report,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Employee": st.column_config.TextColumn("Employee Name"),
            "AD_ID": st.column_config.TextColumn("AD Username"),
            "Department": st.column_config.TextColumn("Department"),
            "Location": st.column_config.TextColumn("Location"),
            "AD_Created": st.column_config.CheckboxColumn("AD Created"),
            "ELMS_Created": st.column_config.CheckboxColumn("ELMS Created"),
            "Approved": st.column_config.CheckboxColumn("Approved"),
            "Status": st.column_config.TextColumn("Status"),
            "Execution_Time": st.column_config.TextColumn("Execution Time"),
            "Timestamp": st.column_config.DatetimeColumn("Timestamp")
        }
    )
    
    st.markdown(f"**Showing {len(df_report)} records**")
    
    st.markdown("---")
    
    # Performance Metrics
    st.markdown("### 📈 Performance Metrics")
    
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    
    with metric_col1:
        st.markdown("""
        <div class="metric-card">
            <h4 style="margin: 0; color: #1e3a8a;">Average Execution Time</h4>
            <p style="margin: 0.5rem 0; font-size: 1.5rem; font-weight: 600; color: #3b82f6;">00:01:34</p>
            <p style="margin: 0; color: #64748b;">Per request</p>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_col2:
        st.markdown("""
        <div class="metric-card">
            <h4 style="margin: 0; color: #1e3a8a;">Success Rate</h4>
            <p style="margin: 0.5rem 0; font-size: 1.5rem; font-weight: 600; color: #10b981;">98.9%</p>
            <p style="margin: 0; color: #64748b;">Last 30 days</p>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_col3:
        st.markdown("""
        <div class="metric-card">
            <h4 style="margin: 0; color: #1e3a8a;">Peak Throughput</h4>
            <p style="margin: 0.5rem 0; font-size: 1.5rem; font-weight: 600; color: #3b82f6;">45/hr</p>
            <p style="margin: 0; color: #64748b;">Requests per hour</p>
        </div>
        """, unsafe_allow_html=True)


def get_sample_report_data():
    """Generate sample report data for demonstration"""
    return [
        {
            "Employee": "Amit Mishra",
            "AD_ID": "amit.mishra",
            "Department": "IT",
            "Location": "INDORE",
            "AD_Created": True,
            "ELMS_Created": True,
            "Approved": True,
            "Status": "Success",
            "Execution_Time": "00:01:23",
            "Timestamp": "2026-08-01 14:31:25"
        },
        {
            "Employee": "Joshi Joshiji",
            "AD_ID": "joshi.joshiji",
            "Department": "IT",
            "Location": "INDORE",
            "AD_Created": True,
            "ELMS_Created": False,
            "Approved": True,
            "Status": "Success",
            "Execution_Time": "00:01:45",
            "Timestamp": "2026-08-01 15:20:55"
        },
        {
            "Employee": "Priya Sharma",
            "AD_ID": "priya.sharma",
            "Department": "HR",
            "Location": "MUMBAI",
            "AD_Created": True,
            "ELMS_Created": True,
            "Approved": True,
            "Status": "Success",
            "Execution_Time": "00:01:18",
            "Timestamp": "2026-08-01 13:45:12"
        },
        {
            "Employee": "Rahul Kumar",
            "AD_ID": "rahul.kumar",
            "Department": "Finance",
            "Location": "DELHI",
            "AD_Created": True,
            "ELMS_Created": True,
            "Approved": True,
            "Status": "Success",
            "Execution_Time": "00:01:52",
            "Timestamp": "2026-08-01 12:30:45"
        },
        {
            "Employee": "Sneha Patel",
            "AD_ID": "sneha.patel",
            "Department": "Operations",
            "Location": "BANGALORE",
            "AD_Created": False,
            "ELMS_Created": False,
            "Approved": False,
            "Status": "Failed",
            "Execution_Time": "00:00:45",
            "Timestamp": "2026-08-01 11:15:30"
        },
        {
            "Employee": "Vikram Singh",
            "AD_ID": "vikram.singh",
            "Department": "Sales",
            "Location": "INDORE",
            "AD_Created": True,
            "ELMS_Created": True,
            "Approved": True,
            "Status": "Success",
            "Execution_Time": "00:01:38",
            "Timestamp": "2026-08-01 10:20:15"
        },
        {
            "Employee": "Anjali Verma",
            "AD_ID": "anjali.verma",
            "Department": "IT",
            "Location": "MUMBAI",
            "AD_Created": True,
            "ELMS_Created": True,
            "Approved": True,
            "Status": "Success",
            "Execution_Time": "00:01:27",
            "Timestamp": "2026-08-01 09:45:50"
        },
        {
            "Employee": "Deepak Gupta",
            "AD_ID": "deepak.gupta",
            "Department": "Finance",
            "Location": "DELHI",
            "AD_Created": True,
            "ELMS_Created": True,
            "Approved": True,
            "Status": "Success",
            "Execution_Time": "00:01:41",
            "Timestamp": "2026-08-01 08:30:25"
        }
    ]
