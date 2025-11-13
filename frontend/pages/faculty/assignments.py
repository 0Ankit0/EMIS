"""
Faculty Assignments Management Page
"""
import streamlit as st
import pandas as pd
from datetime import datetime, date
from utils.api_client import api_client
from utils.helpers import show_error, show_success, show_info
from services.faculty_service import faculty_service


def show():
    """Display faculty assignments page"""
    st.title("📝 Assignments Management")
    st.markdown("### Create and manage course assignments")
    
    tab1, tab2, tab3 = st.tabs(["📋 My Assignments", "➕ Create Assignment", "📊 Submissions"])
    
    with tab1:
        show_assignments_list()
    
    with tab2:
        show_create_assignment()
    
    with tab3:
        show_submissions()


def show_assignments_list():
    """Show list of assignments"""
    st.subheader("All Assignments")
    
    try:
        faculty_id = st.session_state.user.get("id")
        courses = faculty_service.get_courses(faculty_id)
        
        if courses:
            course_options = {f"{c['name']} ({c['code']})": c['id'] for c in courses}
            selected_course = st.selectbox("Select Course", list(course_options.keys()))
            course_id = course_options[selected_course]
            
            assignments = faculty_service.get_assignments(course_id)
            
            if assignments:
                for assignment in assignments:
                    with st.expander(f"📄 {assignment.get('title', 'Assignment')}", expanded=False):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.write(f"**Due Date:** {assignment.get('due_date', 'N/A')}")
                            st.write(f"**Max Marks:** {assignment.get('max_marks', 0)}")
                        
                        with col2:
                            submissions = assignment.get('submissions_count', 0)
                            total_students = assignment.get('total_students', 0)
                            st.metric("Submissions", f"{submissions}/{total_students}")
                        
                        with col3:
                            graded = assignment.get('graded_count', 0)
                            st.metric("Graded", f"{graded}/{submissions}")
                        
                        st.write(f"**Description:** {assignment.get('description', 'No description')}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("View Submissions", key=f"view_{assignment.get('id')}"):
                                st.session_state.selected_assignment = assignment.get('id')
                                st.rerun()
                        with col2:
                            if st.button("Delete", key=f"delete_{assignment.get('id')}"):
                                delete_assignment(assignment.get('id'))
            else:
                show_info("No assignments created for this course")
        else:
            show_info("You are not teaching any courses")
    
    except Exception as e:
        show_error(f"Error loading assignments: {str(e)}")


def show_create_assignment():
    """Show create assignment form"""
    st.subheader("Create New Assignment")
    
    try:
        faculty_id = st.session_state.user.get("id")
        courses = faculty_service.get_courses(faculty_id)
        
        if courses:
            with st.form("create_assignment_form"):
                course_options = {f"{c['name']} ({c['code']})": c['id'] for c in courses}
                selected_course = st.selectbox("Select Course *", list(course_options.keys()))
                course_id = course_options[selected_course]
                
                title = st.text_input("Assignment Title *", placeholder="e.g., Assignment 1 - Data Structures")
                description = st.text_area("Description *", placeholder="Describe the assignment requirements...")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    due_date = st.date_input("Due Date *", min_value=date.today())
                    max_marks = st.number_input("Maximum Marks *", min_value=1, max_value=100, value=20)
                
                with col2:
                    assignment_type = st.selectbox("Type", ["Individual", "Group", "Project", "Lab"])
                    attachments = st.file_uploader("Attach Files (optional)", type=['pdf', 'doc', 'docx'], accept_multiple_files=True)
                
                instructions = st.text_area("Instructions", placeholder="Additional instructions for students...")
                
                submitted = st.form_submit_button("Create Assignment", type="primary")
                
                if submitted:
                    if not title or not description:
                        show_error("Please fill all required fields")
                    else:
                        create_assignment({
                            "course_id": course_id,
                            "title": title,
                            "description": description,
                            "due_date": str(due_date),
                            "max_marks": max_marks,
                            "assignment_type": assignment_type,
                            "instructions": instructions
                        }, attachments)
        else:
            show_info("You are not teaching any courses")
    
    except Exception as e:
        show_error(f"Error: {str(e)}")


def show_submissions():
    """Show assignment submissions"""
    st.subheader("Assignment Submissions")
    
    selected_assignment_id = st.session_state.get('selected_assignment')
    
    if selected_assignment_id:
        try:
            submissions = faculty_service.get_submissions(selected_assignment_id)
            
            if submissions:
                # Filter options
                col1, col2 = st.columns(2)
                with col1:
                    status_filter = st.selectbox("Filter by Status", ["All", "Submitted", "Graded", "Pending"])
                with col2:
                    sort_by = st.selectbox("Sort by", ["Name", "Submission Date", "Marks"])
                
                # Apply filters
                filtered = submissions
                if status_filter != "All":
                    filtered = [s for s in submissions if s.get('status', '').lower() == status_filter.lower()]
                
                st.divider()
                
                for submission in filtered:
                    with st.container():
                        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                        
                        with col1:
                            st.write(f"**{submission.get('student_name', 'Student')}**")
                            st.caption(f"Roll No: {submission.get('roll_no', 'N/A')}")
                        
                        with col2:
                            st.write(f"**Submitted:** {submission.get('submitted_date', 'N/A')}")
                        
                        with col3:
                            marks = submission.get('marks_obtained')
                            if marks is not None:
                                st.success(f"✅ Graded: {marks}")
                            else:
                                st.warning("⏳ Pending")
                        
                        with col4:
                            if st.button("Grade", key=f"grade_{submission.get('id')}"):
                                grade_submission(submission)
                        
                        st.divider()
            else:
                show_info("No submissions yet")
        
        except Exception as e:
            show_error(f"Error loading submissions: {str(e)}")
    else:
        st.info("Select an assignment from 'My Assignments' tab to view submissions")


def create_assignment(data, attachments=None):
    """Create new assignment"""
    try:
        response = faculty_service.create_assignment(data)
        show_success("Assignment created successfully!")
        st.balloons()
        st.rerun()
    except Exception as e:
        show_error(f"Error creating assignment: {str(e)}")


def grade_submission(submission):
    """Grade a submission"""
    with st.form(f"grade_form_{submission.get('id')}"):
        st.write(f"**Grading submission for:** {submission.get('student_name')}")
        
        max_marks = submission.get('max_marks', 100)
        marks = st.number_input(
            "Marks Obtained",
            min_value=0.0,
            max_value=float(max_marks),
            value=float(submission.get('marks_obtained', 0))
        )
        
        feedback = st.text_area(
            "Feedback",
            value=submission.get('feedback', ''),
            placeholder="Provide feedback to the student..."
        )
        
        if st.form_submit_button("Save Grade"):
            try:
                faculty_service.grade_submission(submission.get('id'), marks, feedback)
                show_success("Grade saved successfully!")
                st.rerun()
            except Exception as e:
                show_error(f"Error saving grade: {str(e)}")


def delete_assignment(assignment_id):
    """Delete an assignment"""
    try:
        api_client.delete(f"/api/assignments/{assignment_id}")
        show_success("Assignment deleted successfully!")
        st.rerun()
    except Exception as e:
        show_error(f"Error deleting assignment: {str(e)}")
