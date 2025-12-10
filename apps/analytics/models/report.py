import uuid
from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import TimeStampedModel

User = get_user_model()

class Report(TimeStampedModel):
    """
    Model for storing generated reports
    """
    
    class ReportType(models.TextChoices):
        ADMISSIONS = 'admissions', 'Admissions Report'
        ATTENDANCE = 'attendance', 'Attendance Report'
        ACADEMIC = 'academic', 'Academic Performance Report'
        FINANCIAL = 'financial', 'Financial Report'
        STUDENT = 'student', 'Student Report'
        TEACHER = 'teacher', 'Teacher Report'
        CUSTOM = 'custom', 'Custom Report'
    
    class Format(models.TextChoices):
        PDF = 'pdf', 'PDF'
        CSV = 'csv', 'CSV'
        EXCEL = 'excel', 'Excel'
        JSON = 'json', 'JSON'
    
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PROCESSING = 'processing', 'Processing'
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    report_type = models.CharField(max_length=50, choices=ReportType.choices, db_index=True)
    description = models.TextField(blank=True)
    parameters = models.JSONField(default=dict, help_text="Report generation parameters")
    filters = models.JSONField(default=dict, help_text="Applied filters")
    report_data = models.JSONField(default=dict, help_text="Generated report data")
    file_path = models.FileField(upload_to='reports/%Y/%m/', blank=True, null=True)
    format = models.CharField(max_length=20, choices=Format.choices, default=Format.PDF)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True)
    error_message = models.TextField(blank=True)
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='analytics_generated_reports')
    shared_with = models.ManyToManyField(User, blank=True, related_name='shared_reports')
    is_scheduled = models.BooleanField(default=False)
    schedule_frequency = models.CharField(max_length=50, blank=True, help_text="daily, weekly, monthly")
    next_run = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'analytics_reports'
        ordering = ['-created_at']
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'
    
    def __str__(self):
        return f"{self.title} - {self.get_report_type_display()}"

