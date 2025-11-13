"""
Faculty Exams Page
"""
import streamlit as st
from utils.api_client import api_client
from utils.helpers import show_error, show_success, show_info
from services.faculty_service import faculty_service


def show():
    """Display faculty exams page"""
    st.title("📋 Exams Management")
    
    tab1, tab2 = st.tabs(["Scheduled Exams", "Create Exam"])
    
    with tab1:
        show_exams_list()
    
    with tab2:
        show_create_exam()


def show_exams_list():
    """Show list of exams"""
    try:
        faculty_id = st.session_state.user.get("id")
        courses = faculty_service.get_courses(faculty_id)
        
        if courses:
            course_options = {f"{c['name']} ({c['code']})": c['id'] for c in courses}
            selected_course = st.selectbox("Select Course", list(course_options.keys()))
            course_id = course_options[selected_course]
            
            response = api_client.get(f"/api/courses/{course_id}/exams")
            exams = response.get("items", [])
            
            if exams:
                for exam in exams:
                    with st.expander(f"📝 {exam.get('name')} - {exam.get('exam_type')}"):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.write(f"**Date:** {exam.get('date')}")
                            st.write(f"**Max Marks:** {exam.get('max_marks')}")
                        with col2:
                            st.write(f"**Duration:** {exam.get('duration')} mins")
                            st.write(f"**Room:** {exam.get('room')}")
                        with col3:
                            if st.button("Enter Marks", key=f"marks_{exam.get('id')}"):
                                st.session_state.selected_exam = exam.get('id')
                                st.session_state.page = "faculty_grading"
                                st.rerun()
            else:
                show_info("No exams scheduled")
        else:
            show_info("You are not teaching any courses")
    
    except Exception as e:
        show_error(f"Error: {str(e)}")


def show_create_exam():
    """Create new exam"""
    try:
        faculty_id = st.session_state.user.get("id")
        courses = faculty_service.get_courses(faculty_id)
        
        if courses:
            with st.form("create_exam_form"):
                course_options = {f"{c['name']} ({c['code']})": c['id'] for c in courses}
                selected_course = st.selectbox("Select Course *", list(course_options.keys()))
                course_id = course_options[selected_course]
                
                col1, col2 = st.columns(2)
                with col1:
                    exam_name = st.text_input("Exam Name *", placeholder="e.g., Mid Term Exam")
                    exam_type = st.selectbox("Exam Type *", ["Mid Term", "End Term", "Quiz", "Practical"])
                    exam_date = st.date_input("Exam Date *")
                
                with col2:
                    max_marks = st.number_input("Maximum Marks *", min_value=1, max_value=100, value=100)
                    duration = st.number_input("Duration (minutes) *", min_value=30, max_value=180, value=120)
                    room = st.text_input("Room/Hall")
                
                instructions = st.text_area("Instructions for students")
                
                submitted = st.form_submit_button("Create Exam", type="primary")
                
                if submitted:
                    create_exam({
                        "course_id": course_id,
                        "name": exam_name,
                        "exam_type": exam_type.lower().replace(" ", "_"),
                        "date": str(exam_date),
                        "max_marks": max_marks,
                        "duration": duration,
                        "room": room,
                        "instructions": instructions
                    })
        else:
            show_info("You are not teaching any courses")
    
    except Exception as e:
        show_error(f"Error: {str(e)}")


def create_exam(data):
    """Create new exam"""
    try:
        api_client.post("/api/exams", data)
        show_success("Exam created successfully!")
        st.balloons()
        st.rerun()
    except Exception as e:
        show_error(f"Error creating exam: {str(e)}")
