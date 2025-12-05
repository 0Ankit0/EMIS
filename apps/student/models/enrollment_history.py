from . import EnrollmentStatus, Enrollment
from django.db import models
from . import Student
from . import BaseModel


class EnrollmentHistory(BaseModel):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='history')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollment_histories')
    semester = models.CharField(max_length=20)
    previous_status = models.CharField(
        max_length=20,
        choices=EnrollmentStatus.choices
    )
    new_status = models.CharField(
        max_length=20,
        choices=EnrollmentStatus.choices
    )
    def __str__(self):
        return f"Enrollment status changed from {self.previous_status} to {self.new_status} on {self.created_at} for {self.student.first_name} {self.student.last_name}"

    class Meta: # type: ignore
        db_table = 'enrollment_history'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['student', 'created_at']),
            models.Index(fields=['enrollment']),
        ]