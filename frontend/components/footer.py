"""
Footer Component
"""
import streamlit as st
from datetime import datetime


def show_footer():
    """Show page footer"""
    current_year = datetime.now().year
    
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #6c757d; padding: 1rem 0;">
        <p>© {current_year} EMIS - Education Management Information System. All rights reserved.</p>
        <p style="font-size: 0.875rem;">
            <a href="#" style="color: #0066cc; text-decoration: none; margin: 0 10px;">Privacy Policy</a> | 
            <a href="#" style="color: #0066cc; text-decoration: none; margin: 0 10px;">Terms of Service</a> | 
            <a href="#" style="color: #0066cc; text-decoration: none; margin: 0 10px;">Contact Support</a>
        </p>
        <p style="font-size: 0.75rem;">Version 1.0.0</p>
    </div>
    """, unsafe_allow_html=True)
