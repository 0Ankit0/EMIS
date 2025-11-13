"""
Password Reset Page
"""
import streamlit as st
from services.auth_service import auth_service
from utils.helpers import show_error, show_success
from utils.validators import validate_email


def show():
    """Display password reset page"""
    st.title("🔒 Reset Password")
    
    tab1, tab2 = st.tabs(["Request Reset", "Reset with Token"])
    
    with tab1:
        with st.form("request_reset_form"):
            email = st.text_input("Enter your email address")
            submitted = st.form_submit_button("Send Reset Link")
            
            if submitted:
                if not email:
                    show_error("Please enter your email")
                elif not validate_email(email):
                    show_error("Invalid email address")
                else:
                    try:
                        auth_service.request_password_reset(email)
                        show_success("Password reset link sent to your email!")
                    except Exception as e:
                        show_error(f"Error: {str(e)}")
    
    with tab2:
        with st.form("reset_password_form"):
            token = st.text_input("Reset Token")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            
            submitted = st.form_submit_button("Reset Password")
            
            if submitted:
                if not all([token, new_password, confirm_password]):
                    show_error("Please fill all fields")
                elif new_password != confirm_password:
                    show_error("Passwords do not match")
                else:
                    try:
                        auth_service.reset_password(token, new_password)
                        show_success("Password reset successful!")
                        st.balloons()
                    except Exception as e:
                        show_error(f"Error: {str(e)}")
