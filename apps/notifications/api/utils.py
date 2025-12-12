"""
Notifications API Utilities
"""
from django.contrib.auth import get_user_model
from ..models import Notification

User = get_user_model()


def send_notification(user, title, message, notification_type='info', metadata=None, channels=None):
    """
    Send a notification to a single user
    
    Args:
        user: User object
        title: Notification title
        message: Notification message
        notification_type: Type of notification
        metadata: Additional metadata
        channels: List of channels to send through
    
    Returns:
        Notification object
    """
    notification = Notification.objects.create(
        user=user,
        title=title,
        message=message,
        notification_type=notification_type,
        metadata=metadata or {},
    )
    
    # TODO: Implement actual channel delivery (email, SMS, push, etc.)
    # For now, just create the notification in database
    
    return notification


def send_bulk_notifications(user_ids, title, message, notification_type='info', metadata=None, channels=None):
    """
    Send notifications to multiple users
    
    Args:
        user_ids: List of user IDs
        title: Notification title
        message: Notification message
        notification_type: Type of notification
        metadata: Additional metadata
        channels: List of channels to send through
    
    Returns:
        List of created Notification objects
    """
    users = User.objects.filter(id__in=user_ids)
    notifications = []
    
    for user in users:
        notification = Notification.objects.create(
            user=user,
            title=title,
            message=message,
            notification_type=notification_type,
            metadata=metadata or {},
        )
        notifications.append(notification)
    
    # TODO: Implement bulk channel delivery
    
    return notifications
