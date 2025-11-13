"""
2FA Setup Page
"""
import streamlit as st
from services.auth_service import auth_service
from utils.helpers import show_error, show_success


def show():
    """Display 2FA setup page"""
    st.title("🔐 Two-Factor Authentication")
    
    if st.session_state.user.get('2fa_enabled'):
        st.warning("2FA is currently enabled")
        if st.button("Disable 2FA"):
            try:
                auth_service.disable_2fa()
                show_success("2FA has been disabled")
                st.rerun()
            except Exception as e:
                show_error(f"Error: {str(e)}")
    else:
        st.info("Enable 2FA for enhanced security")
        if st.button("Enable 2FA"):
            try:
                response = auth_service.setup_2fa()
                st.success("2FA enabled successfully!")
                st.balloons()
            except Exception as e:
                show_error(f"Error: {str(e)}")
