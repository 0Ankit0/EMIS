"""Library Management Page"""
import streamlit as st
from utils.api_client import api_client
from utils.helpers import show_error

def show():
    st.title("📖 Library Management")
    tabs = st.tabs(["�� Books", "🔄 Circulation", "💰 Fines", "📊 Reports"])
    
    with tabs[0]:
        st.subheader("Books Catalog")
        try:
            books = api_client.get("/api/library/books")
            st.dataframe(books.get("items", []))
        except Exception as e:
            show_error(f"Error: {str(e)}")
    
    with tabs[1]:
        st.subheader("Circulation")
        st.info("Circulation management coming soon")
    
    with tabs[2]:
        st.subheader("Fines")
        st.info("Fine management coming soon")
    
    with tabs[3]:
        st.subheader("Library Reports")
        st.info("Reports coming soon")
