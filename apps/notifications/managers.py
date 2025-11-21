"""
Notifications Custom Managers and QuerySets
"""
from django.db import models
from django.utils import timezone


class NotificationQuerySet(models.QuerySet):
    """Custom queryset for Notification"""
    
    def unread(self):
        """Get unread notifications"""
        return self.filter(is_read=False)
    
    def read(self):
        """Get read notifications"""
        return self.filter(is_read=True)
    
    def for_user(self, user):
        """Get notifications for specific user"""
        return self.filter(recipient=user)
    
    def by_type(self, notification_type):
        """Get notifications by type"""
        return self.filter(notification_type=notification_type)
    
    def not_expired(self):
        """Get non-expired notifications"""
        now = timezone.now()
        return self.filter(
            models.Q(expires_at__isnull=True) | models.Q(expires_at__gt=now)
        )
    
    def mark_all_as_read(self):
        """Mark all notifications in queryset as read"""
        return self.update(is_read=True, read_at=timezone.now())


class NotificationManager(models.Manager):
    """Custom manager for Notification"""
    
    def get_queryset(self):
        return NotificationQuerySet(self.model, using=self._db)
    
    def unread(self):
        return self.get_queryset().unread()
    
    def read(self):
        return self.get_queryset().read()
    
    def for_user(self, user):
        return self.get_queryset().for_user(user)
    
    def by_type(self, notification_type):
        return self.get_queryset().by_type(notification_type)
    
    def not_expired(self):
        return self.get_queryset().not_expired()
    
    def create_notification(self, recipient, title, message, **kwargs):
        """
        Create a new notification
        
        Args:
            recipient: User to receive notification
            title: Notification title
            message: Notification message
            **kwargs: Additional fields
        """
        return self.create(
            recipient=recipient,
            title=title,
            message=message,
            **kwargs
        )
    
    def bulk_create_notifications(self, recipients, title, message, **kwargs):
        """
        Create notifications for multiple recipients
        
        Args:
            recipients: List of users
            title: Notification title
            message: Notification message
            **kwargs: Additional fields
        """
        notifications = [
            self.model(
                recipient=recipient,
                title=title,
                message=message,
                **kwargs
            )
            for recipient in recipients
        ]
        return self.bulk_create(notifications)


class NotificationTemplateQuerySet(models.QuerySet):
    """Custom queryset for NotificationTemplate"""
    
    def active(self):
        """Get active templates"""
        return self.filter(is_active=True)
    
    def by_code(self, code):
        """Get template by code"""
        return self.filter(code=code).first()


class NotificationTemplateManager(models.Manager):
    """Custom manager for NotificationTemplate"""
    
    def get_queryset(self):
        return NotificationTemplateQuerySet(self.model, using=self._db)
    
    def active(self):
        return self.get_queryset().active()
    
    def by_code(self, code):
        return self.get_queryset().by_code(code)
