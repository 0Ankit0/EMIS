"""Finance Management Page"""
import streamlit as st
from utils.api_client import api_client
from utils.helpers import show_error, format_currency

def show():
    st.title("💰 Finance Management")
    tabs = st.tabs(["💳 Billing", "📊 Accounting", "📈 Reports", "📋 Budget"])
    
    with tabs[0]:
        st.subheader("Billing & Payments")
        try:
            bills = api_client.get("/api/finance/bills")
            st.dataframe(bills.get("items", []))
        except Exception as e:
            show_error(f"Error: {str(e)}")
    
    with tabs[1]:
        st.subheader("Accounting")
        st.info("Accounting management coming soon")
    
    with tabs[2]:
        st.subheader("Financial Reports")
        st.info("Financial reports coming soon")
    
    with tabs[3]:
        st.subheader("Budget Management")
        st.info("Budget management coming soon")
