"""Services module"""
from .auth_service import auth_service
from .student_service import student_service
from .faculty_service import faculty_service

__all__ = ['auth_service', 'student_service', 'faculty_service']
