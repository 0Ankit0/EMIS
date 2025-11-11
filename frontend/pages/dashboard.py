"""
Dashboard Page - Main Overview
"""
import streamlit as st
import pandas as pd
from utils.api_client import api_client
from components.ui_components import render_stats_cards, render_bar_chart, render_line_chart, render_pie_chart


def show():
    """Display dashboard page"""
    st.title("📊 Dashboard")
    st.markdown("### Welcome to EMIS - Education Management Information System")
    
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
        
        # Demo metrics
        demo_metrics = [
            {"title": "Total Students", "value": 1250, "icon": "👨‍🎓", "color": "#0066cc"},
            {"title": "Total Faculty", "value": 85, "icon": "👨‍🏫", "color": "#28a745"},
            {"title": "Active Courses", "value": 45, "icon": "📚", "color": "#ffc107"},
            {"title": "Library Books", "value": 5000, "icon": "📖", "color": "#dc3545"}
        ]
        render_stats_cards(demo_metrics)
