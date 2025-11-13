"""
Admissions Applications List Page
"""
import streamlit as st
import pandas as pd
from utils.api_client import api_client
from utils.helpers import show_error, show_success, show_info


def show():
    """Display applications list page"""
    st.title("📝 Admission Applications")
    st.markdown("### Manage student applications")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.selectbox(
            "Status",
            ["All", "Pending", "Under Review", "Approved", "Rejected"]
        )
    
    with col2:
        program_filter = st.selectbox(
            "Program",
            ["All", "B.Tech", "M.Tech", "MBA", "MCA"]
        )
    
    with col3:
        search = st.text_input("Search", placeholder="Name, Email, Phone...")
    
    st.divider()
    
    try:
        # Fetch applications
        params = {}
        if status_filter != "All":
            params["status"] = status_filter.lower().replace(" ", "_")
        if program_filter != "All":
            params["program"] = program_filter
        if search:
            params["search"] = search
        
        response = api_client.get("/api/admissions/applications", params=params)
        applications = response.get("items", [])
        total = response.get("total", 0)
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Applications", total)
        with col2:
            pending = len([a for a in applications if a.get('status') == 'pending'])
            st.metric("Pending", pending)
        with col3:
            approved = len([a for a in applications if a.get('status') == 'approved'])
            st.metric("Approved", approved)
        with col4:
            rejected = len([a for a in applications if a.get('status') == 'rejected'])
            st.metric("Rejected", rejected)
        
        st.divider()
        
        if applications:
            for app in applications:
                with st.expander(
                    f"{'🟢' if app.get('status') == 'approved' else '🟡' if app.get('status') == 'pending' else '🔴'} "
                    f"{app.get('name', 'N/A')} - {app.get('application_no', 'N/A')}"
                ):
                    col1, col2, col3 = st.columns([2, 2, 1])
                    
                    with col1:
                        st.write(f"**Name:** {app.get('name')}")
                        st.write(f"**Email:** {app.get('email')}")
                        st.write(f"**Phone:** {app.get('phone')}")
                    
                    with col2:
                        st.write(f"**Program:** {app.get('program')}")
                        st.write(f"**Applied Date:** {app.get('applied_date', 'N/A')}")
                        st.write(f"**Status:** {app.get('status', 'N/A').title()}")
                    
                    with col3:
                        if st.button("View Details", key=f"view_{app.get('id')}"):
                            st.session_state.selected_application = app.get('id')
                            st.session_state.page = "admin_application_details"
                            st.rerun()
                        
                        if app.get('status') == 'pending':
                            if st.button("Approve", key=f"approve_{app.get('id')}", type="primary"):
                                approve_application(app.get('id'))
                            if st.button("Reject", key=f"reject_{app.get('id')}"):
                                reject_application(app.get('id'))
        else:
            show_info("No applications found")
    
    except Exception as e:
        show_error(f"Error loading applications: {str(e)}")


def approve_application(app_id):
    """Approve an application"""
    try:
        api_client.post(f"/api/admissions/applications/{app_id}/approve")
        show_success("Application approved successfully!")
        st.rerun()
    except Exception as e:
        show_error(f"Error approving application: {str(e)}")


def reject_application(app_id):
    """Reject an application"""
    try:
        reason = st.text_area("Rejection Reason", key=f"reason_{app_id}")
        if reason:
            api_client.post(f"/api/admissions/applications/{app_id}/reject", {
                "reason": reason
            })
            show_success("Application rejected")
            st.rerun()
        else:
            show_error("Please provide a rejection reason")
    except Exception as e:
        show_error(f"Error rejecting application: {str(e)}")
