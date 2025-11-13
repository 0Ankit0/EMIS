"""
Student Exams and Results Page
"""
import streamlit as st
import pandas as pd
from utils.api_client import api_client
from utils.helpers import show_error, show_info
from components.ui_components import render_data_table


def show():
    """Display student exams and results page"""
    st.title("🏆 Exams & Results")
    st.markdown("### View exam schedule and your results")
    
    tab1, tab2, tab3 = st.tabs(["📅 Upcoming Exams", "📊 Results", "📄 Hall Tickets"])
    
    with tab1:
        show_upcoming_exams()
    
    with tab2:
        show_results()
    
    with tab3:
        show_hall_tickets()


def show_upcoming_exams():
    """Show upcoming exams"""
    st.subheader("Upcoming Exams")
    
    try:
        student_id = st.session_state.user.get("id")
        response = api_client.get(f"/api/students/{student_id}/exams/upcoming")
        exams = response.get("items", [])
        
        if exams:
            for exam in exams:
                with st.container():
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.markdown(f"### 📝 {exam.get('course_name', 'Exam')}")
                        st.write(f"**Course Code:** {exam.get('course_code', 'N/A')}")
                        st.write(f"**Type:** {exam.get('exam_type', 'N/A')}")
                    
                    with col2:
                        st.write(f"**Date:** {exam.get('exam_date', 'N/A')}")
                        st.write(f"**Time:** {exam.get('exam_time', 'N/A')}")
                    
                    with col3:
                        st.write(f"**Duration:** {exam.get('duration', 'N/A')} hrs")
                        st.write(f"**Room:** {exam.get('room', 'N/A')}")
                    
                    st.write(f"**Syllabus:** {exam.get('syllabus', 'Full syllabus')}")
                    
                    if st.button(f"Download Hall Ticket", key=f"hall_ticket_{exam.get('id')}"):
                        download_hall_ticket(exam.get('id'))
                    
                    st.divider()
        else:
            show_info("No upcoming exams")
    
    except Exception as e:
        show_error(f"Error loading exams: {str(e)}")
        show_demo_exams()


def show_results():
    """Show exam results"""
    st.subheader("Exam Results")
    
    try:
        student_id = st.session_state.user.get("id")
        response = api_client.get(f"/api/students/{student_id}/results")
        results = response.get("items", [])
        
        if results:
            # Overall performance
            st.subheader("📊 Overall Performance")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                total_subjects = len(results)
                st.metric("Total Subjects", total_subjects)
            
            with col2:
                avg_marks = sum([r.get('marks_obtained', 0) for r in results]) / total_subjects if total_subjects > 0 else 0
                st.metric("Average Marks", f"{avg_marks:.2f}")
            
            with col3:
                passed = sum([1 for r in results if r.get('marks_obtained', 0) >= r.get('passing_marks', 40)])
                st.metric("Passed Subjects", f"{passed}/{total_subjects}")
            
            # Subject-wise results
            st.divider()
            st.subheader("📚 Subject-wise Results")
            
            for result in results:
                with st.container():
                    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                    
                    with col1:
                        st.write(f"**{result.get('course_name', 'Course')}**")
                        st.caption(result.get('course_code', ''))
                    
                    with col2:
                        marks = result.get('marks_obtained', 0)
                        max_marks = result.get('max_marks', 100)
                        st.write(f"**Marks:** {marks}/{max_marks}")
                    
                    with col3:
                        percentage = (marks / max_marks * 100) if max_marks > 0 else 0
                        st.write(f"**Percentage:** {percentage:.1f}%")
                    
                    with col4:
                        grade = calculate_grade(percentage)
                        if grade in ['A+', 'A']:
                            st.success(f"**Grade:** {grade}")
                        elif grade in ['B+', 'B']:
                            st.info(f"**Grade:** {grade}")
                        elif grade in ['C+', 'C']:
                            st.warning(f"**Grade:** {grade}")
                        else:
                            st.error(f"**Grade:** {grade}")
                    
                    st.divider()
            
            # Download transcript
            if st.button("📄 Download Transcript"):
                download_transcript()
        else:
            show_info("No results available yet")
    
    except Exception as e:
        show_error(f"Error loading results: {str(e)}")


def show_hall_tickets():
    """Show available hall tickets"""
    st.subheader("Hall Tickets")
    
    try:
        student_id = st.session_state.user.get("id")
        response = api_client.get(f"/api/students/{student_id}/hall-tickets")
        tickets = response.get("items", [])
        
        if tickets:
            for ticket in tickets:
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**{ticket.get('exam_name', 'Exam')}** - {ticket.get('exam_date', 'N/A')}")
                
                with col2:
                    if st.button("📥 Download", key=f"download_{ticket.get('id')}"):
                        download_hall_ticket(ticket.get('id'))
                
                st.divider()
        else:
            show_info("No hall tickets available")
    
    except Exception as e:
        show_error(f"Error loading hall tickets: {str(e)}")


def calculate_grade(percentage):
    """Calculate grade from percentage"""
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B+"
    elif percentage >= 60:
        return "B"
    elif percentage >= 50:
        return "C+"
    elif percentage >= 40:
        return "C"
    else:
        return "F"


def download_hall_ticket(exam_id):
    """Download hall ticket"""
    try:
        response = api_client.get(f"/api/exams/{exam_id}/hall-ticket", stream=True)
        st.success("Hall ticket download started!")
    except Exception as e:
        show_error(f"Error downloading hall ticket: {str(e)}")


def download_transcript():
    """Download academic transcript"""
    try:
        student_id = st.session_state.user.get("id")
        response = api_client.get(f"/api/students/{student_id}/transcript", stream=True)
        st.success("Transcript download started!")
    except Exception as e:
        show_error(f"Error downloading transcript: {str(e)}")


def show_demo_exams():
    """Show demo exam data"""
    st.info("Showing demo data...")
    
    demo_exams = [
        {
            "id": 1,
            "course_name": "Data Structures",
            "course_code": "CS201",
            "exam_type": "Mid-Term",
            "exam_date": "2024-12-20",
            "exam_time": "10:00 AM",
            "duration": "2",
            "room": "Hall A",
            "syllabus": "Chapters 1-5"
        }
    ]
    
    for exam in demo_exams:
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"### 📝 {exam['course_name']}")
            st.write(f"**Course Code:** {exam['course_code']}")
        
        with col2:
            st.write(f"**Date:** {exam['exam_date']}")
            st.write(f"**Time:** {exam['exam_time']}")
        
        with col3:
            st.write(f"**Duration:** {exam['duration']} hrs")
            st.write(f"**Room:** {exam['room']}")
