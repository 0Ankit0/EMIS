"""Event Category Model"""
import uuid
from django.db import models
from apps.core.models import TimeStampedModel


class EventCategory(TimeStampedModel):
    """Event Category with color coding"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    # Color coding for visual distinction
    color_code = models.CharField(
        max_length=7,
        default='#3788d8',
        help_text="Hex color code (e.g., #FF5733)"
    )
    
    # Icon
    icon = models.CharField(max_length=50, blank=True, help_text="Icon class or emoji")
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'event_categories'
        ordering = ['name']
        verbose_name = 'Event Category'
        verbose_name_plural = 'Event Categories'
    
    def __str__(self):
        return self.name
