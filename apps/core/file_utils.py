"""File upload and management utilities"""
import os
import uuid
from pathlib import Path
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from PIL import Image
import io


def get_upload_path(instance, filename, folder='documents'):
    """Generate upload path for files"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    
    # Organize by year and month
    from datetime import datetime
    now = datetime.now()
    year = now.strftime('%Y')
    month = now.strftime('%m')
    
    return f'{folder}/{year}/{month}/{filename}'


def handle_uploaded_file(file, folder='documents'):
    """Handle file upload and return the saved path"""
    from apps.core.validators import validate_file_size, validate_document_file
    
    # Validate file
    validate_file_size(file)
    validate_document_file(file)
    
    # Generate path
    upload_path = get_upload_path(None, file.name, folder)
    
    # Save file
    path = default_storage.save(upload_path, ContentFile(file.read()))
    
    return path


def handle_uploaded_image(file, folder='images', resize=None):
    """Handle image upload with optional resizing"""
    from apps.core.validators import validate_image_file
    
    # Validate image
    validate_image_file(file)
    
    # Open image
    img = Image.open(file)
    
    # Convert RGBA to RGB if necessary
    if img.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
        img = background
    
    # Resize if specified
    if resize:
        img.thumbnail(resize, Image.Resampling.LANCZOS)
    
    # Save to bytes
    img_io = io.BytesIO()
    img.save(img_io, format='JPEG', quality=85, optimize=True)
    img_io.seek(0)
    
    # Generate path
    filename = f"{uuid.uuid4()}.jpg"
    from datetime import datetime
    now = datetime.now()
    year = now.strftime('%Y')
    month = now.strftime('%m')
    upload_path = f'{folder}/{year}/{month}/{filename}'
    
    # Save file
    path = default_storage.save(upload_path, ContentFile(img_io.read()))
    
    return path


def create_thumbnail(image_path, size=(300, 300)):
    """Create thumbnail from image"""
    try:
        # Open original image
        full_path = os.path.join(settings.MEDIA_ROOT, image_path)
        img = Image.open(full_path)
        
        # Create thumbnail
        img.thumbnail(size, Image.Resampling.LANCZOS)
        
        # Save thumbnail
        thumb_path = image_path.replace('/images/', '/thumbnails/')
        thumb_dir = os.path.dirname(os.path.join(settings.MEDIA_ROOT, thumb_path))
        os.makedirs(thumb_dir, exist_ok=True)
        
        thumb_full_path = os.path.join(settings.MEDIA_ROOT, thumb_path)
        img.save(thumb_full_path, quality=85, optimize=True)
        
        return thumb_path
    except Exception as e:
        print(f"Error creating thumbnail: {e}")
        return image_path


def delete_file(file_path):
    """Delete a file from storage"""
    try:
        if file_path and default_storage.exists(file_path):
            default_storage.delete(file_path)
            return True
    except Exception as e:
        print(f"Error deleting file: {e}")
    return False


def get_file_size(file_path):
    """Get file size in bytes"""
    try:
        if file_path and default_storage.exists(file_path):
            return default_storage.size(file_path)
    except Exception:
        pass
    return 0


def get_file_url(file_path):
    """Get URL for a file"""
    if file_path:
        return default_storage.url(file_path)
    return None


def allowed_file(filename, allowed_extensions=None):
    """Check if file extension is allowed"""
    if allowed_extensions is None:
        allowed_extensions = {
            'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif',
            'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx'
        }
    
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def format_file_size(bytes_size):
    """Format file size to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"


class FileUploadMixin:
    """Mixin to handle file uploads in views"""
    
    def handle_file_upload(self, request, field_name, folder='documents'):
        """Handle file upload from request"""
        file = request.FILES.get(field_name)
        if file:
            return handle_uploaded_file(file, folder)
        return None
    
    def handle_image_upload(self, request, field_name, folder='images', resize=(800, 800)):
        """Handle image upload from request"""
        file = request.FILES.get(field_name)
        if file:
            return handle_uploaded_image(file, folder, resize)
        return None
    
    def handle_multiple_files(self, request, field_name, folder='documents'):
        """Handle multiple file uploads"""
        files = request.FILES.getlist(field_name)
        uploaded_paths = []
        
        for file in files:
            try:
                path = handle_uploaded_file(file, folder)
                uploaded_paths.append(path)
            except Exception as e:
                print(f"Error uploading {file.name}: {e}")
        
        return uploaded_paths
