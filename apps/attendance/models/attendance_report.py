import uuid
from django.db import models
from apps.core.models import TimeStampedModel
from django.contrib.auth import get_user_model

User = get_user_model()

class AttendanceReport(TimeStampedModel):
    """
    Generated attendance reports
    """
    class ReportType(models.TextChoices):
        STUDENT = 'student', 'Student Report'
        COURSE = 'course', 'Course Report'
        PROGRAM = 'program', 'Program Report'
        DAILY = 'daily', 'Daily Report'
        MONTHLY = 'monthly', 'Monthly Report'
        CUSTOM = 'custom', 'Custom Report'
    
    class Format(models.TextChoices):
        PDF = 'pdf', 'PDF'
        CSV = 'csv', 'CSV'
        EXCEL = 'excel', 'Excel'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    report_type = models.CharField(max_length=20, choices=ReportType.choices)
    format = models.CharField(max_length=10, choices=Format.choices, default=Format.PDF)
    start_date = models.DateField()
    end_date = models.DateField()
    filters = models.JSONField(default=dict, help_text="Report filter parameters")
    report_data = models.JSONField(default=dict)
    file_path = models.FileField(upload_to='reports/attendance/%Y/%m/', null=True, blank=True)
    generated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='attendance_reports'
    )
    
    class Meta:
        db_table = 'attendance_reports'
        ordering = ['-created_at']
        verbose_name = 'Attendance Report'
        verbose_name_plural = 'Attendance Reports'
    
    def __str__(self):
        return f"{self.title} ({self.start_date} to {self.end_date})"

