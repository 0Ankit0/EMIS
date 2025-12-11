from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import TimeStampedModel
from .report_template import ReportTemplate
from .report_format import ReportFormat
from ..managers import GeneratedReportManager

User = get_user_model()

class GeneratedReport(TimeStampedModel):
    """
    Generated reports history
    """
    template = models.ForeignKey(
        ReportTemplate,
        on_delete=models.CASCADE,
        related_name='generated_reports'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    generated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='reports_generated_reports'
    )
    generated_at = models.DateTimeField(auto_now_add=True)
    parameters = models.JSONField(
        default=dict,
        help_text="Parameters used for generation"
    )
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
    record_count = models.IntegerField(default=0)
    generation_time = models.FloatField(
        default=0,
        help_text="Generation time in seconds"
    )
    class Meta:
        db_table = 'generated_reports'
        ordering = ['-generated_at']
        verbose_name = 'Generated Report'
        verbose_name_plural = 'Generated Reports'
    def __str__(self):
        return self.title
