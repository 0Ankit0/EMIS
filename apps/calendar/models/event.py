"""Event Model"""
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.core.models import TimeStampedModel
from .calendar import Calendar
from .category import EventCategory

User = get_user_model()


class Event(TimeStampedModel):
    """Event that can be added to calendars"""
    
    class Recurrence(models.TextChoices):
        NONE = 'none', 'Does not repeat'
        DAILY = 'daily', 'Daily'
        WEEKLY = 'weekly', 'Weekly'
        BIWEEKLY = 'biweekly', 'Biweekly'
        MONTHLY = 'monthly', 'Monthly'
        YEARLY = 'yearly', 'Yearly'
        CUSTOM = 'custom', 'Custom'
    
    class Priority(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'
        URGENT = 'urgent', 'Urgent'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Basic info
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Categorization
    category = models.ForeignKey(
        EventCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events',
        help_text="Category determines the event color"
    )
    
    # Time details
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    is_all_day = models.BooleanField(default=False)
    
    # Location
    location = models.CharField(max_length=200, blank=True)
    location_url = models.URLField(blank=True, help_text="Google Maps or meeting link")
    
    # Recurrence
    recurrence = models.CharField(
        max_length=20,
        choices=Recurrence.choices,
        default=Recurrence.NONE
    )
    recurrence_end_date = models.DateField(null=True, blank=True)
    
    # Priority
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM
    )
    
    # Association - Event can be attached to multiple calendars
    calendars = models.ManyToManyField(
        Calendar,
        related_name='events',
        help_text="Calendars this event appears in"
    )
    
    # Creator and participants
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_events'
    )
    
    attendees = models.ManyToManyField(
        User,
        blank=True,
        related_name='attending_events',
        help_text="Users invited to this event"
    )
    
    # Additional options
    send_notifications = models.BooleanField(default=True)
    is_private = models.BooleanField(default=False)
    
    # Attachments
    attachment = models.FileField(
        upload_to='calendar/attachments/%Y/%m/',
        blank=True,
        null=True
    )
    
    # Notes
    notes = models.TextField(blank=True, help_text="Internal notes")
    
    class Meta:
        db_table = 'events'
        ordering = ['start_datetime']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        indexes = [
            models.Index(fields=['start_datetime', 'end_datetime']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.start_datetime.strftime('%Y-%m-%d %H:%M')}"
    
    def get_color(self):
        """Get color from category or use default"""
        if self.category:
            return self.category.color_code
        return '#3788d8'  # Default blue
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.end_datetime <= self.start_datetime:
            raise ValidationError('End time must be after start time')
