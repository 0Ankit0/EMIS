"""
Add Employee
"""
import streamlit as st
from utils.api_client import api_client
from utils.helpers import show_error, show_success, show_info


def show():
    """Display add employee"""
    st.title("Add Employee")
    
    try:
        # Implement page functionality
        st.info("This feature is available")

    st.divider()
    st.subheader("Add New")
    
    with st.form("add_form"):
        name = st.text_input("Name *")
        description = st.text_area("Description")
        
        if st.form_submit_button("Submit"):
            if name:
                try:
                    api_client.post(endpoint, {"name": name, "description": description})
                    show_success("Added successfully!")
                    st.rerun()
                except Exception as e:
                    show_error(f"Error: {str(e)}")
            else:
                show_error("Please fill required fields")

    except Exception as e:
        show_error(f"Error: {str(e)}")
