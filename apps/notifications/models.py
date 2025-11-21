"""
Notifications Models
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from apps.core.models import TimeStampedModel
from .managers import NotificationManager, NotificationTemplateManager

User = get_user_model()


class NotificationType(models.TextChoices):
    """Notification types"""
    INFO = 'info', 'Information'
    SUCCESS = 'success', 'Success'
    WARNING = 'warning', 'Warning'
    ERROR = 'error', 'Error'
    ANNOUNCEMENT = 'announcement', 'Announcement'
    REMINDER = 'reminder', 'Reminder'


class NotificationChannel(models.TextChoices):
    """Notification delivery channels"""
    IN_APP = 'in_app', 'In-App'
    EMAIL = 'email', 'Email'
    SMS = 'sms', 'SMS'
    PUSH = 'push', 'Push Notification'


class Notification(TimeStampedModel):
    """
    Main notification model
    """
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications_received'
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notifications_sent'
    )
    
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(
        max_length=20,
        choices=NotificationType.choices,
        default=NotificationType.INFO
    )
    
    # Generic relation to any model
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # URL to redirect when clicked
    action_url = models.URLField(max_length=500, blank=True)
    
    # Status
    is_read = models.BooleanField(default=False, db_index=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Delivery channels
    channels = models.JSONField(default=list, help_text="List of delivery channels")
    
    # Email specific
    email_sent = models.BooleanField(default=False)
    email_sent_at = models.DateTimeField(null=True, blank=True)
    
    # SMS specific
    sms_sent = models.BooleanField(default=False)
    sms_sent_at = models.DateTimeField(null=True, blank=True)
    
    # Push notification specific
    push_sent = models.BooleanField(default=False)
    push_sent_at = models.DateTimeField(null=True, blank=True)
    
    # Additional data
    metadata = models.JSONField(default=dict, blank=True)
    
    # Expiry
    expires_at = models.DateTimeField(null=True, blank=True)
    
    objects = NotificationManager()
    
    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['created_at']),
            models.Index(fields=['notification_type']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.recipient.get_full_name()}"
    
    def mark_as_read(self):
        """Mark notification as read"""
        from django.utils import timezone
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])
    
    def mark_as_unread(self):
        """Mark notification as unread"""
        if self.is_read:
            self.is_read = False
            self.read_at = None
            self.save(update_fields=['is_read', 'read_at'])


class NotificationTemplate(TimeStampedModel):
    """
    Reusable notification templates
    """
    name = models.CharField(max_length=100, unique=True)
    code = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    # Template content
    title_template = models.CharField(max_length=255)
    message_template = models.TextField()
    
    # Default settings
    notification_type = models.CharField(
        max_length=20,
        choices=NotificationType.choices,
        default=NotificationType.INFO
    )
    default_channels = models.JSONField(
        default=list,
        help_text="Default delivery channels"
    )
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Variables used in template
    template_variables = models.JSONField(
        default=list,
        help_text="List of variables used in template"
    )
    
    objects = NotificationTemplateManager()
    
    class Meta:
        db_table = 'notification_templates'
        ordering = ['name']
        verbose_name = 'Notification Template'
        verbose_name_plural = 'Notification Templates'
    
    def __str__(self):
        return self.name
    
    def render(self, context):
        """Render template with context data"""
        from django.template import Template, Context
        
        title = Template(self.title_template).render(Context(context))
        message = Template(self.message_template).render(Context(context))
        
        return {
            'title': title,
            'message': message,
            'notification_type': self.notification_type,
            'channels': self.default_channels,
        }


class NotificationPreference(TimeStampedModel):
    """
    User notification preferences
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='notification_preference'
    )
    
    # Channel preferences
    enable_email = models.BooleanField(default=True)
    enable_sms = models.BooleanField(default=False)
    enable_push = models.BooleanField(default=True)
    enable_in_app = models.BooleanField(default=True)
    
    # Notification type preferences
    notification_types = models.JSONField(
        default=dict,
        help_text="Preferences for each notification type"
    )
    
    # Quiet hours
    quiet_hours_enabled = models.BooleanField(default=False)
    quiet_hours_start = models.TimeField(null=True, blank=True)
    quiet_hours_end = models.TimeField(null=True, blank=True)
    
    # Digest preferences
    enable_daily_digest = models.BooleanField(default=False)
    daily_digest_time = models.TimeField(null=True, blank=True)
    
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
