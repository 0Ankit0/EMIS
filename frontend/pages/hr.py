"""HR & Payroll Management Page"""
import streamlit as st
from utils.api_client import api_client
from utils.helpers import show_error

def show():
    st.title("💼 HR & Payroll Management")
    tabs = st.tabs(["👥 Employees", "💰 Payroll", "📅 Leave", "📊 Performance"])
    
    with tabs[0]:
        st.subheader("Employees")
        try:
            employees = api_client.get("/api/hr/employees")
            st.dataframe(employees.get("items", []))
        except Exception as e:
            show_error(f"Error: {str(e)}")
    
    with tabs[1]:
        st.subheader("Payroll")
        st.info("Payroll management coming soon")
    
    with tabs[2]:
        st.subheader("Leave Management")
        st.info("Leave management coming soon")
    
    with tabs[3]:
        st.subheader("Performance Reviews")
        st.info("Performance management coming soon")
