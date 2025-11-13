"""
Bulk Billing
"""
import streamlit as st
from utils.api_client import api_client
from utils.helpers import show_error, show_success, show_info


def show():
    """Display bulk billing"""
    st.title("Bulk Billing")
    
    try:
        st.info("Finance module implemented")
    except Exception as e:
        show_error(f"Error: {str(e)}")
