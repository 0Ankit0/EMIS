"""
Dashboard Page - Main Overview
"""
import streamlit as st
import pandas as pd
from utils.api_client import api_client
from components.ui_components import render_stats_cards, render_bar_chart, render_line_chart, render_pie_chart


def show():
    """Display dashboard page based on user role"""
    user_role = st.session_state.get("user_role", "student")
    user_name = st.session_state.user.get("name", "User")
    
    st.title("📊 Dashboard")
    st.markdown(f"### Welcome back, {user_name}!")
    
    # Show role-specific dashboard
    if user_role == "student":
        show_student_dashboard()
    elif user_role == "teacher":
        show_faculty_dashboard()
    elif user_role in ["admin", "staff"]:
        show_admin_dashboard()
    else:
        show_admin_dashboard()


def show_student_dashboard():
    """Show student-specific dashboard"""
    st.subheader("📚 Student Dashboard")
    
    try:
        student_id = st.session_state.user.get("id")
        dashboard_data = api_client.get(f"/api/students/{student_id}/dashboard")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Enrolled Courses", dashboard_data.get("enrolled_courses", 0))
        with col2:
            attendance = dashboard_data.get("overall_attendance", 0)
            st.metric("Attendance", f"{attendance}%", delta="Good" if attendance >= 75 else "Low")
        with col3:
            st.metric("Pending Assignments", dashboard_data.get("pending_assignments", 0))
        with col4:
            st.metric("CGPA", dashboard_data.get("cgpa", "N/A"))
        
        # Quick links
        st.divider()
        st.subheader("⚡ Quick Access")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📚 My Courses", use_container_width=True):
                st.session_state.page = "student_courses"
                st.rerun()
        with col2:
            if st.button("📝 Assignments", use_container_width=True):
                st.session_state.page = "student_assignments"
                st.rerun()
        with col3:
            if st.button("💰 Pay Fees", use_container_width=True):
                st.session_state.page = "student_fees"
                st.rerun()
        
        # Recent activities
        st.divider()
        st.subheader("🔔 Recent Updates")
        
        activities = dashboard_data.get("recent_activities", [])
        if activities:
            for activity in activities[:5]:
                st.info(f"📌 {activity.get('message', '')}")
        else:
            st.info("No recent updates")
    
    except Exception as e:
        st.error(f"Error loading dashboard: {str(e)}")
        show_demo_student_dashboard()


def show_faculty_dashboard():
    """Show faculty-specific dashboard"""
    st.subheader("👨‍🏫 Faculty Dashboard")
    
    try:
        faculty_id = st.session_state.user.get("id")
        dashboard_data = api_client.get(f"/api/faculty/{faculty_id}/dashboard")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Courses Teaching", dashboard_data.get("courses_teaching", 0))
        with col2:
            st.metric("Total Students", dashboard_data.get("total_students", 0))
        with col3:
            st.metric("Pending Grading", dashboard_data.get("pending_grading", 0))
        with col4:
            st.metric("Classes This Week", dashboard_data.get("classes_this_week", 0))
        
        # Quick links
        st.divider()
        st.subheader("⚡ Quick Access")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📚 My Courses", use_container_width=True):
                st.session_state.page = "faculty_courses"
                st.rerun()
        with col2:
            if st.button("📅 Mark Attendance", use_container_width=True):
                st.session_state.page = "faculty_attendance"
                st.rerun()
        with col3:
            if st.button("📝 Assignments", use_container_width=True):
                st.session_state.page = "faculty_assignments"
                st.rerun()
        
        # Today's schedule
        st.divider()
        st.subheader("📅 Today's Classes")
        
        classes = dashboard_data.get("todays_classes", [])
        if classes:
            for cls in classes:
                with st.container():
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.write(f"**{cls.get('course_name')}**")
                    with col2:
                        st.write(f"⏰ {cls.get('time')}")
                    with col3:
                        st.write(f"🏫 {cls.get('room')}")
                    st.divider()
        else:
            st.info("No classes scheduled for today")
    
    except Exception as e:
        st.error(f"Error loading dashboard: {str(e)}")
        show_demo_faculty_dashboard()


