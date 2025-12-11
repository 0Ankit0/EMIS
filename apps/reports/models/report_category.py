from django.db import models

class ReportCategory(models.TextChoices):
    """Report categories"""
    ACADEMIC = 'academic', 'Academic'
    FINANCIAL = 'financial', 'Financial'
    ATTENDANCE = 'attendance', 'Attendance'
    STUDENT = 'student', 'Student'
    FACULTY = 'faculty', 'Faculty'
    EXAMINATION = 'examination', 'Examination'
    ADMINISTRATIVE = 'administrative', 'Administrative'
    CUSTOM = 'custom', 'Custom'
