"""
Common Profile Page for All Users
"""
import streamlit as st
from utils.api_client import api_client
from utils.helpers import show_error, show_success, show_info


def show():
    """Display user profile page"""
    st.title("👤 My Profile")
    st.markdown("### View and update your profile information")
    
    user = st.session_state.get("user", {})
    user_role = st.session_state.get("user_role", "student")
    
    tab1, tab2, tab3 = st.tabs(["📋 View Profile", "✏️ Edit Profile", "🔒 Change Password"])
    
    with tab1:
        show_profile_view(user, user_role)
    
    with tab2:
        show_profile_edit(user, user_role)
    
    with tab3:
        show_change_password()


def show_profile_view(user, role):
    """Display profile information"""
    st.subheader("Profile Information")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Profile photo
        st.image("https://via.placeholder.com/150", caption="Profile Photo", width=150)
        if st.button("📷 Upload Photo"):
            st.info("Photo upload feature coming soon!")
    
    with col2:
        st.markdown(f"### {user.get('name', 'User Name')}")
        st.caption(f"Role: {role.title()}")
        
        st.divider()
        
        # Basic information
        st.write(f"**Email:** {user.get('email', 'N/A')}")
        st.write(f"**Phone:** {user.get('phone', 'N/A')}")
        st.write(f"**ID:** {user.get('id', 'N/A')}")
        
        if role == "student":
            st.write(f"**Program:** {user.get('program', 'N/A')}")
            st.write(f"**Year:** {user.get('year', 'N/A')}")
            st.write(f"**Roll No:** {user.get('roll_no', 'N/A')}")
        elif role in ["teacher", "staff", "admin"]:
            st.write(f"**Department:** {user.get('department', 'N/A')}")
            st.write(f"**Designation:** {user.get('designation', 'N/A')}")
            st.write(f"**Employee ID:** {user.get('employee_id', 'N/A')}")
    
    # Additional details
    st.divider()
    st.subheader("Additional Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Date of Birth:** {user.get('date_of_birth', 'N/A')}")
        st.write(f"**Gender:** {user.get('gender', 'N/A')}")
        st.write(f"**Blood Group:** {user.get('blood_group', 'N/A')}")
    
    with col2:
        st.write(f"**Address:** {user.get('address', 'N/A')}")
        st.write(f"**City:** {user.get('city', 'N/A')}")
        st.write(f"**State:** {user.get('state', 'N/A')}")
        st.write(f"**Pincode:** {user.get('pincode', 'N/A')}")
    
    # Emergency contact
    st.divider()
    st.subheader("Emergency Contact")
    
    emergency_contact = user.get('emergency_contact', {})
    if emergency_contact:
        st.write(f"**Name:** {emergency_contact.get('name', 'N/A')}")
        st.write(f"**Relationship:** {emergency_contact.get('relationship', 'N/A')}")
        st.write(f"**Phone:** {emergency_contact.get('phone', 'N/A')}")
    else:
        st.info("No emergency contact information available")


def show_profile_edit(user, role):
    """Edit profile information"""
    st.subheader("Edit Profile")
    
    with st.form("edit_profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name", value=user.get('name', ''))
            email = st.text_input("Email", value=user.get('email', ''))
            phone = st.text_input("Phone", value=user.get('phone', ''))
            date_of_birth = st.date_input("Date of Birth")
        
        with col2:
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], 
                                index=["male", "female", "other"].index(user.get('gender', 'male').lower()) if user.get('gender') else 0)
            blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
            city = st.text_input("City", value=user.get('city', ''))
            state = st.text_input("State", value=user.get('state', ''))
        
        address = st.text_area("Address", value=user.get('address', ''))
        pincode = st.text_input("Pincode", value=user.get('pincode', ''))
        
        st.divider()
        st.subheader("Emergency Contact")
        
        col1, col2 = st.columns(2)
        
        with col1:
            emergency_name = st.text_input("Emergency Contact Name")
            emergency_phone = st.text_input("Emergency Contact Phone")
        
        with col2:
            emergency_relationship = st.text_input("Relationship")
        
        submit = st.form_submit_button("💾 Save Changes", type="primary")
        
        if submit:
            profile_data = {
                "name": name,
                "email": email,
                "phone": phone,
                "date_of_birth": str(date_of_birth),
                "gender": gender.lower(),
                "blood_group": blood_group,
                "address": address,
                "city": city,
                "state": state,
                "pincode": pincode,
                "emergency_contact": {
                    "name": emergency_name,
                    "phone": emergency_phone,
                    "relationship": emergency_relationship
                }
            }
            
            update_profile(profile_data)


def show_change_password():
    """Change password form"""
    st.subheader("Change Password")
    
    with st.form("change_password_form"):
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        
        # Password strength indicator
        if new_password:
            strength = check_password_strength(new_password)
            if strength == "Strong":
                st.success("✅ Strong password")
            elif strength == "Medium":
                st.warning("⚠️ Medium strength password")
            else:
                st.error("❌ Weak password")
        
        submit = st.form_submit_button("🔒 Change Password", type="primary")
        
        if submit:
            if not current_password or not new_password or not confirm_password:
                show_error("Please fill all fields")
            elif new_password != confirm_password:
                show_error("New passwords do not match")
            elif len(new_password) < 8:
                show_error("Password must be at least 8 characters long")
            else:
                change_password(current_password, new_password)


def update_profile(data):
    """Update user profile"""
    try:
        user_id = st.session_state.user.get("id")
        response = api_client.put(f"/api/users/{user_id}", data)
        
        # Update session state
        st.session_state.user = response
        
        show_success("Profile updated successfully!")
        st.rerun()
    except Exception as e:
        show_error(f"Error updating profile: {str(e)}")


def change_password(current_password, new_password):
    """Change user password"""
    try:
        data = {
            "current_password": current_password,
            "new_password": new_password
        }
        response = api_client.post("/api/auth/change-password", data)
        show_success("Password changed successfully!")
    except Exception as e:
        show_error(f"Error changing password: {str(e)}")


def check_password_strength(password):
    """Check password strength"""
    if len(password) >= 12 and any(c.isupper() for c in password) and any(c.isdigit() for c in password) and any(c in "!@#$%^&*" for c in password):
        return "Strong"
    elif len(password) >= 8 and (any(c.isupper() for c in password) or any(c.isdigit() for c in password)):
        return "Medium"
    else:
        return "Weak"
