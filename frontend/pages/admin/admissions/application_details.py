"""
Admission Application Details Page
"""
import streamlit as st
from utils.api_client import api_client
from utils.helpers import show_error, show_success


def show():
    """Display application details"""
    app_id = st.session_state.get('selected_application')
    
    if not app_id:
        st.warning("No application selected")
        if st.button("← Back to Applications"):
            st.session_state.page = "admin_applications"
            st.rerun()
        return
    
    try:
        response = api_client.get(f"/api/admissions/applications/{app_id}")
        app = response.get("application", {})
        
        st.title(f"Application Details - {app.get('application_no')}")
        
        # Action buttons
        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            if st.button("← Back"):
                st.session_state.page = "admin_applications"
                st.rerun()
        with col2:
            if app.get('status') == 'pending':
                if st.button("✓ Approve", type="primary"):
                    approve_application(app_id)
        
        st.divider()
        
        # Personal Information
        st.subheader("📋 Personal Information")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Full Name:** {app.get('name')}")
            st.write(f"**Email:** {app.get('email')}")
            st.write(f"**Phone:** {app.get('phone')}")
            st.write(f"**Date of Birth:** {app.get('dob', 'N/A')}")
        with col2:
            st.write(f"**Gender:** {app.get('gender', 'N/A')}")
            st.write(f"**Father's Name:** {app.get('father_name', 'N/A')}")
            st.write(f"**Mother's Name:** {app.get('mother_name', 'N/A')}")
            st.write(f"**Category:** {app.get('category', 'N/A')}")
        
        st.divider()
        
        # Academic Information
        st.subheader("🎓 Academic Information")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Program Applied:** {app.get('program')}")
            st.write(f"**10th Percentage:** {app.get('tenth_percentage', 'N/A')}%")
            st.write(f"**12th Percentage:** {app.get('twelfth_percentage', 'N/A')}%")
        with col2:
            if app.get('entrance_exam'):
                st.write(f"**Entrance Exam:** {app.get('entrance_exam')}")
                st.write(f"**Exam Score:** {app.get('exam_score', 'N/A')}")
        
        st.divider()
        
        # Documents
        st.subheader("📄 Documents")
        documents = app.get('documents', [])
        if documents:
            for doc in documents:
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.write(f"📎 {doc.get('name')}")
                with col2:
                    st.write(doc.get('status', 'Pending').title())
                with col3:
                    if st.button("View", key=f"doc_{doc.get('id')}"):
                        st.info(f"Opening: {doc.get('name')}")
        else:
            st.info("No documents uploaded")
        
        st.divider()
        
        # Status and Actions
        st.subheader("📊 Application Status")
        status = app.get('status', 'pending')
        
        if status == 'approved':
            st.success(f"✅ Application Approved on {app.get('approved_date', 'N/A')}")
        elif status == 'rejected':
            st.error(f"❌ Application Rejected")
            if app.get('rejection_reason'):
                st.write(f"**Reason:** {app.get('rejection_reason')}")
        else:
            st.warning("⏳ Application Pending Review")
            
            # Review form
            with st.form("review_form"):
                st.write("**Review Application**")
                
                action = st.radio("Decision", ["Approve", "Reject"])
                remarks = st.text_area("Remarks")
                
                if st.form_submit_button("Submit Decision", type="primary"):
                    if action == "Approve":
                        approve_application(app_id, remarks)
                    else:
                        reject_application(app_id, remarks)
    
    except Exception as e:
        show_error(f"Error loading application: {str(e)}")


def approve_application(app_id, remarks=""):
    """Approve application"""
    try:
        api_client.post(f"/api/admissions/applications/{app_id}/approve", {
            "remarks": remarks
        })
        show_success("Application approved successfully!")
        st.balloons()
        st.rerun()
    except Exception as e:
        show_error(f"Error: {str(e)}")


def reject_application(app_id, reason):
    """Reject application"""
    try:
        if not reason:
            show_error("Please provide a rejection reason")
            return
        
        api_client.post(f"/api/admissions/applications/{app_id}/reject", {
            "reason": reason
        })
        show_success("Application rejected")
        st.rerun()
    except Exception as e:
        show_error(f"Error: {str(e)}")
