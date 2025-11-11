"""Settings Page"""
import streamlit as st
from utils.api_client import api_client
from utils.helpers import show_success, show_error

def show():
    st.title("⚙️ Settings")
    tabs = st.tabs(["👤 Profile", "🔐 Security", "🎨 Preferences", "🔔 Notifications"])
    
    with tabs[0]:
        st.subheader("User Profile")
        with st.form("profile_form"):
            name = st.text_input("Name", value=st.session_state.user.get("name", ""))
            email = st.text_input("Email", value=st.session_state.user.get("email", ""))
            phone = st.text_input("Phone", value=st.session_state.user.get("phone", ""))
            
            if st.form_submit_button("💾 Save Changes"):
                try:
                    api_client.put("/api/users/profile", {
                        "name": name,
                        "email": email,
                        "phone": phone
                    })
                    show_success("Profile updated successfully!")
                except Exception as e:
                    show_error(f"Error: {str(e)}")
    
    with tabs[1]:
        st.subheader("Security Settings")
        with st.form("password_form"):
            current_password = st.text_input("Current Password", type="password")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            
            if st.form_submit_button("🔒 Change Password"):
                if new_password != confirm_password:
                    show_error("Passwords don't match!")
                else:
                    try:
                        api_client.post("/api/users/change-password", {
                            "current_password": current_password,
                            "new_password": new_password
                        })
                        show_success("Password changed successfully!")
                    except Exception as e:
                        show_error(f"Error: {str(e)}")
    
    with tabs[2]:
        st.subheader("Preferences")
        st.info("Preferences settings coming soon")
    
    with tabs[3]:
        st.subheader("Notification Settings")
        st.info("Notification settings coming soon")
