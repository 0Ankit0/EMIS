"""
EMIS - Education Management Information System
Main Streamlit Application Entry Point
"""
import streamlit as st
from streamlit_option_menu import option_menu
from utils.helpers import init_session_state
from utils.api_client import api_client
from config.settings import PAGE_TITLE, PAGE_ICON, LAYOUT

# Configure page
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state="expanded"
)

# Initialize session state
init_session_state()


def show_login_page():
    """Display login page"""
    st.title("🎓 EMIS Login")
    st.markdown("### Education Management Information System")
    
    with st.form("login_form"):
        st.subheader("Sign In")
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            submit = st.form_submit_button("🔐 Login", use_container_width=True)
        
        if submit:
            if not username or not password:
                st.error("Please enter both username and password")
            else:
                with st.spinner("Authenticating..."):
                    try:
                        response = api_client.login(username, password)
                        st.session_state.authenticated = True
                        st.session_state.access_token = response.get("access_token")
                        st.session_state.user = response.get("user")
                        st.session_state.user_role = response.get("user", {}).get("role", "student")
                        st.success("Login successful!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Login failed: {str(e)}")


def show_dashboard():
    """Display main dashboard"""
    from pages import (
        dashboard,
        students,
        admissions,
        academics,
        hr,
        library,
        finance,
        reports,
        settings
    )
    
    # Sidebar navigation
    with st.sidebar:
        st.title(f"👤 {st.session_state.user.get('name', 'User')}")
        st.caption(f"Role: {st.session_state.user_role.title()}")
        st.divider()
        
        # Main menu
        selected = option_menu(
            menu_title="Main Menu",
            options=[
                "Dashboard",
                "Students",
                "Admissions",
                "Academics",
                "HR & Payroll",
                "Library",
                "Finance",
                "Reports",
                "Settings"
            ],
            icons=[
                "speedometer2",
                "people",
                "file-earmark-text",
                "book",
                "briefcase",
                "journal-text",
                "currency-dollar",
                "bar-chart",
                "gear"
            ],
            menu_icon="cast",
            default_index=0,
            key="main_menu"
        )
        
        st.divider()
        
        if st.button("🚪 Logout", use_container_width=True):
            api_client.logout()
            st.rerun()
    
    # Display selected page
    if selected == "Dashboard":
        dashboard.show()
    elif selected == "Students":
        students.show()
    elif selected == "Admissions":
        admissions.show()
    elif selected == "Academics":
        academics.show()
    elif selected == "HR & Payroll":
        hr.show()
    elif selected == "Library":
        library.show()
    elif selected == "Finance":
        finance.show()
    elif selected == "Reports":
        reports.show()
    elif selected == "Settings":
        settings.show()


def main():
    """Main application entry point"""
    # Check authentication
    if not st.session_state.get("authenticated", False):
        show_login_page()
    else:
        show_dashboard()


if __name__ == "__main__":
    main()
