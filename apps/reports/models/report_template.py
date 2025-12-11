from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from apps.core.models import TimeStampedModel
from .report_category import ReportCategory
from .report_format import ReportFormat
from ..managers import ReportTemplateManager

User = get_user_model()

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
    query_sql = models.TextField(
        blank=True,
        help_text="SQL query for data retrieval"
    )
    data_source = models.CharField(
        max_length=100,
        blank=True,
        help_text="Python path to data source function"
    )
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
    parameters = models.JSONField(
        default=dict,
        help_text="Report parameters definition"
    )
    supported_formats = models.JSONField(
        default=list,
        help_text="List of supported output formats"
    )
    default_format = models.CharField(
        max_length=20,
        choices=ReportFormat.choices,
        default=ReportFormat.PDF
    )
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
    roles_allowed = models.JSONField(
        default=list,
        help_text="User roles allowed to generate this report"
    )
    is_public = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_scheduled = models.BooleanField(
        default=False,
        help_text="Can this report be scheduled"
    )
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
