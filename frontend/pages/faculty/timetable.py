"""
Faculty Timetable Page
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from utils.api_client import api_client
from utils.helpers import show_error, show_info


def show():
    """Display faculty timetable page"""
    st.title("📅 My Timetable")
    st.markdown("### View your teaching schedule")
    
    tab1, tab2 = st.tabs(["📆 Weekly View", "📋 Day View"])
    
    with tab1:
        show_weekly_timetable()
    
    with tab2:
        show_day_timetable()


def show_weekly_timetable():
    """Show weekly timetable"""
    st.subheader("Weekly Schedule")
    
    try:
        faculty_id = st.session_state.user.get("id")
        response = api_client.get(f"/api/faculty/{faculty_id}/timetable/weekly")
        
        timetable = response.get("schedule", {})
        
        if timetable:
            # Create a grid view
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
            time_slots = ["09:00-10:00", "10:00-11:00", "11:00-12:00", "12:00-13:00", 
                         "14:00-15:00", "15:00-16:00", "16:00-17:00"]
            
            # Create DataFrame for display
            schedule_data = {}
            for day in days:
                schedule_data[day] = []
                day_schedule = timetable.get(day, [])
                
                for slot in time_slots:
                    class_info = next((c for c in day_schedule if c.get('time') == slot), None)
                    if class_info:
                        schedule_data[day].append(
                            f"📚 {class_info.get('course_code')}\n"
                            f"🏫 {class_info.get('room')}"
                        )
                    else:
                        schedule_data[day].append("-")
            
            df = pd.DataFrame(schedule_data, index=time_slots)
            st.dataframe(df, use_container_width=True, height=400)
        else:
            show_info("No timetable available")
    
    except Exception as e:
        show_error(f"Error loading timetable: {str(e)}")
        show_demo_timetable()


def show_day_timetable():
    """Show day-wise detailed timetable"""
    st.subheader("Daily Schedule")
    
    selected_date = st.date_input("Select Date", value=datetime.now().date())
    
    try:
        faculty_id = st.session_state.user.get("id")
        response = api_client.get(
            f"/api/faculty/{faculty_id}/timetable/day",
            params={"date": str(selected_date)}
        )
        
        classes = response.get("classes", [])
        
        if classes:
            for cls in classes:
                with st.container():
                    col1, col2, col3, col4 = st.columns([1, 2, 1, 1])
                    
                    with col1:
                        st.markdown(f"### {cls.get('time')}")
                    
                    with col2:
                        st.write(f"**{cls.get('course_name')}**")
                        st.caption(f"Course Code: {cls.get('course_code')}")
                    
                    with col3:
                        st.write(f"**Room:** {cls.get('room')}")
                        st.write(f"**Type:** {cls.get('class_type', 'Lecture')}")
                    
                    with col4:
                        students = cls.get('enrolled_students', 0)
                        st.metric("Students", students)
                    
                    # Quick actions
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("📅 Mark Attendance", key=f"attend_{cls.get('id')}"):
                            st.session_state.selected_course = cls.get('course_id')
                            st.session_state.page = "faculty_attendance"
                            st.rerun()
                    with col2:
                        if st.button("📎 Materials", key=f"material_{cls.get('id')}"):
                            st.session_state.selected_course = cls.get('course_id')
                            st.session_state.page = "faculty_courses"
                            st.rerun()
                    
                    st.divider()
        else:
            st.info(f"No classes scheduled for {selected_date.strftime('%A, %B %d, %Y')}")
    
    except Exception as e:
        show_error(f"Error loading schedule: {str(e)}")


def show_demo_timetable():
    """Show demo timetable"""
    st.info("Showing demo data...")
    
    demo_schedule = {
        "Monday": ["Data Structures\nRoom 301", "Database Systems\nRoom 205", "-", "-", "Lab\nLab 1", "-", "-"],
        "Tuesday": ["-", "Data Structures\nRoom 301", "-", "-", "-", "Database Systems\nRoom 205", "-"],
        "Wednesday": ["Data Structures\nRoom 301", "-", "-", "-", "Database Systems\nRoom 205", "-", "-"],
        "Thursday": ["-", "Lab\nLab 1", "-", "-", "-", "Data Structures\nRoom 301", "-"],
        "Friday": ["-", "-", "Database Systems\nRoom 205", "-", "-", "-", "-"],
        "Saturday": ["-", "-", "-", "-", "-", "-", "-"]
    }
    
    time_slots = ["09:00-10:00", "10:00-11:00", "11:00-12:00", "12:00-13:00", 
                 "14:00-15:00", "15:00-16:00", "16:00-17:00"]
    
    df = pd.DataFrame(demo_schedule, index=time_slots)
    st.dataframe(df, use_container_width=True, height=400)
