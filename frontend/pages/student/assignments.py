"""
Student Assignments Page
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from utils.api_client import api_client
from utils.helpers import show_error, show_success, show_info
from components.ui_components import render_data_table


def show():
    """Display student assignments page"""
    st.title("📝 Assignments")
    st.markdown("### View and submit your assignments")
    
    tab1, tab2, tab3 = st.tabs(["📋 Pending", "✅ Submitted", "📊 Graded"])
    
    with tab1:
        show_pending_assignments()
    
    with tab2:
        show_submitted_assignments()
    
    with tab3:
        show_graded_assignments()


def show_pending_assignments():
    """Show pending assignments"""
    st.subheader("Pending Assignments")
    
    try:
        student_id = st.session_state.user.get("id")
        response = api_client.get(f"/api/students/{student_id}/assignments/pending")
        assignments = response.get("items", [])
        
        if assignments:
            for assignment in assignments:
                with st.container():
                    st.markdown(f"### 📄 {assignment.get('title', 'Assignment')}")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**Course:** {assignment.get('course_name', 'N/A')}")
                    with col2:
                        st.write(f"**Due Date:** {assignment.get('due_date', 'N/A')}")
                    with col3:
                        st.write(f"**Max Marks:** {assignment.get('max_marks', 0)}")
                    
                    st.write(f"**Description:** {assignment.get('description', 'No description')}")
                    
                    # File upload for submission
                    uploaded_file = st.file_uploader(
                        f"Upload submission for {assignment.get('title')}",
                        key=f"upload_{assignment.get('id')}",
                        type=['pdf', 'doc', 'docx', 'zip']
                    )
                    
                    if uploaded_file:
                        if st.button(f"Submit Assignment", key=f"submit_{assignment.get('id')}"):
                            submit_assignment(assignment.get('id'), uploaded_file)
                    
                    st.divider()
        else:
            show_info("No pending assignments")
    
    except Exception as e:
        show_error(f"Error loading assignments: {str(e)}")
        show_demo_pending_assignments()


def show_submitted_assignments():
    """Show submitted assignments"""
    st.subheader("Submitted Assignments")
    
    try:
        student_id = st.session_state.user.get("id")
        response = api_client.get(f"/api/students/{student_id}/assignments/submitted")
        assignments = response.get("items", [])
        
        if assignments:
            df = pd.DataFrame(assignments)
            display_columns = ["title", "course_name", "submitted_date", "status"]
            available_columns = [col for col in display_columns if col in df.columns]
            render_data_table(df[available_columns], "Submitted Assignments")
        else:
            show_info("No submitted assignments")
    
    except Exception as e:
        show_error(f"Error loading submitted assignments: {str(e)}")


def show_graded_assignments():
    """Show graded assignments"""
    st.subheader("Graded Assignments")
    
    try:
        student_id = st.session_state.user.get("id")
        response = api_client.get(f"/api/students/{student_id}/assignments/graded")
        assignments = response.get("items", [])
        
        if assignments:
            for assignment in assignments:
                with st.container():
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.write(f"**{assignment.get('title')}**")
                        st.write(f"Course: {assignment.get('course_name')}")
                    
                    with col2:
                        marks = assignment.get('marks_obtained', 0)
                        max_marks = assignment.get('max_marks', 100)
                        st.metric("Score", f"{marks}/{max_marks}")
                    
                    with col3:
                        percentage = (marks / max_marks * 100) if max_marks > 0 else 0
                        if percentage >= 90:
                            st.success(f"Grade: A+ ({percentage:.1f}%)")
                        elif percentage >= 80:
                            st.info(f"Grade: A ({percentage:.1f}%)")
                        elif percentage >= 70:
                            st.info(f"Grade: B ({percentage:.1f}%)")
                        else:
                            st.warning(f"Grade: C ({percentage:.1f}%)")
                    
                    if assignment.get('feedback'):
                        with st.expander("View Feedback"):
                            st.write(assignment.get('feedback'))
                    
                    st.divider()
        else:
            show_info("No graded assignments yet")
    
    except Exception as e:
        show_error(f"Error loading graded assignments: {str(e)}")


def submit_assignment(assignment_id: int, file):
    """Submit an assignment"""
    try:
        files = {'file': file.getvalue()}
        response = api_client.post(
            f"/api/assignments/{assignment_id}/submit",
            files=files
        )
        show_success("Assignment submitted successfully!")
        st.balloons()
        st.rerun()
    except Exception as e:
        show_error(f"Error submitting assignment: {str(e)}")


def show_demo_pending_assignments():
    """Show demo pending assignments"""
    st.info("Showing demo data...")
    demo_assignments = [
        {
            "id": 1,
            "title": "Data Structures Assignment 1",
            "course_name": "Data Structures",
            "due_date": "2024-12-15",
            "max_marks": 20,
            "description": "Implement a binary search tree with insert, delete, and search operations"
        }
    ]
    
    for assignment in demo_assignments:
        st.markdown(f"### 📄 {assignment['title']}")
        st.write(f"**Course:** {assignment['course_name']}")
        st.write(f"**Due Date:** {assignment['due_date']}")
        st.write(f"**Description:** {assignment['description']}")
        st.divider()
