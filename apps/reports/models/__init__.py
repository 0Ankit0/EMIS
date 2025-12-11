"""
Reports Models
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from apps.core.models import TimeStampedModel
from .managers import ReportTemplateManager, GeneratedReportManager

User = get_user_model()


class ReportCategory(models.TextChoices):
    """Report categories"""
    ACADEMIC = 'academic', 'Academic'
    FINANCIAL = 'financial', 'Financial'
    ATTENDANCE = 'attendance', 'Attendance'
    STUDENT = 'student', 'Student'
    FACULTY = 'faculty', 'Faculty'
    EXAMINATION = 'examination', 'Examination'
    ADMINISTRATIVE = 'administrative', 'Administrative'
    CUSTOM = 'custom', 'Custom'


class ReportFormat(models.TextChoices):
    """Report output formats"""
    PDF = 'pdf', 'PDF'
    EXCEL = 'excel', 'Excel'
    CSV = 'csv', 'CSV'

    # Modularized reports models
    from .report_category import ReportCategory
    from .report_format import ReportFormat
    from .report_template import ReportTemplate
    from .generated_report import GeneratedReport
    
    # Schedule configuration
    schedule_type = models.CharField(
        max_length=20,
        choices=[
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
            ('quarterly', 'Quarterly'),
            ('yearly', 'Yearly'),
            ('custom', 'Custom'),
        ],
        default='daily'
    )
    cron_expression = models.CharField(
        max_length=100,
        blank=True,
        help_text="Cron expression for custom schedules"
    )
    
    # Time settings
    scheduled_time = models.TimeField()
    timezone = models.CharField(max_length=50, default='UTC')
    
    # Parameters
    parameters = models.JSONField(
        default=dict,
        help_text="Default parameters for generation"
    )
    
    # Output settings
    format = models.CharField(
        max_length=20,
        choices=ReportFormat.choices,
        default=ReportFormat.PDF
    )
    
    # Distribution
    recipients = models.ManyToManyField(
        User,
        related_name='scheduled_report_recipients',
        blank=True
    )
    recipient_emails = models.JSONField(
        default=list,
        help_text="Additional email addresses"
    )
    
    # Status
    is_active = models.BooleanField(default=True)
    last_run = models.DateTimeField(null=True, blank=True)
    next_run = models.DateTimeField(null=True, blank=True)
    
    # Created by
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_scheduled_reports'
    )
    
    class Meta:
        db_table = 'scheduled_reports'
        ordering = ['name']
        verbose_name = 'Scheduled Report'
        verbose_name_plural = 'Scheduled Reports'
    
    def __str__(self):
        return self.name


class ReportWidget(TimeStampedModel):
    """
    Dashboard widgets for quick report access
    """
    name = models.CharField(max_length=100)
    template = models.ForeignKey(
        ReportTemplate,
        on_delete=models.CASCADE,
        related_name='widgets'
    )
    
    # Widget configuration
    widget_type = models.CharField(
        max_length=50,
        choices=[
            ('chart', 'Chart'),
            ('table', 'Table'),
            ('card', 'Card'),
            ('list', 'List'),
        ],
        default='card'
    )
    config = models.JSONField(
        default=dict,
        help_text="Widget display configuration"
    )
    
    # Default parameters
    default_parameters = models.JSONField(default=dict)
    
    # Layout
    order = models.IntegerField(default=0)
    width = models.IntegerField(
        default=6,
        help_text="Width in grid columns (1-12)"
    )
    
    # Access
    roles_allowed = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'report_widgets'
        ordering = ['order', 'name']
        verbose_name = 'Report Widget'
        verbose_name_plural = 'Report Widgets'
    
    def __str__(self):
        return self.name


class ReportFavorite(TimeStampedModel):
    """
    User's favorite reports
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_reports'
    )
    template = models.ForeignKey(
        ReportTemplate,
        on_delete=models.CASCADE,
        related_name='favorited_by'
    )
    
    # Custom settings
    custom_parameters = models.JSONField(
        default=dict,
        help_text="User's preferred parameters"
    )
    
    class Meta:
        db_table = 'report_favorites'
        unique_together = ['user', 'template']
        verbose_name = 'Report Favorite'
        verbose_name_plural = 'Report Favorites'
    
    def __str__(self):
        return f"{self.user.username} - {self.template.name}"


class ReportAccessLog(TimeStampedModel):
    """
    Log of report generation and access
    """
    template = models.ForeignKey(
        ReportTemplate,
        on_delete=models.CASCADE,
        related_name='access_logs'
    )
    generated_report = models.ForeignKey(
        GeneratedReport,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='access_logs'
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='report_access_logs'
    )
    
    action = models.CharField(
        max_length=50,
        choices=[
            ('generate', 'Generate'),
            ('view', 'View'),
            ('download', 'Download'),
            ('delete', 'Delete'),
        ]
    )
    
    # Request info
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    # Additional metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'report_access_logs'
        ordering = ['-created_at']
        verbose_name = 'Report Access Log'
        verbose_name_plural = 'Report Access Logs'
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['template', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username if self.user else 'Anonymous'} - {self.action} - {self.template.name}"
