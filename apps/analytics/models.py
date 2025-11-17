"""Analytics models"""
from django.db import models
from apps.core.models import TimeStampedModel


class DashboardMetric(TimeStampedModel):
    """
    Model for storing cached dashboard metrics
    """
    
    # Metric identification
    metric_key = models.CharField(max_length=100, unique=True, db_index=True)
    metric_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Computed value (stored as JSON for flexibility)
    computed_value = models.JSONField(default=dict)
    
    # Metadata
    last_refreshed = models.DateTimeField(auto_now=True)
    refresh_frequency = models.IntegerField(
        default=3600,
        help_text="Refresh frequency in seconds"
    )
    
    # Categorization
    category = models.CharField(
        max_length=50,
        choices=[
            ('admissions', 'Admissions'),
            ('attendance', 'Attendance'),
            ('finance', 'Finance'),
            ('courses', 'Courses'),
            ('general', 'General'),
        ],
        default='general'
    )
    
    # Status
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'analytics_dashboard_metrics'
        ordering = ['category', 'metric_key']
        indexes = [
            models.Index(fields=['metric_key']),
            models.Index(fields=['category']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.metric_key}: {self.metric_name}"
    
    def is_stale(self):
        """Check if metric needs refresh"""
        from django.utils import timezone
        from datetime import timedelta
        
        if not self.last_refreshed:
            return True
        
        threshold = timezone.now() - timedelta(seconds=self.refresh_frequency)
        return self.last_refreshed < threshold
