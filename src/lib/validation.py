"""Validation utilities for EMIS."""
import re
from datetime import date, datetime
from typing import Optional
from uuid import UUID


class ValidationError(Exception):
    """Custom validation error."""
    pass


def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """Validate phone number format."""
    # Remove common separators
    phone = re.sub(r'[-\s\(\)]', '', phone)
    # Check if it's 10-15 digits
    return bool(re.match(r'^\+?\d{10,15}$', phone))


def validate_student_number(student_number: str) -> bool:
    """Validate student number format."""
    # Example format: STU2024001
    return bool(re.match(r'^STU\d{7}$', student_number))


def validate_employee_number(employee_number: str) -> bool:
    """Validate employee number format."""
    # Example format: EMP2024001
    return bool(re.match(r'^EMP\d{7}$', employee_number))


def validate_isbn(isbn: str) -> bool:
    """Validate ISBN format (ISBN-10 or ISBN-13)."""
    isbn = re.sub(r'[-\s]', '', isbn)
    
    # ISBN-10
    if len(isbn) == 10:
        if not isbn[:-1].isdigit():
            return False
        total = sum((i + 1) * int(digit) for i, digit in enumerate(isbn[:-1]))
        check = (11 - (total % 11)) % 11
        return isbn[-1] == str(check) or (check == 10 and isbn[-1].upper() == 'X')
    
    # ISBN-13
    elif len(isbn) == 13:
        if not isbn.isdigit():
            return False
        total = sum(int(digit) * (1 if i % 2 == 0 else 3) for i, digit in enumerate(isbn[:-1]))
        check = (10 - (total % 10)) % 10
        return int(isbn[-1]) == check
    
    return False


def validate_age_range(date_of_birth: date, min_age: int = 16, max_age: int = 100) -> bool:
    """Validate if age is within acceptable range."""
    today = date.today()
    age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    return min_age <= age <= max_age


def validate_academic_year(academic_year: str) -> bool:
    """Validate academic year format (e.g., 2024-2025)."""
    pattern = r'^\d{4}-\d{4}$'
    if not re.match(pattern, academic_year):
        return False
    
    start, end = academic_year.split('-')
    return int(end) == int(start) + 1


def validate_gpa(gpa: float) -> bool:
    """Validate GPA value (0.0 to 4.0)."""
    return 0.0 <= gpa <= 4.0


def validate_percentage(percentage: float) -> bool:
    """Validate percentage value (0 to 100)."""
    return 0 <= percentage <= 100


def validate_uuid(value: str) -> bool:
    """Validate UUID format."""
    try:
        UUID(value)
        return True
    except (ValueError, AttributeError):
        return False


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent directory traversal."""
    # Remove path separators and special characters
    return re.sub(r'[^\w\s.-]', '', filename).strip()


def validate_password_strength(password: str) -> tuple[bool, Optional[str]]:
    """
    Validate password strength.
    
    Requirements:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    
    return True, None


def validate_date_range(start_date: date, end_date: date) -> bool:
    """Validate that start date is before end date."""
    return start_date < end_date


def validate_working_hours(start_time: datetime, end_time: datetime) -> bool:
    """Validate working hours (between 6 AM and 10 PM)."""
    return 6 <= start_time.hour < 22 and 6 <= end_time.hour <= 22 and start_time < end_time
