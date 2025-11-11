"""
Students Management Page
"""
import streamlit as st
import pandas as pd
from utils.api_client import api_client
from components.ui_components import render_data_table, render_form_field
from utils.helpers import show_success, show_error


def show():
    """Display students management page"""
    st.title("👨‍🎓 Students Management")
    
    # Tabs for different student operations
    tab1, tab2, tab3, tab4 = st.tabs(["📋 All Students", "➕ Add Student", "🔍 Search", "📊 Analytics"])
    
    with tab1:
        show_students_list()
    
    with tab2:
        show_add_student_form()
    
    with tab3:
        show_student_search()
    
    with tab4:
        show_student_analytics()


def show_students_list():
    """Display list of all students"""
    st.subheader("All Students")
    
    try:
        # Fetch students
        response = api_client.get("/api/students", params={"page": 1, "limit": 50})
        students = response.get("items", [])
        
        if students:
            df = pd.DataFrame(students)
            
            # Select columns to display
            display_columns = ["id", "first_name", "last_name", "email", "phone", "program", "status"]
            available_columns = [col for col in display_columns if col in df.columns]
            
            render_data_table(df[available_columns], "Student Records")
            
            # Student actions
            st.divider()
            student_id = st.selectbox("Select Student for Actions", df["id"].tolist())
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("👁️ View Details", use_container_width=True):
                    show_student_details(student_id)
            with col2:
                if st.button("✏️ Edit", use_container_width=True):
                    st.session_state.edit_student_id = student_id
            with col3:
                if st.button("🗑️ Delete", use_container_width=True):
                    if confirm_delete_student(student_id):
                        delete_student(student_id)
        else:
            st.info("No students found")
    
    except Exception as e:
        show_error(f"Error loading students: {str(e)}")


def show_add_student_form():
    """Display form to add new student"""
    st.subheader("Add New Student")
    
    with st.form("add_student_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = render_form_field("First Name", "text", required=True)
            last_name = render_form_field("Last Name", "text", required=True)
            email = render_form_field("Email", "text", required=True)
            phone = render_form_field("Phone", "text", required=True)
            date_of_birth = render_form_field("Date of Birth", "date", required=True)
        
        with col2:
            gender = st.selectbox("Gender *", ["Male", "Female", "Other"])
            program = st.selectbox("Program *", ["B.Tech", "M.Tech", "MBA", "BBA", "MCA"])
            admission_year = render_form_field("Admission Year", "number", min_value=2000, max_value=2030)
            blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
            address = render_form_field("Address", "textarea")
        
        submit = st.form_submit_button("➕ Add Student", use_container_width=True)
        
        if submit:
            student_data = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone,
                "date_of_birth": str(date_of_birth),
                "gender": gender.lower(),
                "program": program,
                "admission_year": admission_year,
                "blood_group": blood_group,
                "address": address
            }
            
            try:
                response = api_client.post("/api/students", student_data)
                show_success(f"Student added successfully! ID: {response.get('id')}")
                st.balloons()
            except Exception as e:
                show_error(f"Error adding student: {str(e)}")


def show_student_search():
    """Display student search interface"""
    st.subheader("Search Students")
    
    col1, col2 = st.columns(2)
    
    with col1:
        search_term = st.text_input("🔍 Search by name, email, or ID")
    
    with col2:
        program_filter = st.selectbox("Filter by Program", ["All", "B.Tech", "M.Tech", "MBA", "BBA", "MCA"])
    
    if search_term or program_filter != "All":
        try:
            params = {}
            if search_term:
                params["search"] = search_term
            if program_filter != "All":
                params["program"] = program_filter
            
            response = api_client.get("/api/students/search", params=params)
            results = response.get("items", [])
            
            if results:
                df = pd.DataFrame(results)
                render_data_table(df, f"Search Results ({len(results)} found)")
            else:
                st.info("No students found matching your criteria")
        
        except Exception as e:
            show_error(f"Error searching students: {str(e)}")


def show_student_analytics():
    """Display student analytics"""
    st.subheader("Student Analytics")
    
    try:
        analytics = api_client.get("/api/students/analytics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Students", analytics.get("total", 0))
        with col2:
            st.metric("Active Students", analytics.get("active", 0))
        with col3:
            st.metric("Graduated", analytics.get("graduated", 0))
        
        # More analytics charts can be added here
        
    except Exception as e:
        show_error(f"Error loading analytics: {str(e)}")


def show_student_details(student_id: int):
    """Show detailed student information"""
    try:
        student = api_client.get(f"/api/students/{student_id}")
        
        with st.expander("📋 Student Details", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Name:** {student.get('first_name')} {student.get('last_name')}")
                st.write(f"**Email:** {student.get('email')}")
                st.write(f"**Phone:** {student.get('phone')}")
                st.write(f"**Program:** {student.get('program')}")
            
            with col2:
                st.write(f"**Gender:** {student.get('gender', '').title()}")
                st.write(f"**DOB:** {student.get('date_of_birth')}")
                st.write(f"**Blood Group:** {student.get('blood_group')}")
                st.write(f"**Status:** {student.get('status', '').title()}")
    
    except Exception as e:
        show_error(f"Error loading student details: {str(e)}")


def confirm_delete_student(student_id: int) -> bool:
    """Confirm student deletion"""
    return st.checkbox(f"I confirm deletion of student ID: {student_id}", key=f"confirm_delete_{student_id}")


def delete_student(student_id: int):
    """Delete a student"""
    try:
        api_client.delete(f"/api/students/{student_id}")
        show_success(f"Student {student_id} deleted successfully")
        st.rerun()
    except Exception as e:
        show_error(f"Error deleting student: {str(e)}")
