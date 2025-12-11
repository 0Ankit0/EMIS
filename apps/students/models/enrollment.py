"""Enrollment model for student course/program enrollment"""
import uuid
from django.db import models
from apps.core.models import TimeStampedModel


class Enrollment(TimeStampedModel):
    """Model representing student enrollment in a program"""
    
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        ACTIVE = 'active', 'Active'
        COMPLETED = 'completed', 'Completed'
        WITHDRAWN = 'withdrawn', 'Withdrawn'
        SUSPENDED = 'suspended', 'Suspended'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='enrollments')
    
    # Program/Course Information
    program = models.CharField(max_length=100, db_index=True, default='')
    batch = models.CharField(max_length=50, default='')
    section = models.CharField(max_length=10, blank=True, default='')
    
    # Enrollment Dates
    start_date = models.DateField(db_index=True)
    expected_end_date = models.DateField(null=True, blank=True)
    actual_end_date = models.DateField(null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True)
    
    # Application reference
    application = models.ForeignKey('admissions.Application', on_delete=models.SET_NULL, 
                                   null=True, blank=True, related_name='enrollments')
    
    # Additional metadata
    enrollment_data = models.JSONField(default=dict, help_text="Additional enrollment information")
    
    class Meta:
        db_table = 'enrollments'
        ordering = ['-start_date']
        unique_together = (('student', 'program', 'start_date'),)
        indexes = [
            models.Index(fields=['student', 'status']),
            models.Index(fields=['program', 'batch']),
        ]
    
    def __str__(self):
        return f"{self.student.student_id} - {self.program} ({self.batch})"
