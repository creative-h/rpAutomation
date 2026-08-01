"""
Screenshots Page
Displays screenshots captured during automation
"""

import streamlit as st
import os
import sys
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def show_screenshots():
    """Display the screenshots page"""
    
    # Screenshot Controls Section
    st.markdown("### 📸 Screenshot Controls")
    st.markdown("---")
    
    control_col1, control_col2, control_col3 = st.columns(3)
    
    with control_col1:
        date_filter = st.selectbox(
            "Date Range",
            ["Today", "Last 7 Days", "Last 30 Days", "All Time"],
            index=0
        )
    
    with control_col2:
        category_filter = st.selectbox(
            "Category",
            ["All", "Login", "Request Page", "User Creation", "Approval", "Error"],
            index=0
        )
    
    with control_col3:
        if st.button("🔄 Refresh Screenshots", use_container_width=True):
            st.success("Screenshots refreshed!")
    
    st.markdown("---")
    
    # Screenshot Statistics
    st.markdown("### 📊 Screenshot Statistics")
    
    stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
    
    with stats_col1:
        st.metric(
            label="Total Screenshots",
            value=1248,
            delta="+45 today",
            delta_color="normal"
        )
    
    with stats_col2:
        st.metric(
            label="Storage Used",
            value="2.4 GB",
            delta="+120 MB today",
            delta_color="normal"
        )
    
    with stats_col3:
        st.metric(
            label="Avg Size",
            value="1.9 MB",
            delta="Stable",
            delta_color="normal"
        )
    
    with stats_col4:
        st.metric(
            label="Retention",
            value="30 Days",
            delta="Configured",
            delta_color="normal"
        )
    
    st.markdown("---")
    
    # Screenshot Gallery
    st.markdown("### 🖼️ Screenshot Gallery")
    
    # Sample screenshot data
    screenshots = get_sample_screenshots()
    
    # Apply filters
    if category_filter != "All":
        screenshots = [s for s in screenshots if s['category'] == category_filter]
    
    # Display screenshots in grid
    if screenshots:
        cols_per_row = 4
        for i in range(0, len(screenshots), cols_per_row):
            cols = st.columns(cols_per_row)
            for j in range(cols_per_row):
                if i + j < len(screenshots):
                    screenshot = screenshots[i + j]
                    with cols[j]:
                        st.markdown(f"""
                        <div style="text-align: center; margin-bottom: 1rem;">
                            <div style="background: #f1f5f9; border-radius: 8px; padding: 1rem; height: 150px; display: flex; align-items: center; justify-content: center; border: 2px dashed #cbd5e1;">
                                <span style="color: #64748b; font-size: 0.9rem;">📷 {screenshot['name']}</span>
                            </div>
                            <p style="margin: 0.5rem 0 0 0; font-weight: 600; font-size: 0.9rem;">{screenshot['title']}</p>
                            <p style="margin: 0; color: #64748b; font-size: 0.8rem;">{screenshot['timestamp']}</p>
                            <p style="margin: 0; color: #3b82f6; font-size: 0.8rem;">{screenshot['category']}</p>
                        </div>
                        """, unsafe_allow_html=True)
    else:
        st.info("No screenshots found for the selected filters.")
    
    st.markdown(f"**Showing {len(screenshots)} screenshots**")
    
    st.markdown("---")
    
    # Screenshot Preview (when clicked)
    st.markdown("### 🔍 Screenshot Preview")
    
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: #f1f5f9; border-radius: 8px; border: 2px dashed #cbd5e1;">
        <p style="color: #64748b; font-size: 1rem;">Click on a screenshot above to view full-size preview</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Configuration Options
    st.markdown("### ⚙️ Screenshot Configuration")
    
    config_col1, config_col2 = st.columns(2)
    
    with config_col1:
        auto_capture = st.checkbox(
            "Auto-capture screenshots",
            value=True,
            help="Automatically capture screenshots during automation"
        )
        
        capture_on_error = st.checkbox(
            "Capture on error only",
            value=False,
            help="Only capture screenshots when errors occur"
        )
    
    with config_col2:
        retention_days = st.slider(
            "Retention Period (Days)",
            min_value=7,
            max_value=90,
            value=30,
            help="Number of days to keep screenshots"
        )
        
        image_quality = st.selectbox(
            "Image Quality",
            ["Low (faster)", "Medium", "High (slower)"],
            index=1
        )
    
    if st.button("💾 Save Configuration", use_container_width=True):
        st.success("Configuration saved!")


def get_sample_screenshots():
    """Generate sample screenshot data for demonstration"""
    return [
        {
            "name": "login_001.png",
            "title": "Portal Login",
            "timestamp": "14:30:27",
            "category": "Login"
        },
        {
            "name": "request_001.png",
            "title": "Request List",
            "timestamp": "14:30:31",
            "category": "Request Page"
        },
        {
            "name": "details_001.png",
            "title": "Request Details",
            "timestamp": "14:30:33",
            "category": "Request Page"
        },
        {
            "name": "ad_create_001.png",
            "title": "AD User Creation",
            "timestamp": "14:30:38",
            "category": "User Creation"
        },
        {
            "name": "ad_verify_001.png",
            "title": "AD Verification",
            "timestamp": "14:30:46",
            "category": "User Creation"
        },
        {
            "name": "elms_login_001.png",
            "title": "ELMS Login",
            "timestamp": "14:30:52",
            "category": "Login"
        },
        {
            "name": "elms_create_001.png",
            "title": "ELMS User Creation",
            "timestamp": "14:31:01",
            "category": "User Creation"
        },
        {
            "name": "approval_001.png",
            "title": "Request Approval",
            "timestamp": "14:31:18",
            "category": "Approval"
        },
        {
            "name": "success_001.png",
            "title": "Success Confirmation",
            "timestamp": "14:31:25",
            "category": "Approval"
        },
        {
            "name": "error_001.png",
            "title": "Error Screenshot",
            "timestamp": "13:44:45",
            "category": "Error"
        },
        {
            "name": "login_002.png",
            "title": "Portal Login",
            "timestamp": "13:43:50",
            "category": "Login"
        },
        {
            "name": "request_002.png",
            "title": "Request List",
            "timestamp": "13:43:55",
            "category": "Request Page"
        }
    ]
