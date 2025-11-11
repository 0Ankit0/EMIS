"""
Admissions Management Page
"""
import streamlit as st
import pandas as pd
from utils.api_client import api_client
from components.ui_components import render_data_table
from utils.helpers import show_success, show_error


def show():
    """Display admissions management page"""
    st.title("📝 Admissions Management")
    
    tabs = st.tabs(["📋 Applications", "✅ Approved", "❌ Rejected", "📊 Statistics"])
    
    with tabs[0]:
        show_applications()
    with tabs[1]:
        show_approved_applications()
    with tabs[2]:
        show_rejected_applications()
    with tabs[3]:
        show_admission_statistics()


def show_applications():
    """Show pending applications"""
    st.subheader("Pending Applications")
    
    try:
        response = api_client.get("/api/admissions/applications", params={"status": "pending"})
        applications = response.get("items", [])
        
        if applications:
            df = pd.DataFrame(applications)
            render_data_table(df, "Applications")
        else:
            st.info("No pending applications")
    except Exception as e:
        show_error(f"Error loading applications: {str(e)}")


def show_approved_applications():
    """Show approved applications"""
    st.subheader("Approved Applications")
    
    try:
        response = api_client.get("/api/admissions/applications", params={"status": "approved"})
        applications = response.get("items", [])
        
        if applications:
            df = pd.DataFrame(applications)
            render_data_table(df, "Approved Applications")
        else:
            st.info("No approved applications")
    except Exception as e:
        show_error(f"Error loading applications: {str(e)}")


def show_rejected_applications():
    """Show rejected applications"""
    st.subheader("Rejected Applications")
    
    try:
        response = api_client.get("/api/admissions/applications", params={"status": "rejected"})
        applications = response.get("items", [])
        
        if applications:
            df = pd.DataFrame(applications)
            render_data_table(df, "Rejected Applications")
        else:
            st.info("No rejected applications")
    except Exception as e:
        show_error(f"Error loading applications: {str(e)}")


def show_admission_statistics():
    """Show admission statistics"""
    st.subheader("Admission Statistics")
    
    try:
        stats = api_client.get("/api/admissions/statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Applications", stats.get("total", 0))
        with col2:
            st.metric("Pending", stats.get("pending", 0))
        with col3:
            st.metric("Approved", stats.get("approved", 0))
        with col4:
            st.metric("Rejected", stats.get("rejected", 0))
    except Exception as e:
        show_error(f"Error loading statistics: {str(e)}")
