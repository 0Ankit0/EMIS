"""
Student Profile Photo Upload Page
"""
import streamlit as st
from PIL import Image
import io
from utils.api_client import api_client
from utils.helpers import show_error, show_success
from utils.file_handler import upload_file


def show():
    """Display profile photo upload page"""
    st.title("📸 Profile Photo")
    st.markdown("### Upload and edit your profile picture")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Show current photo
        student = st.session_state.user
        photo_url = student.get('photo_url')
        
        if photo_url:
            st.image(photo_url, caption="Current Photo", width=200)
        else:
            st.info("No photo uploaded")
        
        st.divider()
        
        # Photo requirements
        st.markdown("**Requirements:**")
        st.write("- Format: JPG, PNG")
        st.write("- Max size: 2MB")
        st.write("- Recommended: 300x300px")
        st.write("- Clear, front-facing photo")
    
    with col2:
        st.subheader("Upload New Photo")
        
        uploaded_file = st.file_uploader(
            "Choose a photo",
            type=['jpg', 'jpeg', 'png'],
            help="Upload a clear photo of yourself"
        )
        
        if uploaded_file:
            # Display preview
            image = Image.open(uploaded_file)
            
            st.image(image, caption="Preview", width=300)
            
            # Show image details
            st.write(f"**Size:** {image.size[0]} x {image.size[1]} pixels")
            st.write(f"**Format:** {image.format}")
            
            # Crop options
            st.subheader("Adjust Photo")
            
            crop = st.checkbox("Enable cropping")
            
            if crop:
                col_a, col_b = st.columns(2)
                with col_a:
                    crop_size = st.slider("Crop Size", 100, min(image.size), min(image.size))
                with col_b:
                    rotation = st.slider("Rotation", 0, 360, 0)
                
                # Apply transformations
                if rotation != 0:
                    image = image.rotate(rotation, expand=True)
                
                if crop:
                    # Center crop
                    width, height = image.size
                    left = (width - crop_size) / 2
                    top = (height - crop_size) / 2
                    right = (width + crop_size) / 2
                    bottom = (height + crop_size) / 2
                    image = image.crop((left, top, right, bottom))
                    
                    st.image(image, caption="Cropped Preview", width=250)
            
            st.divider()
            
            col_x, col_y = st.columns(2)
            
            with col_x:
                if st.button("Upload Photo", type="primary", use_container_width=True):
                    upload_photo(image, uploaded_file.name)
            
            with col_y:
                if st.button("Cancel", use_container_width=True):
                    st.rerun()


def upload_photo(image, filename):
    """Upload profile photo"""
    try:
        # Convert image to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        student_id = st.session_state.user.get("id")
        
        # Upload file
        file_url = upload_file(img_byte_arr, f"students/{student_id}/photo", filename)
        
        # Update student profile
        api_client.patch(f"/api/students/{student_id}", {
            "photo_url": file_url
        })
        
        # Update session
        st.session_state.user['photo_url'] = file_url
        
        show_success("Profile photo updated successfully!")
        st.balloons()
        st.rerun()
    
    except Exception as e:
        show_error(f"Error uploading photo: {str(e)}")
