"""
Student Attendance Page
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from utils.api_client import api_client
from utils.helpers import show_error, show_info
from components.ui_components import render_data_table, render_line_chart


def show():
    """Display student attendance page"""
    st.title("📅 Attendance")
    st.markdown("### Track your attendance across all courses")
    
    try:
        student_id = st.session_state.user.get("id")
        
        # Overall attendance summary
        st.subheader("📊 Overall Attendance")
        response = api_client.get(f"/api/students/{student_id}/attendance/summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_classes = response.get("total_classes", 0)
            st.metric("Total Classes", total_classes)
        
        with col2:
            attended = response.get("attended", 0)
            st.metric("Attended", attended, delta=f"+{attended}")
        
        with col3:
            absent = response.get("absent", 0)
            st.metric("Absent", absent, delta=f"-{absent}", delta_color="inverse")
        
        with col4:
            percentage = response.get("percentage", 0)
            if percentage >= 75:
                st.metric("Attendance %", f"{percentage}%", delta="Good")
            else:
                st.metric("Attendance %", f"{percentage}%", delta="Low", delta_color="inverse")
        
        # Course-wise attendance
        st.divider()
        st.subheader("📚 Course-wise Attendance")
        
        courses_attendance = response.get("courses", [])
        if courses_attendance:
            for course in courses_attendance:
                with st.container():
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"**{course.get('course_name', 'Course')}** ({course.get('course_code', '')})")
                        
                        # Progress bar
                        percentage = course.get('percentage', 0)
                        progress_color = "🟢" if percentage >= 75 else "🔴"
                        st.progress(percentage / 100)
                        st.caption(f"{progress_color} {course.get('attended', 0)}/{course.get('total', 0)} classes - {percentage}%")
                    
                    with col2:
                        st.metric("Attendance", f"{percentage}%")
                    
                    st.divider()
        else:
            show_info("No attendance records found")
        
        # Attendance trends
        st.divider()
        st.subheader("📈 Attendance Trend")
        
        trend_data = response.get("trend", [])
        if trend_data:
            df = pd.DataFrame(trend_data)
            render_line_chart(df, "date", "percentage", "Attendance Over Time")
        else:
            show_info("No trend data available")
        
        # Leave application
        st.divider()
        st.subheader("📝 Apply for Leave")
        
        with st.form("leave_form"):
            leave_date = st.date_input("Leave Date", min_value=datetime.now().date())
            reason = st.text_area("Reason for Leave", placeholder="Enter reason...")
            
            if st.form_submit_button("Submit Leave Application"):
                apply_leave(leave_date, reason)
    
    except Exception as e:
        show_error(f"Error loading attendance: {str(e)}")
        show_demo_attendance()


def apply_leave(leave_date, reason):
    """Apply for leave"""
    try:
        student_id = st.session_state.user.get("id")
        data = {
            "student_id": student_id,
            "leave_date": str(leave_date),
            "reason": reason
        }
        response = api_client.post("/api/students/leave", data)
        st.success("Leave application submitted successfully!")
    except Exception as e:
        show_error(f"Error submitting leave: {str(e)}")


def show_demo_attendance():
    """Show demo attendance data"""
    st.info("Showing demo data...")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Classes", 45)
    with col2:
        st.metric("Attended", 38, delta="+38")
    with col3:
        st.metric("Absent", 7, delta="-7", delta_color="inverse")
    with col4:
        st.metric("Attendance %", "84%", delta="Good")
    
    st.divider()
    st.subheader("📚 Course-wise Attendance")
    
    demo_courses = [
        {"course_name": "Data Structures", "course_code": "CS201", "attended": 15, "total": 18, "percentage": 83},
        {"course_name": "Database Systems", "course_code": "CS202", "attended": 12, "total": 14, "percentage": 86},
        {"course_name": "Web Development", "course_code": "CS203", "attended": 11, "total": 13, "percentage": 85},
    ]
    
    for course in demo_courses:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write(f"**{course['course_name']}** ({course['course_code']})")
            percentage = course['percentage']
            progress_color = "🟢" if percentage >= 75 else "🔴"
            st.progress(percentage / 100)
            st.caption(f"{progress_color} {course['attended']}/{course['total']} classes - {percentage}%")
        
        with col2:
            st.metric("Attendance", f"{percentage}%")
        
        st.divider()
