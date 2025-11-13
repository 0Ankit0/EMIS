"""
File Upload Utilities
"""
import os
from typing import Optional, Tuple
from datetime import datetime


def save_uploaded_file(uploaded_file, upload_dir: str = "uploads", allowed_extensions: Optional[list] = None) -> Tuple[bool, str, str]:
    """
    Save uploaded file to directory
    Returns (success, message, file_path)
    """
    try:
        # Validate file extension
        if allowed_extensions:
            file_ext = uploaded_file.name.split('.')[-1].lower()
            if file_ext not in allowed_extensions:
                return False, f"File type .{file_ext} not allowed", ""
        
        # Create upload directory if not exists
        os.makedirs(upload_dir, exist_ok=True)
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        original_name = uploaded_file.name
        name, ext = os.path.splitext(original_name)
        filename = f"{name}_{timestamp}{ext}"
        
        file_path = os.path.join(upload_dir, filename)
        
        # Save file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        return True, "File uploaded successfully", file_path
    
    except Exception as e:
        return False, f"Error uploading file: {str(e)}", ""


def get_file_extension(filename: str) -> str:
    """Get file extension"""
    return filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''


def get_file_size(uploaded_file) -> int:
    """Get file size in bytes"""
    return uploaded_file.size if hasattr(uploaded_file, 'size') else len(uploaded_file.getvalue())


def is_image(filename: str) -> bool:
    """Check if file is an image"""
    image_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'webp']
    ext = get_file_extension(filename)
    return ext in image_extensions


def is_document(filename: str) -> bool:
    """Check if file is a document"""
    doc_extensions = ['pdf', 'doc', 'docx', 'txt', 'rtf', 'odt']
    ext = get_file_extension(filename)
    return ext in doc_extensions


def is_spreadsheet(filename: str) -> bool:
    """Check if file is a spreadsheet"""
    sheet_extensions = ['xls', 'xlsx', 'csv', 'ods']
    ext = get_file_extension(filename)
    return ext in sheet_extensions


def is_video(filename: str) -> bool:
    """Check if file is a video"""
    video_extensions = ['mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv', 'webm']
    ext = get_file_extension(filename)
    return ext in video_extensions


def get_mime_type(filename: str) -> str:
    """Get MIME type from filename"""
    mime_types = {
        'pdf': 'application/pdf',
        'doc': 'application/msword',
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'xls': 'application/vnd.ms-excel',
        'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'csv': 'text/csv',
        'txt': 'text/plain',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'mp4': 'video/mp4',
        'zip': 'application/zip',
    }
    
    ext = get_file_extension(filename)
    return mime_types.get(ext, 'application/octet-stream')


def sanitize_filename(filename: str) -> str:
    """Sanitize filename by removing special characters"""
    # Remove path separators
    filename = filename.replace('/', '_').replace('\\', '_')
    
    # Remove potentially dangerous characters
    dangerous_chars = '<>:"|?*'
    for char in dangerous_chars:
        filename = filename.replace(char, '_')
    
    return filename
