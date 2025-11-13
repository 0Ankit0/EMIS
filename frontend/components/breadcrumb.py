"""
Breadcrumb Navigation Component
"""
import streamlit as st
from typing import List, Tuple


def show_breadcrumb(items: List[Tuple[str, str]]):
    """
    Show breadcrumb navigation
    items: List of (label, page_key) tuples
    """
    breadcrumb_html = '<div style="margin-bottom: 20px;">'
    
    for i, (label, page_key) in enumerate(items):
        if i > 0:
            breadcrumb_html += ' <span style="color: #999;">›</span> '
        
        if i == len(items) - 1:
            # Current page - not clickable
            breadcrumb_html += f'<span style="color: #333; font-weight: bold;">{label}</span>'
        else:
            # Clickable link
            breadcrumb_html += f'<a href="#" onclick="return false;" style="color: #0066cc; text-decoration: none;">{label}</a>'
    
    breadcrumb_html += '</div>'
    
    st.markdown(breadcrumb_html, unsafe_allow_html=True)


def show_back_button(label: str = "← Back", page_key: Optional[str] = None):
    """Show back button"""
    if st.button(label):
        if page_key:
            st.session_state.page = page_key
        st.rerun()
