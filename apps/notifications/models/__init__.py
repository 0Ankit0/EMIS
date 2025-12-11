"""
Notifications Models
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from apps.core.models import TimeStampedModel

# Modularized notifications models
from .notification_type import NotificationType
from .notification_channel import NotificationChannel
from .notification import Notification
from .notification_template import NotificationTemplate
from .notification_preference import NotificationPreference
    class Meta:
        db_table = 'notification_preferences'
        verbose_name = 'Notification Preference'
        verbose_name_plural = 'Notification Preferences'
    
    def __str__(self):
        return f"Preferences for {self.user.get_full_name()}"


class ScheduledNotification(TimeStampedModel):
    """
    Scheduled notifications to be sent at a specific time
    """
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(
        max_length=20,
        choices=NotificationType.choices,
        default=NotificationType.INFO
    )
    
    # Recipients
    recipients = models.ManyToManyField(User, related_name='scheduled_notifications')
    recipient_groups = models.JSONField(
        default=list,
        help_text="List of user groups to notify"
    )
    
    # Scheduling
    scheduled_for = models.DateTimeField()
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    # Delivery
    channels = models.JSONField(default=list)
    action_url = models.URLField(max_length=500, blank=True)
    
    # Template
    template = models.ForeignKey(
        NotificationTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='scheduled_notifications'
    )
    template_context = models.JSONField(default=dict, blank=True)
    
    # Recurrence
    is_recurring = models.BooleanField(default=False)
    recurrence_pattern = models.CharField(
        max_length=20,
        choices=[
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
        ],
        blank=True
    )
    
    # Status
    is_active = models.BooleanField(default=True)
    
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_scheduled_notifications'
    )
    
    class Meta:
        db_table = 'scheduled_notifications'
        ordering = ['scheduled_for']
        verbose_name = 'Scheduled Notification'
        verbose_name_plural = 'Scheduled Notifications'
    
    def __str__(self):
        return f"{self.title} - {self.scheduled_for}"


class NotificationLog(TimeStampedModel):
    """
    Log of all notification deliveries
    """
    notification = models.ForeignKey(
        Notification,
        on_delete=models.CASCADE,
        related_name='logs'
    )
    channel = models.CharField(max_length=20, choices=NotificationChannel.choices)
    
    # Delivery status
    is_successful = models.BooleanField(default=False)
    error_message = models.TextField(blank=True)
    
    # Additional data
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'notification_logs'
        ordering = ['-created_at']
        verbose_name = 'Notification Log'
        verbose_name_plural = 'Notification Logs'
    
    def __str__(self):
        return f"{self.notification.title} - {self.channel}"
