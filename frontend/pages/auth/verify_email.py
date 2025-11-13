"""
Email Verification Page
"""
import streamlit as st
from services.auth_service import auth_service
from utils.helpers import show_error, show_success


def show():
    """Display email verification page"""
    st.title("✉️ Email Verification")
    
    query_params = st.query_params
    token = query_params.get('token')
    
    if token:
        try:
            auth_service.verify_email(token)
            show_success("Email verified successfully!")
            st.balloons()
        except Exception as e:
            show_error(f"Verification failed: {str(e)}")
    else:
        st.info("Please check your email for the verification link")
