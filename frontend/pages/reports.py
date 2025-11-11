"""Reports Page"""
import streamlit as st
from utils.api_client import api_client
from utils.helpers import show_error

def show():
    st.title("📊 Reports & Analytics")
    tabs = st.tabs(["📈 Dashboard", "📋 Custom Reports", "📅 Quarterly", "📊 Annual"])
    
    with tabs[0]:
        st.subheader("Analytics Dashboard")
        try:
            analytics = api_client.get("/api/reports/dashboard")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Revenue", f"₹{analytics.get('revenue', 0):,.2f}")
            with col2:
                st.metric("Total Expenses", f"₹{analytics.get('expenses', 0):,.2f}")
            with col3:
                st.metric("Net Profit", f"₹{analytics.get('profit', 0):,.2f}")
        except Exception as e:
            show_error(f"Error: {str(e)}")
    
    with tabs[1]:
        st.subheader("Custom Reports")
        st.info("Custom report builder coming soon")
    
    with tabs[2]:
        st.subheader("Quarterly Reports")
        st.info("Quarterly reports coming soon")
    
    with tabs[3]:
        st.subheader("Annual Reports")
        st.info("Annual reports coming soon")
