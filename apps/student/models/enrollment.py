from django.db import models
from . import Student
from . import BaseModel

class Enrollment(BaseModel):
    ENROLLMENT_STATUS_ENROLLED = 'enrolled'
    ENROLLMENT_STATUS_WAITLISTED = 'waitlisted'
    ENROLLMENT_STATUS_COMPLETED = 'completed'
    ENROLLMENT_STATUS_DROPPED = 'dropped'
    ENROLLMENT_STATUS_REPEATED = 'repeated'
    ENROLLMENT_STATUS_CHOICES = [
        (ENROLLMENT_STATUS_ENROLLED, 'Enrolled'),
        (ENROLLMENT_STATUS_WAITLISTED, 'Waitlisted'),
        (ENROLLMENT_STATUS_COMPLETED, 'Completed'),
        (ENROLLMENT_STATUS_DROPPED, 'Dropped'),
        (ENROLLMENT_STATUS_REPEATED, 'Repeated'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    program = models.CharField(max_length=100)
    batch = models.CharField(max_length=6)
    section = models.CharField(max_length=10)
    semester = models.CharField(max_length=20)
    enrollment_date = models.DateField()
    status = models.CharField(max_length=20, choices=ENROLLMENT_STATUS_CHOICES, default=ENROLLMENT_STATUS_ENROLLED)
    
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

