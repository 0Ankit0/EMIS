import uuid
from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import TimeStampedModel

User = get_user_model()

class AnalyticsQuery(TimeStampedModel):
    """
    Model to store and reuse analytics queries
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    query_type = models.CharField(max_length=50, db_index=True)
    query_config = models.JSONField(help_text="Query configuration and parameters")
    visualization_config = models.JSONField(default=dict, help_text="Chart/visualization settings")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_queries')
    is_public = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    usage_count = models.IntegerField(default=0)
    last_used_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'analytics_queries'
        ordering = ['-created_at']
        verbose_name = 'Analytics Query'
        verbose_name_plural = 'Analytics Queries'
    def __str__(self):
        return self.name
