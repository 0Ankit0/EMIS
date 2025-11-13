"""
Faculty Grading Page
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from utils.api_client import api_client
from utils.helpers import show_error, show_success, show_info
from services.faculty_service import faculty_service


def show():
    """Display faculty grading page"""
    st.title("🎯 Grading & Marks Entry")
    st.markdown("### Enter and manage student grades")
    
    tab1, tab2, tab3 = st.tabs(["📝 Enter Marks", "📊 Gradebook", "📤 Bulk Upload"])
    
    with tab1:
        show_enter_marks()
    
    with tab2:
        show_gradebook()
    
    with tab3:
        show_bulk_upload()


def show_enter_marks():
    """Show marks entry interface"""
    st.subheader("Enter Exam Marks")
    
    try:
        faculty_id = st.session_state.user.get("id")
        courses = faculty_service.get_courses(faculty_id)
        
        if courses:
            course_options = {f"{c['name']} ({c['code']})": c['id'] for c in courses}
            selected_course = st.selectbox("Select Course", list(course_options.keys()))
            course_id = course_options[selected_course]
            
            # Get exams for this course
            exams_response = api_client.get(f"/api/courses/{course_id}/exams")
            exams = exams_response.get("items", [])
            
            if exams:
                exam_options = {f"{e['name']} - {e['exam_type']}": e['id'] for e in exams}
                selected_exam = st.selectbox("Select Exam", list(exam_options.keys()))
                exam_id = exam_options[selected_exam]
                
                # Get students
                students = faculty_service.get_course_students(course_id)
                
                if students:
                    st.divider()
                    st.subheader("Enter Marks")
                    
                    max_marks = st.number_input("Maximum Marks", min_value=1, max_value=100, value=100)
                    
                    marks_data = []
                    
                    for student in students:
                        col1, col2, col3 = st.columns([2, 1, 1])
                        
                        with col1:
                            st.write(f"**{student.get('name', 'Student')}**")
                            st.caption(f"Roll No: {student.get('roll_no', 'N/A')}")
                        
                        with col2:
                            marks = st.number_input(
                                "Marks",
                                min_value=0.0,
                                max_value=float(max_marks),
                                value=0.0,
                                step=0.5,
                                key=f"marks_{student.get('id')}",
                                label_visibility="collapsed"
                            )
                            marks_data.append({
                                "student_id": student['id'],
                                "marks": marks
                            })
                        
                        with col3:
                            percentage = (marks / max_marks * 100) if max_marks > 0 else 0
                            if percentage >= 40:
                                st.success(f"{percentage:.1f}%")
                            else:
                                st.error(f"{percentage:.1f}%")
                    
                    st.divider()
                    
                    if st.button("💾 Save All Marks", type="primary", use_container_width=True):
                        save_marks(exam_id, marks_data)
                else:
                    show_info("No students enrolled")
            else:
                show_info("No exams scheduled for this course")
        else:
            show_info("You are not teaching any courses")
    
    except Exception as e:
        show_error(f"Error: {str(e)}")


def show_gradebook():
    """Show course gradebook"""
    st.subheader("Gradebook")
    
    try:
        faculty_id = st.session_state.user.get("id")
        courses = faculty_service.get_courses(faculty_id)
        
        if courses:
            course_options = {f"{c['name']} ({c['code']})": c['id'] for c in courses}
            selected_course = st.selectbox("Select Course", list(course_options.keys()), key="gradebook_course")
            course_id = course_options[selected_course]
            
            gradebook = faculty_service.get_gradebook(course_id)
            
            if gradebook:
                students = gradebook.get('students', [])
                
                if students:
                    df = pd.DataFrame(students)
                    
                    # Display summary statistics
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Total Students", len(students))
                    with col2:
                        avg_score = df['total_marks'].mean() if 'total_marks' in df.columns else 0
                        st.metric("Average Score", f"{avg_score:.2f}")
                    with col3:
                        pass_count = len([s for s in students if s.get('percentage', 0) >= 40])
                        st.metric("Pass Count", pass_count)
                    with col4:
                        fail_count = len(students) - pass_count
                        st.metric("Fail Count", fail_count)
                    
                    st.divider()
                    
                    # Display gradebook table
                    st.dataframe(df, use_container_width=True)
                    
                    # Export option
                    csv = df.to_csv(index=False)
                    st.download_button(
                        "📥 Download Gradebook (CSV)",
                        csv,
                        f"gradebook_{selected_course}_{datetime.now().strftime('%Y%m%d')}.csv",
                        "text/csv"
                    )
                else:
                    show_info("No grades recorded yet")
            else:
                show_info("Gradebook not available")
        else:
            show_info("You are not teaching any courses")
    
    except Exception as e:
        show_error(f"Error loading gradebook: {str(e)}")


def show_bulk_upload():
    """Show bulk marks upload"""
    st.subheader("Bulk Marks Upload")
    
    st.info("📋 Upload marks using CSV file")
    
    # Download template
    template_df = pd.DataFrame({
        'roll_no': ['CS001', 'CS002', 'CS003'],
        'student_name': ['John Doe', 'Jane Smith', 'Bob Johnson'],
        'marks': [85, 92, 78]
    })
    
    template_csv = template_df.to_csv(index=False)
    st.download_button(
        "📥 Download Template",
        template_csv,
        "marks_template.csv",
        "text/csv"
    )
    
    st.divider()
    
    try:
        faculty_id = st.session_state.user.get("id")
        courses = faculty_service.get_courses(faculty_id)
        
        if courses:
            course_options = {f"{c['name']} ({c['code']})": c['id'] for c in courses}
            selected_course = st.selectbox("Select Course", list(course_options.keys()), key="bulk_course")
            course_id = course_options[selected_course]
            
            # Get exams
            exams_response = api_client.get(f"/api/courses/{course_id}/exams")
            exams = exams_response.get("items", [])
            
            if exams:
                exam_options = {f"{e['name']} - {e['exam_type']}": e['id'] for e in exams}
                selected_exam = st.selectbox("Select Exam", list(exam_options.keys()), key="bulk_exam")
                exam_id = exam_options[selected_exam]
                
                uploaded_file = st.file_uploader("Upload Marks CSV", type=['csv'])
                
                if uploaded_file:
                    try:
                        df = pd.read_csv(uploaded_file)
                        
                        st.write("**Preview:**")
                        st.dataframe(df.head(10))
                        
                        if st.button("📤 Upload Marks"):
                            upload_bulk_marks(exam_id, df)
                    
                    except Exception as e:
                        show_error(f"Error reading CSV: {str(e)}")
            else:
                show_info("No exams available")
        else:
            show_info("You are not teaching any courses")
    
    except Exception as e:
        show_error(f"Error: {str(e)}")


def save_marks(exam_id, marks_data):
    """Save exam marks"""
    try:
        faculty_service.enter_marks(exam_id, marks_data)
        show_success(f"Marks saved successfully for {len(marks_data)} students!")
        st.balloons()
    except Exception as e:
        show_error(f"Error saving marks: {str(e)}")


def upload_bulk_marks(exam_id, df):
    """Upload marks from CSV"""
    try:
        # Convert dataframe to marks data
        marks_data = []
        for _, row in df.iterrows():
            marks_data.append({
                "roll_no": row['roll_no'],
                "marks": row['marks']
            })
        
        api_client.post(f"/api/exams/{exam_id}/marks/bulk", {"marks": marks_data})
        show_success(f"Successfully uploaded marks for {len(marks_data)} students!")
        st.balloons()
    except Exception as e:
        show_error(f"Error uploading marks: {str(e)}")
