from django.db import models

class ReportFormat(models.TextChoices):
    """Report output formats"""
    PDF = 'pdf', 'PDF'
    EXCEL = 'excel', 'Excel'
    CSV = 'csv', 'CSV'
    HTML = 'html', 'HTML'
    JSON = 'json', 'JSON'
