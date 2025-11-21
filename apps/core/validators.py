"""Custom validators for EMIS"""
import re
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _
import magic
from datetime import date


def validate_phone_number(value):
    """Validate phone number format"""
    if value:
        pattern = r'^\+?1?\d{9,15}$'
        if not re.match(pattern, value):
            raise ValidationError(
                _('Phone number must be entered in the format: "+999999999". Up to 15 digits allowed.')
            )


def validate_student_id(value):
    """Validate student ID format"""
    if value:
        pattern = r'^[A-Z]{2}\d{6}$'
        if not re.match(pattern, value):
            raise ValidationError(
                _('Student ID must be in format: XX000000 (2 letters followed by 6 digits)')
            )


def validate_file_size(file, max_size_mb=5):
    """Validate file size"""
    if file:
        max_size = max_size_mb * 1024 * 1024  # Convert to bytes
        if file.size > max_size:
            raise ValidationError(
                _(f'File size cannot exceed {max_size_mb}MB. Current size: {file.size / (1024 * 1024):.2f}MB')
            )


def validate_image_file(file):
    """Validate that file is an image"""
    if file:
        validate_file_size(file, max_size_mb=2)
        
        allowed_types = ['image/jpeg', 'image/png', 'image/jpg', 'image/gif']
        
        try:
            file_type = magic.from_buffer(file.read(2048), mime=True)
            file.seek(0)  # Reset file pointer
            
            if file_type not in allowed_types:
                raise ValidationError(
                    _('Invalid file type. Only JPEG, PNG, and GIF images are allowed.')
                )
        except Exception:
            # Fallback to extension check
            ext = file.name.split('.')[-1].lower()
            if ext not in ['jpg', 'jpeg', 'png', 'gif']:
                raise ValidationError(
                    _('Invalid file type. Only JPEG, PNG, and GIF images are allowed.')
                )


def validate_document_file(file):
    """Validate document files"""
    if file:
        validate_file_size(file, max_size_mb=5)
        
        allowed_types = [
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'image/jpeg',
            'image/png',
            'image/jpg'
        ]
        
        try:
            file_type = magic.from_buffer(file.read(2048), mime=True)
            file.seek(0)
            
            if file_type not in allowed_types:
                raise ValidationError(
                    _('Invalid file type. Only PDF, DOC, DOCX, and images are allowed.')
                )
        except Exception:
            ext = file.name.split('.')[-1].lower()
            if ext not in ['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png']:
                raise ValidationError(
                    _('Invalid file type. Only PDF, DOC, DOCX, and images are allowed.')
                )


def validate_date_not_future(value):
    """Validate that date is not in the future"""
    if value and value > date.today():
        raise ValidationError(
            _('Date cannot be in the future.')
        )


def validate_date_not_past(value):
    """Validate that date is not in the past"""
    if value and value < date.today():
        raise ValidationError(
            _('Date cannot be in the past.')
        )


def validate_gpa(value):
    """Validate GPA value"""
    if value is not None:
        if value < 0 or value > 4.0:
            raise ValidationError(
                _('GPA must be between 0 and 4.0')
            )


def validate_percentage(value):
    """Validate percentage value"""
    if value is not None:
        if value < 0 or value > 100:
            raise ValidationError(
                _('Percentage must be between 0 and 100')
            )


def validate_positive_number(value):
    """Validate that number is positive"""
    if value is not None and value < 0:
        raise ValidationError(
            _('Value must be positive')
        )


def validate_year(value):
    """Validate academic year"""
    if value is not None:
        current_year = date.today().year
        if value < 1900 or value > current_year + 10:
            raise ValidationError(
                _(f'Year must be between 1900 and {current_year + 10}')
            )


def validate_course_code(value):
    """Validate course code format"""
    if value:
        pattern = r'^[A-Z]{2,4}\d{3,4}$'
        if not re.match(pattern, value):
            raise ValidationError(
                _('Course code must be in format: XX000 or XXXX0000 (2-4 letters followed by 3-4 digits)')
            )


def validate_isbn(value):
    """Validate ISBN format"""
    if value:
        # Remove hyphens and spaces
        clean_isbn = re.sub(r'[-\s]', '', value)
        
        # Check length (ISBN-10 or ISBN-13)
        if len(clean_isbn) not in [10, 13]:
            raise ValidationError(
                _('ISBN must be 10 or 13 digits')
            )
        
        # Check if all digits (except last char of ISBN-10 can be X)
        if len(clean_isbn) == 10:
            if not (clean_isbn[:-1].isdigit() and (clean_isbn[-1].isdigit() or clean_isbn[-1] == 'X')):
                raise ValidationError(
                    _('Invalid ISBN-10 format')
                )
        elif not clean_isbn.isdigit():
            raise ValidationError(
                _('Invalid ISBN-13 format')
            )
