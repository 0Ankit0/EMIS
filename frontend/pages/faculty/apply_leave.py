"""
Faculty Leave Application Page
"""
import streamlit as st
from datetime import date
from utils.helpers import show_error, show_success
from services.faculty_service import faculty_service


def show():
    """Display leave application page"""
    st.title("📝 Apply for Leave")
    
    with st.form("leave_application_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            leave_type = st.selectbox("Leave Type *", ["Casual Leave", "Sick Leave", "Earned Leave", "Maternity Leave"])
            from_date = st.date_input("From Date *", min_value=date.today())
        
        with col2:
            half_day = st.checkbox("Half Day")
            to_date = st.date_input("To Date *", min_value=from_date)
        
        reason = st.text_area("Reason for Leave *", placeholder="Please provide reason for leave...")
        
        attachment = st.file_uploader("Attach Document (if any)", type=['pdf', 'jpg', 'png'])
        
        submitted = st.form_submit_button("Submit Application", type="primary")
        
        if submitted:
            if not reason:
                show_error("Please provide reason for leave")
            else:
                apply_leave({
                    "leave_type": leave_type,
                    "from_date": str(from_date),
                    "to_date": str(to_date),
                    "half_day": half_day,
                    "reason": reason
                })


def apply_leave(data):
    """Submit leave application"""
    try:
        faculty_id = st.session_state.user.get("id")
        faculty_service.apply_leave(
            faculty_id,
            data["from_date"],
            data["to_date"],
            data["reason"]
        )
        show_success("Leave application submitted successfully!")
        st.balloons()
    except Exception as e:
        show_error(f"Error: {str(e)}")
