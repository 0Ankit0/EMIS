"""
Input Validators
"""
import re
from typing import Any, Optional
from datetime import datetime


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """Validate phone number format"""
    pattern = r'^[0-9]{10}$'
    cleaned = re.sub(r'[^0-9]', '', phone)
    return bool(re.match(pattern, cleaned))


def validate_password(password: str) -> tuple[bool, str]:
    """
    Validate password strength
    Returns (is_valid, message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one digit"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    
    return True, "Password is strong"


def validate_required(value: Any, field_name: str) -> tuple[bool, str]:
    """Validate required field"""
    if value is None or (isinstance(value, str) and not value.strip()):
        return False, f"{field_name} is required"
    return True, ""


def validate_number(value: Any, min_val: Optional[float] = None, max_val: Optional[float] = None) -> tuple[bool, str]:
    """Validate numeric value with optional range"""
    try:
        num = float(value)
        if min_val is not None and num < min_val:
            return False, f"Value must be at least {min_val}"
        if max_val is not None and num > max_val:
            return False, f"Value must be at most {max_val}"
        return True, ""
    except (ValueError, TypeError):
        return False, "Invalid number"


def validate_date(date_str: str, format_str: str = "%Y-%m-%d") -> tuple[bool, str]:
    """Validate date format"""
    try:
        datetime.strptime(date_str, format_str)
        return True, ""
    except ValueError:
        return False, f"Invalid date format. Expected {format_str}"


def validate_length(value: str, min_len: Optional[int] = None, max_len: Optional[int] = None) -> tuple[bool, str]:
    """Validate string length"""
    length = len(value) if value else 0
    
    if min_len is not None and length < min_len:
        return False, f"Minimum length is {min_len} characters"
    
    if max_len is not None and length > max_len:
        return False, f"Maximum length is {max_len} characters"
    
    return True, ""


def validate_url(url: str) -> bool:
    """Validate URL format"""
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return bool(re.match(pattern, url))


def validate_alphanumeric(value: str) -> bool:
    """Validate alphanumeric string"""
    return bool(re.match(r'^[a-zA-Z0-9]+$', value))


def validate_file_extension(filename: str, allowed_extensions: list) -> tuple[bool, str]:
    """Validate file extension"""
    if '.' not in filename:
        return False, "File must have an extension"
    
    ext = filename.rsplit('.', 1)[1].lower()
    if ext not in allowed_extensions:
        return False, f"Allowed extensions: {', '.join(allowed_extensions)}"
    
    return True, ""


def validate_file_size(file_size: int, max_size_mb: int = 10) -> tuple[bool, str]:
    """Validate file size"""
    max_bytes = max_size_mb * 1024 * 1024
    if file_size > max_bytes:
        return False, f"File size must be less than {max_size_mb}MB"
    return True, ""
