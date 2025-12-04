from . import Enrollment
from django.db import models
from . import Student

class EnrollmentHistory(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='history')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollment_histories')
    semester = models.CharField(max_length=20)
    previous_status = models.CharField(
        max_length=20,
        choices=Enrollment.ENROLLMENT_STATUS_CHOICES
    )
    new_status = models.CharField(
        max_length=20,
        choices=Enrollment.ENROLLMENT_STATUS_CHOICES
    )
    changed_at = models.DateTimeField(auto_now_add=True)
    changed_by = models.CharField(max_length=100)

    def __str__(self):
        return f"Enrollment status changed from {self.previous_status} to {self.new_status} on {self.changed_at}"

    class Meta:
        db_table = 'enrollment_history'
        ordering = ['-changed_at']
        indexes = [
            models.Index(fields=['student', 'changed_at']),
            models.Index(fields=['enrollment']),
        ]