def show_admin_dashboard():
    """Show admin-specific dashboard"""
    st.subheader("🎓 Administrative Dashboard")
    
    # Fetch dashboard data
    try:
        with st.spinner("Loading dashboard data..."):
            dashboard_data = api_client.get("/api/dashboard/metrics")
        
        # Display key metrics
        st.subheader("📈 Key Metrics")
        metrics = [
            {
                "title": "Total Students",
                "value": dashboard_data.get("total_students", 0),
                "icon": "👨‍🎓",
                "color": "#0066cc"
            },
            {
                "title": "Total Faculty",
                "value": dashboard_data.get("total_faculty", 0),
                "icon": "👨‍🏫",
                "color": "#28a745"
            },
            {
                "title": "Active Courses",
                "value": dashboard_data.get("active_courses", 0),
                "icon": "📚",
                "color": "#ffc107"
            },
            {
                "title": "Library Books",
                "value": dashboard_data.get("total_books", 0),
                "icon": "📖",
                "color": "#dc3545"
            }
        ]
        render_stats_cards(metrics)
        
        # Charts section
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Student Enrollment by Program")
            enrollment_data = dashboard_data.get("enrollment_by_program", [])
            if enrollment_data:
                df_enrollment = pd.DataFrame(enrollment_data)
                render_pie_chart(df_enrollment, "program", "count", "Enrollment Distribution")
            else:
                st.info("No enrollment data available")
        
        with col2:
            st.subheader("📈 Attendance Trends")
            attendance_data = dashboard_data.get("attendance_trends", [])
            if attendance_data:
                df_attendance = pd.DataFrame(attendance_data)
                render_line_chart(df_attendance, "date", "percentage", "Attendance Over Time")
            else:
                st.info("No attendance data available")
        
        # Financial overview
        st.divider()
        st.subheader("💰 Financial Overview")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_revenue = dashboard_data.get("total_revenue", 0)
            st.metric("Total Revenue", f"₹{total_revenue:,.2f}", delta="+12.5%")
        
        with col2:
            total_expenses = dashboard_data.get("total_expenses", 0)
            st.metric("Total Expenses", f"₹{total_expenses:,.2f}", delta="-8.2%")
        
        with col3:
            net_profit = total_revenue - total_expenses
            st.metric("Net Profit", f"₹{net_profit:,.2f}", delta="+15.3%")
        
        # Recent activities
        st.divider()
        st.subheader("🔔 Recent Activities")
        
        activities = dashboard_data.get("recent_activities", [])
        if activities:
            for activity in activities[:5]:
                with st.expander(f"{activity.get('type', '')} - {activity.get('timestamp', '')}"):
                    st.write(activity.get('description', ''))
        else:
            st.info("No recent activities")
        
        # Pending tasks
        st.divider()
        st.subheader("📋 Pending Tasks")
        
        pending_tasks = dashboard_data.get("pending_tasks", [])
        if pending_tasks:
            df_tasks = pd.DataFrame(pending_tasks)
            st.dataframe(df_tasks, use_container_width=True)
        else:
            st.success("✅ No pending tasks!")
        
    except Exception as e:
        st.error(f"Error loading dashboard: {str(e)}")
        st.info("Using demo data...")
        
