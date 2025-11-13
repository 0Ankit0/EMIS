"""
Registration Page
"""
import streamlit as st
from services.auth_service import auth_service
from utils.helpers import show_error, show_success
from utils.validators import validate_email, validate_password, validate_phone


def show():
    """Display registration page"""
    st.title("📝 Register")
    st.markdown("### Create your account")
    
    with st.form("registration_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("Full Name *")
            email = st.text_input("Email *")
            password = st.text_input("Password *", type="password")
        
        with col2:
            phone = st.text_input("Phone Number *")
            role = st.selectbox("Select Role", ["Student", "Teacher", "Staff"])
            confirm_password = st.text_input("Confirm Password *", type="password")
        
        address = st.text_area("Address")
        terms = st.checkbox("I agree to the Terms and Conditions")
        
        submitted = st.form_submit_button("Register", type="primary")
        
        if submitted:
            if not all([full_name, email, password, phone, confirm_password]):
                show_error("Please fill all required fields")
            elif not validate_email(email):
                show_error("Invalid email address")
            elif not validate_phone(phone):
                show_error("Invalid phone number")
            elif password != confirm_password:
                show_error("Passwords do not match")
            else:
                is_valid, msg = validate_password(password)
                if not is_valid:
                    show_error(msg)
                elif not terms:
                    show_error("Please accept the terms and conditions")
                else:
                    register_user({
                        "name": full_name,
                        "email": email,
                        "password": password,
                        "phone": phone,
                        "role": role.lower(),
                        "address": address
                    })


def register_user(data):
    """Register new user"""
    try:
        response = auth_service.register(data)
        show_success("Registration successful! Please check your email to verify your account.")
        st.balloons()
    except Exception as e:
        show_error(f"Registration failed: {str(e)}")
