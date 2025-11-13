"""
Faculty Courses Page
"""
import streamlit as st
import pandas as pd
from utils.api_client import api_client
from utils.helpers import show_error, show_success, show_info
from components.ui_components import render_data_table


def show():
    """Display faculty courses page"""
    st.title("📚 My Courses")
    st.markdown("### Courses you are teaching")
    
    try:
        # Fetch teaching courses
        with st.spinner("Loading your courses..."):
            faculty_id = st.session_state.user.get("id")
            response = api_client.get(f"/api/faculty/{faculty_id}/courses")
            courses = response.get("items", [])
        
        if courses:
            for course in courses:
                with st.expander(f"📖 {course.get('name', 'Course')} - {course.get('code', '')}", expanded=True):
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Students Enrolled", course.get('enrolled_students', 0))
                    
                    with col2:
                        st.metric("Classes Conducted", course.get('classes_conducted', 0))
                    
                    with col3:
                        avg_attendance = course.get('avg_attendance', 0)
                        st.metric("Avg Attendance", f"{avg_attendance}%")
                    
                    with col4:
                        st.metric("Credits", course.get('credits', 0))
                    
                    st.divider()
                    
                    # Course actions
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        if st.button("👥 View Students", key=f"students_{course.get('id')}", use_container_width=True):
                            show_course_students(course.get('id'))
                    
                    with col2:
                        if st.button("📝 Assignments", key=f"assignments_{course.get('id')}", use_container_width=True):
                            st.session_state.selected_course = course.get('id')
                            st.session_state.page = "faculty_assignments"
                    
                    with col3:
                        if st.button("📅 Attendance", key=f"attendance_{course.get('id')}", use_container_width=True):
                            st.session_state.selected_course = course.get('id')
                            st.session_state.page = "faculty_attendance"
                    
                    with col4:
                        if st.button("📎 Materials", key=f"materials_{course.get('id')}", use_container_width=True):
                            upload_course_material(course.get('id'))
        else:
            show_info("You are not assigned to any courses")
    
    except Exception as e:
        show_error(f"Error loading courses: {str(e)}")
        show_demo_courses()


def show_course_students(course_id):
    """Show students enrolled in course"""
    try:
        response = api_client.get(f"/api/courses/{course_id}/students")
        students = response.get("items", [])
        
        if students:
            with st.expander("👥 Enrolled Students", expanded=True):
                df = pd.DataFrame(students)
                display_columns = ["roll_no", "name", "email", "attendance_percentage"]
                available_columns = [col for col in display_columns if col in df.columns]
                render_data_table(df[available_columns], f"Students ({len(students)})")
        else:
            show_info("No students enrolled")
    except Exception as e:
        show_error(f"Error loading students: {str(e)}")


def upload_course_material(course_id):
    """Upload course material"""
    with st.expander("📎 Upload Course Material", expanded=True):
        title = st.text_input("Material Title")
        description = st.text_area("Description")
        file = st.file_uploader("Select File", type=['pdf', 'ppt', 'pptx', 'doc', 'docx'])
        
        if st.button("📤 Upload"):
            if not title or not file:
                show_error("Please provide title and file")
            else:
                try:
                    files = {'file': file.getvalue()}
                    data = {
                        "course_id": course_id,
                        "title": title,
                        "description": description
                    }
                    response = api_client.post("/api/courses/materials", data=data, files=files)
                    show_success("Material uploaded successfully!")
                except Exception as e:
                    show_error(f"Error uploading material: {str(e)}")


def show_demo_courses():
    """Show demo course data"""
    st.info("Showing demo data...")
    
    demo_courses = [
        {
            "id": 1,
            "name": "Data Structures",
            "code": "CS201",
            "enrolled_students": 45,
            "classes_conducted": 18,
            "avg_attendance": 85,
            "credits": 4
        }
    ]
    
    for course in demo_courses:
        with st.expander(f"📖 {course['name']} - {course['code']}", expanded=True):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Students Enrolled", course['enrolled_students'])
            with col2:
                st.metric("Classes Conducted", course['classes_conducted'])
            with col3:
                st.metric("Avg Attendance", f"{course['avg_attendance']}%")
            with col4:
                st.metric("Credits", course['credits'])
