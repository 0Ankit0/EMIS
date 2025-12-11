"""Event Reminder Model"""
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import TimeStampedModel
from .event import Event

User = get_user_model()


class EventReminder(TimeStampedModel):
    """Reminder for events"""
    
    class ReminderType(models.TextChoices):
        NOTIFICATION = 'notification', 'In-App Notification'
        EMAIL = 'email', 'Email'
        SMS = 'sms', 'SMS'
        ALL = 'all', 'All Methods'
    
    class TimeUnit(models.TextChoices):
        MINUTES = 'minutes', 'Minutes'
        HOURS = 'hours', 'Hours'
        DAYS = 'days', 'Days'
        WEEKS = 'weeks', 'Weeks'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='reminders'
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='event_reminders'
    )
    
    # Reminder timing
    time_value = models.IntegerField(
        help_text="Number of time units before event"
    )
    time_unit = models.CharField(
        max_length=10,
        choices=TimeUnit.choices,
        default=TimeUnit.MINUTES
    )
    
    # Reminder method
    reminder_type = models.CharField(
        max_length=20,
        choices=ReminderType.choices,
        default=ReminderType.NOTIFICATION
    )
    
    # Status
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    # Custom message
    custom_message = models.TextField(
        blank=True,
        help_text="Optional custom reminder message"
    )
    
    class Meta:
        db_table = 'event_reminders'
        ordering = ['event', 'time_value']
        verbose_name = 'Event Reminder'
        verbose_name_plural = 'Event Reminders'
        indexes = [
            models.Index(fields=['event', 'user']),
            models.Index(fields=['is_sent']),
        ]
    
    def __str__(self):
        return f"Reminder for {self.event.title} - {self.time_value} {self.time_unit} before"
    
    def get_reminder_datetime(self):
        """Calculate when the reminder should be sent"""
        from datetime import timedelta
        
        time_deltas = {
            self.TimeUnit.MINUTES: timedelta(minutes=self.time_value),
            self.TimeUnit.HOURS: timedelta(hours=self.time_value),
            self.TimeUnit.DAYS: timedelta(days=self.time_value),
            self.TimeUnit.WEEKS: timedelta(weeks=self.time_value),
        }
        
        delta = time_deltas.get(self.time_unit, timedelta(minutes=self.time_value))
        return self.event.start_datetime - delta
