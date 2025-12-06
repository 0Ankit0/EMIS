from django.db import models
from .student import Student
from .base import BaseModel

class EnrollmentStatus(models.TextChoices):
    """Enrollment status choices."""
    ENROLLED = 'enrolled', 'Enrolled'
    COMPLETED = 'completed', 'Completed'
    DROPPED = 'dropped', 'Dropped'
    SUSPENDED = 'suspended', 'Suspended'

class Enrollment(BaseModel):
    """Model representing a student's enrollment in a program."""

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    program = models.CharField(max_length=100)
    batch = models.CharField(max_length=6)
    section = models.CharField(max_length=10)
    semester = models.CharField(max_length=20)
    enrollment_date = models.DateField()
    status = models.CharField(max_length=20, choices=EnrollmentStatus.choices, default=EnrollmentStatus.ENROLLED)
    
    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name} enrolled in {self.program} ({self.semester})"
    
    class Meta: # type: ignore
        db_table = 'enrollments'
        ordering = ['-enrollment_date']
        unique_together = [['student', 'program', 'semester']]
        indexes = [
            models.Index(fields=['program', 'batch']),
            models.Index(fields=['student','status']),
        ]

