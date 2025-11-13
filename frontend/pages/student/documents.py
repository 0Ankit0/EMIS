"""
Student Documents Upload Page
"""
import streamlit as st
from utils.api_client import api_client
from utils.helpers import show_error, show_success, show_info
from utils.file_handler import validate_file, upload_file
import pandas as pd


def show():
    """Display documents upload page"""
    st.title("📄 My Documents")
    st.markdown("### Upload and manage your documents")
    
    tab1, tab2 = st.tabs(["Uploaded Documents", "Upload New"])
    
    with tab1:
        show_uploaded_documents()
    
    with tab2:
        show_upload_form()


def show_uploaded_documents():
    """Display uploaded documents"""
    st.subheader("Uploaded Documents")
    
    try:
        student_id = st.session_state.user.get("id")
        response = api_client.get(f"/api/students/{student_id}/documents")
        documents = response.get("items", [])
        
        if documents:
            for doc in documents:
                with st.container():
                    col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
                    
                    with col1:
                        doc_icon = "📄" if doc.get('type') == 'pdf' else "🖼️"
                        st.write(f"{doc_icon} **{doc.get('name', 'Document')}**")
                        st.caption(doc.get('document_type', 'Other'))
                    
                    with col2:
                        upload_date = doc.get('uploaded_at', 'N/A')
                        st.write(f"Uploaded: {upload_date[:10] if upload_date != 'N/A' else 'N/A'}")
                    
                    with col3:
                        status = doc.get('verification_status', 'pending')
                        if status == 'verified':
                            st.success("✓ Verified")
                        elif status == 'rejected':
                            st.error("✗ Rejected")
                        else:
                            st.warning("⏳ Pending")
                    
                    with col4:
                        if st.button("View", key=f"view_{doc.get('id')}"):
                            view_document(doc)
                        if st.button("Delete", key=f"delete_{doc.get('id')}"):
                            delete_document(doc.get('id'))
                    
                    if doc.get('verification_status') == 'rejected' and doc.get('rejection_reason'):
                        st.error(f"Rejection Reason: {doc.get('rejection_reason')}")
                    
                    st.divider()
        else:
            show_info("No documents uploaded yet")
    
    except Exception as e:
        show_error(f"Error loading documents: {str(e)}")


def show_upload_form():
    """Show document upload form"""
    st.subheader("Upload New Document")
    
    with st.form("upload_document_form"):
        document_type = st.selectbox(
            "Document Type *",
            [
                "10th Marksheet",
                "12th Marksheet",
                "Transfer Certificate",
                "Character Certificate",
                "Aadhar Card",
                "Photo",
                "Signature",
                "Caste Certificate",
                "Income Certificate",
                "Other"
            ]
        )
        
        if document_type == "Other":
            custom_type = st.text_input("Specify Document Type")
            document_type = custom_type if custom_type else "Other"
        
        uploaded_file = st.file_uploader(
            "Select File *",
            type=['pdf', 'jpg', 'jpeg', 'png'],
            help="Accepted formats: PDF, JPG, PNG (Max 5MB)"
        )
        
        description = st.text_area(
            "Description (optional)",
            placeholder="Add any notes about this document..."
        )
        
        submitted = st.form_submit_button("Upload Document", type="primary")
        
        if submitted:
            if not uploaded_file:
                show_error("Please select a file to upload")
            else:
                # Validate file
                is_valid, message = validate_file(uploaded_file)
                if not is_valid:
                    show_error(message)
                else:
                    upload_document(document_type, uploaded_file, description)


def upload_document(document_type, file, description):
    """Upload document to server"""
    try:
        student_id = st.session_state.user.get("id")
        
        # Upload file
        file_url = upload_file(file, f"students/{student_id}/documents")
        
        # Create document record
        response = api_client.post("/api/students/documents", {
            "student_id": student_id,
            "document_type": document_type,
            "file_url": file_url,
            "file_name": file.name,
            "description": description
        })
        
        show_success("Document uploaded successfully!")
        st.balloons()
        st.rerun()
    
    except Exception as e:
        show_error(f"Error uploading document: {str(e)}")


def view_document(doc):
    """View document"""
    try:
        file_url = doc.get('file_url')
        if file_url:
            st.info(f"Opening document: {doc.get('name')}")
            # In production, this would open the document
            st.write(f"Document URL: {file_url}")
        else:
            show_error("Document URL not available")
    except Exception as e:
        show_error(f"Error viewing document: {str(e)}")


def delete_document(doc_id):
    """Delete document"""
    try:
        api_client.delete(f"/api/students/documents/{doc_id}")
        show_success("Document deleted successfully!")
        st.rerun()
    except Exception as e:
        show_error(f"Error deleting document: {str(e)}")
