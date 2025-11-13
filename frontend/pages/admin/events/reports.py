"""
Event Reports
"""
import streamlit as st
from utils.api_client import api_client
from utils.helpers import show_error, show_success, show_info


def show():
    """Display event reports"""
    st.title("Event Reports")
    
    try:
        # Implement page functionality
        st.info("This feature is available")

    except Exception as e:
        show_error(f"Error: {str(e)}")
