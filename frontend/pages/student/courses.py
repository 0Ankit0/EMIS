"""
Student Courses Page
"""
import streamlit as st
import pandas as pd
from utils.api_client import api_client
from utils.helpers import show_error, show_info
from components.ui_components import render_data_table


def show():
    """Display student courses page"""
    st.title("📚 My Courses")
    st.markdown("### View your enrolled courses and course materials")
    
    try:
        # Fetch enrolled courses
        with st.spinner("Loading your courses..."):
            student_id = st.session_state.user.get("id")
            response = api_client.get(f"/api/students/{student_id}/courses")
            courses = response.get("items", [])
        
        if courses:
            # Display courses in cards
            for course in courses:
                with st.expander(f"📖 {course.get('name', 'Course')} - {course.get('code', '')}", expanded=True):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**Instructor:** {course.get('instructor_name', 'N/A')}")
                        st.write(f"**Credits:** {course.get('credits', 0)}")
                    
                    with col2:
                        st.write(f"**Schedule:** {course.get('schedule', 'N/A')}")
                        st.write(f"**Room:** {course.get('room', 'N/A')}")
                    
                    with col3:
                        attendance = course.get('attendance_percentage', 0)
                        st.metric("Attendance", f"{attendance}%")
                        
                        if attendance < 75:
                            st.warning("⚠️ Low attendance!")
                    
                    # Course materials
                    st.divider()
                    st.subheader("📎 Course Materials")
                    
                    materials = course.get('materials', [])
                    if materials:
                        for material in materials:
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.write(f"📄 {material.get('title', 'Document')}")
                            with col2:
                                st.button("📥 Download", key=f"download_{material.get('id')}")
                    else:
                        st.info("No materials uploaded yet")
        else:
            show_info("You are not enrolled in any courses yet")
    
    except Exception as e:
        show_error(f"Error loading courses: {str(e)}")
        # Show demo data
        st.info("Showing demo data...")
        show_demo_courses()


def show_demo_courses():
    """Show demo course data"""
    demo_courses = [
        {
            "name": "Data Structures",
            "code": "CS201",
            "instructor_name": "Dr. Smith",
            "credits": 4,
            "schedule": "Mon, Wed 10:00-11:30",
            "room": "Room 301",
            "attendance_percentage": 85
        },
        {
            "name": "Database Systems",
            "code": "CS202",
            "instructor_name": "Dr. Johnson",
            "credits": 3,
            "schedule": "Tue, Thu 14:00-15:30",
            "room": "Room 205",
            "attendance_percentage": 72
        }
    ]
    
    for course in demo_courses:
        with st.expander(f"📖 {course['name']} - {course['code']}", expanded=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**Instructor:** {course['instructor_name']}")
                st.write(f"**Credits:** {course['credits']}")
            
            with col2:
                st.write(f"**Schedule:** {course['schedule']}")
                st.write(f"**Room:** {course['room']}")
            
            with col3:
                st.metric("Attendance", f"{course['attendance_percentage']}%")
                if course['attendance_percentage'] < 75:
                    st.warning("⚠️ Low attendance!")