def show_admin_dashboard():
    """Show admin-specific dashboard"""
    st.subheader("🎓 Administrative Dashboard")
    
    # Fetch dashboard data
    try:
        with st.spinner("Loading dashboard data..."):
            dashboard_data = api_client.get("/api/dashboard/metrics")
        
        # Display key metrics
        st.markdown("#### 📈 Key Metrics")
        metrics = [
            {
                "title": "Total Students",
                "value": dashboard_data.get("total_students", 0),
                "icon": "👨‍🎓",
                "color": "#0066cc"
            },
            {
                "title": "Total Faculty",
                "value": dashboard_data.get("total_faculty", 0),
                "icon": "👨‍🏫",
                "color": "#28a745"
            },
            {
                "title": "Active Courses",
                "value": dashboard_data.get("active_courses", 0),
                "icon": "📚",
                "color": "#ffc107"
            },
            {
                "title": "Library Books",
                "value": dashboard_data.get("total_books", 0),
                "icon": "📖",
                "color": "#dc3545"
            }
        ]
        render_stats_cards(metrics)
        
        # Charts section
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Student Enrollment by Program")
            enrollment_data = dashboard_data.get("enrollment_by_program", [])
            if enrollment_data:
                df_enrollment = pd.DataFrame(enrollment_data)
                render_pie_chart(df_enrollment, "program", "count", "Enrollment Distribution")
            else:
                st.info("No enrollment data available")
        
        with col2:
            st.subheader("📈 Attendance Trends")
            attendance_data = dashboard_data.get("attendance_trends", [])
            if attendance_data:
                df_attendance = pd.DataFrame(attendance_data)
                render_line_chart(df_attendance, "date", "percentage", "Attendance Over Time")
            else:
                st.info("No attendance data available")
        
        # Financial overview
        st.divider()
        st.subheader("💰 Financial Overview")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_revenue = dashboard_data.get("total_revenue", 0)
            st.metric("Total Revenue", f"₹{total_revenue:,.2f}", delta="+12.5%")
        
        with col2:
            total_expenses = dashboard_data.get("total_expenses", 0)
            st.metric("Total Expenses", f"₹{total_expenses:,.2f}", delta="-8.2%")
        
        with col3:
            net_profit = total_revenue - total_expenses
            st.metric("Net Profit", f"₹{net_profit:,.2f}", delta="+15.3%")
        
        # Recent activities
        st.divider()
        st.subheader("🔔 Recent Activities")
        
        activities = dashboard_data.get("recent_activities", [])
        if activities:
            for activity in activities[:5]:
                with st.expander(f"{activity.get('type', '')} - {activity.get('timestamp', '')}"):
                    st.write(activity.get('description', ''))
        else:
            st.info("No recent activities")
        
        # Pending tasks
        st.divider()
        st.subheader("📋 Pending Tasks")
        
        pending_tasks = dashboard_data.get("pending_tasks", [])
        if pending_tasks:
            df_tasks = pd.DataFrame(pending_tasks)
            st.dataframe(df_tasks, use_container_width=True)
        else:
            st.success("✅ No pending tasks!")
        
    except Exception as e:
        st.error(f"Error loading dashboard: {str(e)}")
        st.info("Using demo data...")
        
        # Demo metrics
        demo_metrics = [
            {"title": "Total Students", "value": 1250, "icon": "👨‍🎓", "color": "#0066cc"},
            {"title": "Total Faculty", "value": 85, "icon": "👨‍🏫", "color": "#28a745"},
            {"title": "Active Courses", "value": 45, "icon": "📚", "color": "#ffc107"},
            {"title": "Library Books", "value": 5000, "icon": "📖", "color": "#dc3545"}
        ]
        render_stats_cards(demo_metrics)


def show_demo_student_dashboard():
    """Show demo student dashboard"""
    st.info("Showing demo data...")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Enrolled Courses", 6)
    with col2:
        st.metric("Attendance", "85%", delta="Good")
    with col3:
        st.metric("Pending Assignments", 3)
    with col4:
        st.metric("CGPA", "8.5")


def show_demo_faculty_dashboard():
    """Show demo faculty dashboard"""
    st.info("Showing demo data...")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Courses Teaching", 3)
    with col2:
        st.metric("Total Students", 120)
    with col3:
        st.metric("Pending Grading", 15)
    with col4:
        st.metric("Classes This Week", 12)

