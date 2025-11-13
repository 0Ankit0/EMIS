"""
Faculty Attendance Management Page
"""
import streamlit as st
import pandas as pd
from datetime import datetime, date
from utils.api_client import api_client
from utils.helpers import show_error, show_success, show_info


def show():
    """Display faculty attendance page"""
    st.title("📅 Mark Attendance")
    st.markdown("### Mark and manage student attendance")
    
    tab1, tab2, tab3 = st.tabs(["✍️ Mark Attendance", "📊 Attendance Reports", "📈 Analytics"])
    
    with tab1:
        show_mark_attendance()
    
    with tab2:
        show_attendance_reports()
    
    with tab3:
        show_attendance_analytics()


def show_mark_attendance():
    """Show attendance marking interface"""
    st.subheader("Mark Attendance")
    
    try:
        faculty_id = st.session_state.user.get("id")
        
        # Select course
        courses_response = api_client.get(f"/api/faculty/{faculty_id}/courses")
        courses = courses_response.get("items", [])
        
        if courses:
            course_options = {f"{c['name']} ({c['code']})": c['id'] for c in courses}
            selected_course_name = st.selectbox("Select Course", list(course_options.keys()))
            selected_course_id = course_options[selected_course_name]
            
            # Select date
            attendance_date = st.date_input("Attendance Date", value=date.today(), max_value=date.today())
            
            # Get students
            students_response = api_client.get(f"/api/courses/{selected_course_id}/students")
            students = students_response.get("items", [])
            
            if students:
                st.divider()
                st.subheader(f"Mark Attendance - {attendance_date}")
                
                # Quick actions
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Mark All Present"):
                        st.session_state.attendance_marks = {s['id']: True for s in students}
                        st.rerun()
                with col2:
                    if st.button("❌ Mark All Absent"):
                        st.session_state.attendance_marks = {s['id']: False for s in students}
                        st.rerun()
                
                st.divider()
                
                # Initialize attendance marks in session state
                if 'attendance_marks' not in st.session_state:
                    st.session_state.attendance_marks = {}
                
                # Student attendance checkboxes
                attendance_data = []
                
                for student in students:
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.write(f"**{student.get('name', 'Student')}**")
                        st.caption(f"Roll No: {student.get('roll_no', 'N/A')}")
                    
                    with col2:
                        is_present = st.checkbox(
                            "Present",
                            value=st.session_state.attendance_marks.get(student['id'], True),
                            key=f"present_{student['id']}"
                        )
                        attendance_data.append({
                            "student_id": student['id'],
                            "is_present": is_present
                        })
                    
                    with col3:
                        if not is_present:
                            st.warning("❌ Absent")
                        else:
                            st.success("✅ Present")
                
                st.divider()
                
                if st.button("💾 Save Attendance", type="primary", use_container_width=True):
                    save_attendance(selected_course_id, attendance_date, attendance_data)
            else:
                show_info("No students enrolled in this course")
        else:
            show_info("You are not assigned to any courses")
    
    except Exception as e:
        show_error(f"Error loading attendance page: {str(e)}")


def show_attendance_reports():
    """Show attendance reports"""
    st.subheader("Attendance Reports")
    
    try:
        faculty_id = st.session_state.user.get("id")
        courses_response = api_client.get(f"/api/faculty/{faculty_id}/courses")
        courses = courses_response.get("items", [])
        
        if courses:
            course_options = {f"{c['name']} ({c['code']})": c['id'] for c in courses}
            selected_course_name = st.selectbox("Select Course", list(course_options.keys()), key="report_course")
            selected_course_id = course_options[selected_course_name]
            
            col1, col2 = st.columns(2)
            with col1:
                from_date = st.date_input("From Date")
            with col2:
                to_date = st.date_input("To Date", value=date.today())
            
            if st.button("📊 Generate Report"):
                response = api_client.get(
                    f"/api/courses/{selected_course_id}/attendance/report",
                    params={"from_date": str(from_date), "to_date": str(to_date)}
                )
                
                report_data = response.get("items", [])
                
                if report_data:
                    df = pd.DataFrame(report_data)
                    
                    st.divider()
                    st.write(f"**Attendance Report: {from_date} to {to_date}**")
                    
                    # Display summary
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Classes", len(report_data))
                    with col2:
                        avg_attendance = df['attendance_percentage'].mean() if 'attendance_percentage' in df.columns else 0
                        st.metric("Avg Attendance", f"{avg_attendance:.1f}%")
                    with col3:
                        st.metric("Total Students", df['student_id'].nunique() if 'student_id' in df.columns else 0)
                    
                    st.divider()
                    st.dataframe(df, use_container_width=True)
                    
                    # Download option
                    csv = df.to_csv(index=False)
                    st.download_button(
                        "📥 Download Report (CSV)",
                        csv,
                        f"attendance_report_{from_date}_{to_date}.csv",
                        "text/csv"
                    )
                else:
                    show_info("No attendance data for selected period")
    
    except Exception as e:
        show_error(f"Error generating report: {str(e)}")


def show_attendance_analytics():
    """Show attendance analytics"""
    st.subheader("Attendance Analytics")
    
    try:
        faculty_id = st.session_state.user.get("id")
        response = api_client.get(f"/api/faculty/{faculty_id}/attendance/analytics")
        
        analytics = response.get("data", {})
        
        # Overall statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Classes", analytics.get("total_classes", 0))
        with col2:
            st.metric("Avg Attendance", f"{analytics.get('avg_attendance', 0)}%")
        with col3:
            st.metric("Students Below 75%", analytics.get("low_attendance_students", 0))
        with col4:
            st.metric("Perfect Attendance", analytics.get("perfect_attendance_students", 0))
        
        # Low attendance students
        st.divider()
        st.subheader("⚠️ Students with Low Attendance")
        
        low_attendance = analytics.get("low_attendance_list", [])
        if low_attendance:
            df = pd.DataFrame(low_attendance)
            st.dataframe(df, use_container_width=True)
        else:
            st.success("No students with low attendance!")
    
    except Exception as e:
        show_error(f"Error loading analytics: {str(e)}")


def save_attendance(course_id, attendance_date, attendance_data):
    """Save attendance data"""
    try:
        data = {
            "course_id": course_id,
            "date": str(attendance_date),
            "attendance": attendance_data
        }
        response = api_client.post("/api/attendance/mark", data)
        show_success(f"Attendance saved successfully for {len(attendance_data)} students!")
        st.session_state.attendance_marks = {}
        st.balloons()
    except Exception as e:
        show_error(f"Error saving attendance: {str(e)}")
