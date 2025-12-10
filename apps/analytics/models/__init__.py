"""
Analytics Models
"""
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import TimeStampedModel

User = get_user_model()


class DashboardMetric(TimeStampedModel):
    """
    Model to store calculated dashboard metrics
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    metric_key = models.CharField(max_length=100, unique=True, db_index=True)
    metric_name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, db_index=True, help_text="Category: admissions, attendance, finance, etc.")
    computed_value = models.JSONField(help_text="Computed metric data")
    is_active = models.BooleanField(default=True)
    last_computed_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'dashboard_metrics'
        ordering = ['category', 'metric_name']
        verbose_name = 'Dashboard Metric'
        verbose_name_plural = 'Dashboard Metrics'
    
    def __str__(self):
        return f"{self.metric_name} ({self.category})"


class Report(TimeStampedModel):
    """
    Model for storing generated reports
    """
    REPORT_TYPES = [
        ('admissions', 'Admissions Report'),
        ('attendance', 'Attendance Report'),
        ('academic', 'Academic Performance Report'),
        ('financial', 'Financial Report'),
        ('student', 'Student Report'),
        ('teacher', 'Teacher Report'),
        ('custom', 'Custom Report'),
    ]
    
    FORMAT_CHOICES = [
        ('pdf', 'PDF'),
        ('csv', 'CSV'),
        ('excel', 'Excel'),
        ('json', 'JSON'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    report_type = models.CharField(max_length=50, choices=REPORT_TYPES, db_index=True)
    description = models.TextField(blank=True)
    
    # Report parameters
    parameters = models.JSONField(default=dict, help_text="Report generation parameters")
    filters = models.JSONField(default=dict, help_text="Applied filters")
    
    # Generated data
    report_data = models.JSONField(default=dict, help_text="Generated report data")
    file_path = models.FileField(upload_to='reports/%Y/%m/', blank=True, null=True)
    format = models.CharField(max_length=20, choices=FORMAT_CHOICES, default='pdf')
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)
    error_message = models.TextField(blank=True)
    
    # User info
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='analytics_generated_reports')
    shared_with = models.ManyToManyField(User, blank=True, related_name='shared_reports')
    
    # Scheduling
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


class AnalyticsQuery(TimeStampedModel):
    """
    Model to store and reuse analytics queries
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    query_type = models.CharField(max_length=50, db_index=True)
    
    # Query definition
    query_config = models.JSONField(help_text="Query configuration and parameters")
    visualization_config = models.JSONField(default=dict, help_text="Chart/visualization settings")
    
    # Access control
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_queries')
    is_public = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    # Usage tracking
    usage_count = models.IntegerField(default=0)
    last_used_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'analytics_queries'
        ordering = ['-created_at']
        verbose_name = 'Analytics Query'
        verbose_name_plural = 'Analytics Queries'
    
    def __str__(self):
        return self.name
