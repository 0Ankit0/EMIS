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
    HTML = 'html', 'HTML'
    JSON = 'json', 'JSON'


class ReportTemplate(TimeStampedModel):
    """
    Report template definitions
    """
    name = models.CharField(max_length=200, unique=True)
    code = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    category = models.CharField(
        max_length=50,
        choices=ReportCategory.choices,
        default=ReportCategory.CUSTOM
    )
    
    # Query and data configuration
    query_sql = models.TextField(
        blank=True,
        help_text="SQL query for data retrieval"
    )
    data_source = models.CharField(
        max_length=100,
        blank=True,
        help_text="Python path to data source function"
    )
    
    # Template configuration
    template_file = models.FileField(
        upload_to='report_templates/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['html', 'jinja2'])]
    )
    template_content = models.TextField(
        blank=True,
        help_text="Template content for report generation"
    )
    
    # Parameters
    parameters = models.JSONField(
        default=dict,
        help_text="Report parameters definition"
    )
    
    # Formatting
    supported_formats = models.JSONField(
        default=list,
        help_text="List of supported output formats"
    )
    default_format = models.CharField(
        max_length=20,
        choices=ReportFormat.choices,
        default=ReportFormat.PDF
    )
    
    # Layout settings
    page_size = models.CharField(
        max_length=20,
        default='A4',
        choices=[
            ('A4', 'A4'),
            ('Letter', 'Letter'),
            ('Legal', 'Legal'),
        ]
    )
    orientation = models.CharField(
        max_length=20,
        default='portrait',
        choices=[
            ('portrait', 'Portrait'),
            ('landscape', 'Landscape'),
        ]
    )
    
    # Access control
    roles_allowed = models.JSONField(
        default=list,
        help_text="User roles allowed to generate this report"
    )
    is_public = models.BooleanField(default=False)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_scheduled = models.BooleanField(
        default=False,
        help_text="Can this report be scheduled"
    )
    
    # Metadata
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_report_templates'
    )
    
    objects = ReportTemplateManager()
    
    class Meta:
        db_table = 'report_templates'
        ordering = ['category', 'name']
        verbose_name = 'Report Template'
        verbose_name_plural = 'Report Templates'
    
    def __str__(self):
        return self.name


class GeneratedReport(TimeStampedModel):
    """
    Generated reports history
    """
    template = models.ForeignKey(
        ReportTemplate,
        on_delete=models.CASCADE,
        related_name='generated_reports'
    )
    
    # Report details
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Generation info
    generated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='generated_reports'
    )
    generated_at = models.DateTimeField(auto_now_add=True)
    
    # Parameters used
    parameters = models.JSONField(
        default=dict,
        help_text="Parameters used for generation"
    )
    
    # Output
    format = models.CharField(
        max_length=20,
        choices=ReportFormat.choices,
        default=ReportFormat.PDF
    )
    file = models.FileField(
        upload_to='generated_reports/%Y/%m/',
        null=True,
        blank=True
    )
    file_size = models.BigIntegerField(default=0, help_text="File size in bytes")
    
    # Generation status
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
        ],
        default='pending'
    )
    error_message = models.TextField(blank=True)
    
    # Metadata
    record_count = models.IntegerField(default=0)
    generation_time = models.FloatField(
        default=0,
        help_text="Generation time in seconds"
    )
    
    # Access tracking
    download_count = models.IntegerField(default=0)
    last_downloaded_at = models.DateTimeField(null=True, blank=True)
    
    # Expiry
    expires_at = models.DateTimeField(null=True, blank=True)
    is_archived = models.BooleanField(default=False)
    
    objects = GeneratedReportManager()
    
    class Meta:
        db_table = 'generated_reports'
        ordering = ['-generated_at']
        verbose_name = 'Generated Report'
        verbose_name_plural = 'Generated Reports'
        indexes = [
            models.Index(fields=['template', '-generated_at']),
            models.Index(fields=['generated_by', '-generated_at']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.generated_at.strftime('%Y-%m-%d %H:%M')}"


class ScheduledReport(TimeStampedModel):
    """
    Scheduled report generation
    """
    template = models.ForeignKey(
        ReportTemplate,
        on_delete=models.CASCADE,
        related_name='scheduled_reports'
    )
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
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
