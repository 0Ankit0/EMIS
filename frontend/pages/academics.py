"""Academics Management Page"""
import streamlit as st
from utils.api_client import api_client
from utils.helpers import show_error

def show():
    st.title("📚 Academics Management")
    tabs = st.tabs(["📖 Courses", "📅 Timetable", "✏️ Exams", "📊 Results"])
    
    with tabs[0]:
        st.subheader("Courses")
        try:
            courses = api_client.get("/api/courses")
            st.dataframe(courses.get("items", []))
        except Exception as e:
            show_error(f"Error: {str(e)}")
    
    with tabs[1]:
        st.subheader("Timetable")
        st.info("Timetable management coming soon")
    
    with tabs[2]:
        st.subheader("Examinations")
        st.info("Exam management coming soon")
    
    with tabs[3]:
        st.subheader("Results")
        st.info("Results management coming soon")
