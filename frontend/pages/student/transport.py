"""
Transport Information Page
"""
import streamlit as st
from utils.api_client import api_client
from utils.helpers import show_error, show_info


def show():
    """Display transport information page"""
    st.title("🚌 Transport Information")
    
    try:
        student_id = st.session_state.user.get("id")
        response = api_client.get(f"/api/students/{student_id}/transport")
        
        if response.get("allocated"):
            transport = response.get("transport", {})
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Route No", transport.get("route_no", "N/A"))
            with col2:
                st.metric("Bus No", transport.get("bus_no", "N/A"))
            with col3:
                st.metric("Stop", transport.get("stop", "N/A"))
            
            st.divider()
            
            st.subheader("Schedule")
            st.write(f"**Morning Pickup:** {transport.get('morning_time', 'N/A')}")
            st.write(f"**Evening Drop:** {transport.get('evening_time', 'N/A')}")
        else:
            show_info("You are not allocated any transport")
    
    except Exception as e:
        show_error(f"Error: {str(e)}")
