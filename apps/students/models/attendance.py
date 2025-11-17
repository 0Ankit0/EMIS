from django.db import models
from apps.core.models import TimeStampedModel


class AttendanceRecord(TimeStampedModel):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ]

    student = models.ForeignKey(
        'students.Student',
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )
    
    session_date = models.DateField()
    session_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    
    # Additional tracking
    marked_at = models.DateTimeField(auto_now_add=True)
    marked_by = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='marked_attendance'
    )
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'attendance_records'
        ordering = ['-session_date']
        unique_together = [['student', 'course', 'session_date']]
        indexes = [
            models.Index(fields=['student']),
            models.Index(fields=['course']),
            models.Index(fields=['session_date']),
        ]

    def __str__(self):
        return f"{self.student.user.email} - {self.course.code} - {self.session_date}: {self.status}"
