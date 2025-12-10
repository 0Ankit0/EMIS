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
