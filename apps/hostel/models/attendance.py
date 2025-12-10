from django.db import models
from django.utils import timezone
from apps.core.models import TimeStampedModel
from django.contrib.auth import get_user_model

User = get_user_model()

class Attendance(TimeStampedModel):
    """Hostel Attendance"""
    class Status(models.TextChoices):
        PRESENT = 'present', 'Present'
        ABSENT = 'absent', 'Absent'
        ON_LEAVE = 'on_leave', 'On Leave'
    
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='hostel_attendance')
    hostel = models.ForeignKey('hostel.Hostel', on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField(db_index=True)
    status = models.CharField(max_length=20, choices=Status.choices)
    marked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='marked_hostel_attendance')
    marked_at = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True)
    
    class Meta:
        db_table = 'hostel_attendance'
        unique_together = ['student', 'date']
        ordering = ['-date']
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance Records'
        indexes = [
            models.Index(fields=['hostel', 'date']),
            models.Index(fields=['student', 'date']),
        ]
    
    def __str__(self):
        return f"{self.student.user.email} - {self.date} - {self.status}"

