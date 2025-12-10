import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.core.models import TimeStampedModel

User = get_user_model()

class AttendanceRecord(TimeStampedModel):
    """
    Individual attendance record for a student in a session
    """
    class Status(models.TextChoices):
        PRESENT = 'present', 'Present'
        ABSENT = 'absent', 'Absent'
        LATE = 'late', 'Late'
        EXCUSED = 'excused', 'Excused'
        SICK_LEAVE = 'sick_leave', 'Sick Leave'
        AUTHORIZED_ABSENCE = 'authorized_absence', 'Authorized Absence'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )
    session = models.ForeignKey(
        'AttendanceSession',
        on_delete=models.CASCADE,
        related_name='records',
        null=True,
        blank=True
    )
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        related_name='attendance_records',
        null=True,
        blank=True
    )
    date = models.DateField(db_index=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PRESENT,
        db_index=True
    )
    time_in = models.TimeField(null=True, blank=True)
    time_out = models.TimeField(null=True, blank=True)
    remarks = models.TextField(blank=True)
    marked_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='marked_attendances'
    )
    marked_at = models.DateTimeField(auto_now_add=True)
    leave_document = models.FileField(
        upload_to='attendance/leave_docs/%Y/%m/',
        null=True,
        blank=True
    )
    class Meta:
        db_table = 'attendance_records'
        unique_together = ['student', 'course', 'date']
        ordering = ['-date', 'student']
        verbose_name = 'Attendance Record'
        verbose_name_plural = 'Attendance Records'
        indexes = [
            models.Index(fields=['student', 'date']),
            models.Index(fields=['course', 'date']),
            models.Index(fields=['status', 'date']),
        ]
    def __str__(self):
        return f"{self.student} - {self.course} - {self.date} ({self.status})"
    def is_present(self):
        return self.status == 'present'
    def is_late(self):
        return self.status == 'late'
    def is_absent(self):
        return self.status in ['absent', 'sick_leave']
