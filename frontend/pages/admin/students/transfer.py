"""
Student Transfer
"""
import streamlit as st
from utils.api_client import api_client
from utils.helpers import show_error, show_success, show_info


def show():
    """Display student transfer"""
    st.title("Student Transfer")
    
    try:
        response = api_client.get("/api/students/transfer")
        items = response.get("items", [])
        
        if items:
            for item in items:
                with st.expander(f"{item.get('name', 'Item')}"):
                    for key, value in item.items():
                        st.write(f"**{key.replace('_', ' ').title()}:** {value}")
        else:
            show_info("No items found")
    except Exception as e:
        show_error(f"Error: {str(e)}")
