"""
Faculty Leave History Page
"""
import streamlit as st
import pandas as pd
from utils.api_client import api_client
from utils.helpers import show_error, show_info


def show():
    """Display leave history page"""
    st.title("📋 Leave History")
    
    try:
        faculty_id = st.session_state.user.get("id")
        response = api_client.get(f"/api/faculty/{faculty_id}/leave/history")
        leaves = response.get("items", [])
        
        if leaves:
            # Filter options
            col1, col2 = st.columns(2)
            with col1:
                status_filter = st.selectbox("Filter by Status", ["All", "Pending", "Approved", "Rejected"])
            with col2:
                sort_by = st.selectbox("Sort by", ["Recent First", "Oldest First"])
            
            # Display leaves
            for leave in leaves:
                status_color = {
                    "approved": "🟢",
                    "pending": "🟡",
                    "rejected": "🔴"
                }.get(leave.get("status", "").lower(), "⚪")
                
                with st.expander(f"{status_color} {leave.get('leave_type')} - {leave.get('from_date')} to {leave.get('to_date')}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Applied On:** {leave.get('applied_date')}")
                        st.write(f"**Status:** {leave.get('status')}")
                    with col2:
                        st.write(f"**Days:** {leave.get('days')}")
                        if leave.get('approver'):
                            st.write(f"**Approved By:** {leave.get('approver')}")
                    
                    st.write(f"**Reason:** {leave.get('reason')}")
                    if leave.get('remarks'):
                        st.info(f"**Remarks:** {leave.get('remarks')}")
        else:
            show_info("No leave applications found")
    
    except Exception as e:
        show_error(f"Error: {str(e)}")
