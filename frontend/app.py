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
    """Display main dashboard based on user role"""
    from utils.navigation import get_menu_items, get_page_title
    
    user_role = st.session_state.user_role
    menu_items = get_menu_items(user_role)
    
    # Sidebar navigation
    with st.sidebar:
        st.title(f"👤 {st.session_state.user.get('name', 'User')}")
        st.caption(f"Role: {user_role.title()}")
        st.divider()
        
        # Main menu
        options = [item['title'] for item in menu_items]
        icons = [item['icon'] for item in menu_items]
        
        selected = option_menu(
            menu_title="Main Menu",
            options=options,
            icons=icons,
            menu_icon="cast",
            default_index=0,
            key="main_menu"
        )
        
        st.divider()
        
        if st.button("🚪 Logout", use_container_width=True):
            api_client.logout()
            st.rerun()
    
    # Get selected page key
    selected_item = next((item for item in menu_items if item['title'] == selected), None)
    
    if selected_item:
        page_key = selected_item['page']
        route_to_page(page_key)
    else:
        st.error("Page not found")


def route_to_page(page_key):
    """Route to the appropriate page based on page key"""
    # Import pages dynamically to avoid circular imports
    
    # Common pages
    if page_key == "dashboard":
        from pages import dashboard
        dashboard.show()
    elif page_key == "profile":
        from pages.common import profile
        profile.show()
    
    # Student pages
    elif page_key == "student_courses":
        from pages.student import courses
        courses.show()
    elif page_key == "student_assignments":
        from pages.student import assignments
        assignments.show()
    elif page_key == "student_attendance":
        from pages.student import attendance
        attendance.show()
    elif page_key == "student_exams":
        from pages.student import exams
        exams.show()
    elif page_key == "student_fees":
        from pages.student import fees
        fees.show()
    elif page_key == "student_library":
        from pages.student import library
        library.show()
    
    # Faculty pages
    elif page_key == "faculty_courses":
        from pages.faculty import courses
        courses.show()
    elif page_key == "faculty_attendance":
        from pages.faculty import attendance
        attendance.show()
    elif page_key == "faculty_assignments":
        from pages.faculty import assignments
        assignments.show()
    elif page_key == "faculty_grading":
        from pages.faculty import grading
        grading.show()
    elif page_key == "faculty_timetable":
        from pages.faculty import timetable
        timetable.show()
    
    # Admin pages
    elif page_key == "students":
        from pages import students
        students.show()
    elif page_key == "admissions":
        from pages import admissions
        admissions.show()
    elif page_key == "academics":
        from pages import academics
        academics.show()
    elif page_key == "hr":
        from pages import hr
        hr.show()
    elif page_key == "library":
        from pages import library
        library.show()
    elif page_key == "finance":
        from pages import finance
        finance.show()
    elif page_key == "reports":
        from pages import reports
        reports.show()
    elif page_key == "settings":
        from pages import settings
        settings.show()
    
    else:
        st.error(f"Page '{page_key}' not found")


def main():
    """Main application entry point"""
    # Check authentication
    if not st.session_state.get("authenticated", False):
        show_login_page()
    else:
        show_dashboard()


if __name__ == "__main__":
    main()
