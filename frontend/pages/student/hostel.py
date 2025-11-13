"""
Hostel Information Page
"""
import streamlit as st
from utils.api_client import api_client
from utils.helpers import show_error, show_info


def show():
    """Display hostel information page"""
    st.title("🏠 Hostel Information")
    
    try:
        student_id = st.session_state.user.get("id")
        response = api_client.get(f"/api/students/{student_id}/hostel")
        
        if response.get("allocated"):
            hostel = response.get("hostel", {})
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Hostel", hostel.get("name", "N/A"))
            with col2:
                st.metric("Room No", hostel.get("room_no", "N/A"))
            with col3:
                st.metric("Block", hostel.get("block", "N/A"))
            
            st.divider()
            
            st.subheader("Room Details")
            st.write(f"**Floor:** {hostel.get('floor', 'N/A')}")
            st.write(f"**Capacity:** {hostel.get('capacity', 'N/A')}")
            st.write(f"**Occupancy:** {hostel.get('occupancy', 'N/A')}")
            
            if st.button("Raise Complaint"):
                st.session_state.show_complaint_form = True
        else:
            show_info("You are not allocated any hostel room")
    
    except Exception as e:
        show_error(f"Error loading hostel information: {str(e)}")
