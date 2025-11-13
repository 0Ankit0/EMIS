"""
Placement Page
"""
import streamlit as st
from utils.api_client import api_client
from utils.helpers import show_error, show_info


def show():
    """Display placement page"""
    st.title("💼 Placement & Careers")
    
    tab1, tab2 = st.tabs(["Job Openings", "My Applications"])
    
    with tab1:
        try:
            response = api_client.get("/api/placements/jobs")
            jobs = response.get("items", [])
            
            if jobs:
                for job in jobs:
                    with st.expander(f"📢 {job.get('company')} - {job.get('position')}"):
                        st.write(f"**Package:** {job.get('package')}")
                        st.write(f"**Location:** {job.get('location')}")
                        if st.button("Apply", key=f"apply_{job.get('id')}"):
                            st.success("Application submitted!")
            else:
                show_info("No job openings available")
        except Exception as e:
            show_error(f"Error: {str(e)}")
    
    with tab2:
        show_info("No applications yet")
