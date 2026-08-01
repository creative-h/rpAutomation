"""
About Page
Displays information about the platform
"""

import streamlit as st


def show_about():
    """Display the about page"""
    
    st.markdown("### ℹ️ About Enterprise Identity Provisioning Platform")
    st.markdown("---")
    
    # Platform Overview
    st.markdown("""
    <div class="metric-card" style="margin-bottom: 2rem;">
        <h2 style="margin: 0; color: #1e3a8a;">Enterprise Identity Provisioning Platform</h2>
        <p style="margin: 1rem 0; color: #64748b; font-size: 1.1rem;">
        A comprehensive automation solution for employee onboarding and identity management across enterprise systems.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Version Information
    st.markdown("#### 📋 Version Information")
    
    version_col1, version_col2, version_col3 = st.columns(3)
    
    with version_col1:
        st.markdown("""
        <div class="metric-card">
            <h4 style="margin: 0; color: #1e3a8a;">Version</h4>
            <p style="margin: 0.5rem 0; font-size: 1.5rem; font-weight: 600; color: #3b82f6;">1.0.0</p>
            <p style="margin: 0; color: #64748b;">Release: August 2026</p>
        </div>
        """, unsafe_allow_html=True)
    
    with version_col2:
        st.markdown("""
        <div class="metric-card">
            <h4 style="margin: 0; color: #1e3a8a;">Build</h4>
            <p style="margin: 0.5rem 0; font-size: 1.5rem; font-weight: 600; color: #3b82f6;">2026.08.01</p>
            <p style="margin: 0; color: #64748b;">Stable Release</p>
        </div>
        """, unsafe_allow_html=True)
    
    with version_col3:
        st.markdown("""
        <div class="metric-card">
            <h4 style="margin: 0; color: #1e3a8a;">License</h4>
            <p style="margin: 0.5rem 0; font-size: 1.5rem; font-weight: 600; color: #3b82f6;">Enterprise</p>
            <p style="margin: 0; color: #64748b;">Proprietary</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Architecture
    st.markdown("#### 🏗️ Architecture")
    
    st.markdown("""
    <div class="metric-card">
        <p style="margin: 0; color: #1e3a8a; font-weight: 600;">Technology Stack</p>
        <ul style="margin: 0.5rem 0; color: #64748b;">
            <li><strong>Frontend:</strong> Streamlit - Modern web interface</li>
            <li><strong>Backend:</strong> Python 3.11+ - Core automation engine</li>
            <li><strong>Automation:</strong> Playwright - Browser automation</li>
            <li><strong>Directory:</strong> LDAP/Active Directory - User management</li>
            <li><strong>Logging:</strong> Loguru - Advanced logging</li>
            <li><strong>Configuration:</strong> .env - Environment variables</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Design Principles
    st.markdown("#### 🎯 Design Principles")
    
    principle_col1, principle_col2 = st.columns(2)
    
    with principle_col1:
        st.markdown("""
        <div class="metric-card">
            <h4 style="margin: 0; color: #1e3a8a;">Code Quality</h4>
            <ul style="margin: 0.5rem 0; color: #64748b;">
                <li>Modular Architecture</li>
                <li>Page Object Model</li>
                <li>Clean Code Practices</li>
                <li>SOLID Principles</li>
                <li>Separation of Concerns</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with principle_col2:
        st.markdown("""
        <div class="metric-card">
            <h4 style="margin: 0; color: #1e3a8a;">Enterprise Features</h4>
            <ul style="margin: 0.5rem 0; color: #64748b;">
                <li>Scalable Design</li>
                <li>Error Handling</li>
                <li>Comprehensive Logging</li>
                <li>Configuration Management</li>
                <li>Security Best Practices</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # System Integrations
    st.markdown("#### 🔌 System Integrations")
    
    integration_col1, integration_col2, integration_col3 = st.columns(3)
    
    with integration_col1:
        st.markdown("""
        <div class="metric-card">
            <h4 style="margin: 0; color: #10b981;">✓ Active</h4>
            <ul style="margin: 0.5rem 0; color: #64748b;">
                <li>Source Portal</li>
                <li>Active Directory</li>
                <li>LDAP</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with integration_col2:
        st.markdown("""
        <div class="metric-card">
            <h4 style="margin: 0; color: #f59e0b;">⚠ In Progress</h4>
            <ul style="margin: 0.5rem 0; color: #64748b;">
                <li>ELMS System</li>
                <li>Microsoft 365</li>
                <li>Exchange</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with integration_col3:
        st.markdown("""
        <div class="metric-card">
            <h4 style="margin: 0; color: #64748b;">⏳ Planned</h4>
            <ul style="margin: 0.5rem 0; color: #64748b;">
                <li>Jira</li>
                <li>ServiceNow</li>
                <li>Custom APIs</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Features
    st.markdown("#### ✨ Key Features")
    
    feature_col1, feature_col2 = st.columns(2)
    
    with feature_col1:
        st.markdown("""
        <div class="metric-card">
            <h4 style="margin: 0; color: #1e3a8a;">Automation</h4>
            <ul style="margin: 0.5rem 0; color: #64748b;">
                <li>Fully automated user provisioning</li>
                <li>No manual intervention required</li>
                <li>Batch processing support</li>
                <li>Scheduled automation</li>
                <li>Real-time monitoring</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with feature_col2:
        st.markdown("""
        <div class="metric-card">
            <h4 style="margin: 0; color: #1e3a8a;">Security</h4>
            <ul style="margin: 0.5rem 0; color: #64748b;">
                <li>Secure credential management</li>
                <li>Force password change policy</li>
                <li>Group-based access control</li>
                <li>Audit trail logging</li>
                <li>Encrypted configuration</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Support Information
    st.markdown("#### 📞 Support Information")
    
    st.markdown("""
    <div class="metric-card">
        <p style="margin: 0; color: #1e3a8a; font-weight: 600;">Contact Information</p>
        <ul style="margin: 0.5rem 0; color: #64748b;">
            <li><strong>Email:</strong> support@swasti.com</li>
            <li><strong>Phone:</strong> +91-123-456-7890</li>
            <li><strong>Documentation:</strong> https://docs.swasti.com/identity-platform</li>
            <li><strong>Issue Tracker:</strong> https://github.com/swasti/identity-platform/issues</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Footer
    st.markdown("""
    <div style="text-align: center; color: #64748b; font-size: 0.9rem; margin-top: 2rem;">
        <p>© 2026 Swasti Solutions. All rights reserved.</p>
        <p>Enterprise Identity Provisioning Platform - Version 1.0.0</p>
    </div>
    """, unsafe_allow_html=True)
