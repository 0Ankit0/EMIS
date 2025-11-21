"""
Celery Tasks for Notifications App

These tasks can be used with Celery for async notification processing
"""
from celery import shared_task
from django.utils import timezone
from .utils import (
    send_notification, send_bulk_notifications, send_notification_from_template,
    process_scheduled_notifications, cleanup_old_notifications
)
from .models import Notification, ScheduledNotification


@shared_task
def send_notification_task(recipient_id, title, message, **kwargs):
    """
    Async task to send a notification
    
    Args:
        recipient_id: User ID of recipient
        title: Notification title
        message: Notification message
        **kwargs: Additional notification fields
    
    Returns:
        int: Notification ID
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    try:
        recipient = User.objects.get(id=recipient_id)
        notification = send_notification(
            recipient=recipient,
            title=title,
            message=message,
            **kwargs
        )
        return notification.id
    except User.DoesNotExist:
        return None


@shared_task
def send_bulk_notifications_task(recipient_ids, title, message, **kwargs):
    """
    Async task to send bulk notifications
    
    Args:
        recipient_ids: List of user IDs
        title: Notification title
        message: Notification message
        **kwargs: Additional notification fields
    
    Returns:
        int: Number of notifications sent
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    recipients = User.objects.filter(id__in=recipient_ids)
    count = send_bulk_notifications(
        recipients=recipients,
        title=title,
        message=message,
        **kwargs
    )
    return count


@shared_task
def send_template_notification_task(template_code, recipient_id, context):
    """
    Async task to send notification from template
    
    Args:
        template_code: Template code
        recipient_id: User ID of recipient
        context: Template context data
    
    Returns:
        int: Notification ID
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    try:
        recipient = User.objects.get(id=recipient_id)
        notification = send_notification_from_template(
            template_code=template_code,
            recipient=recipient,
            context=context
        )
        return notification.id
    except User.DoesNotExist:
        return None


@shared_task
def process_scheduled_notifications_task():
    """
    Periodic task to process scheduled notifications
    Should be run via Celery Beat
    
    Returns:
        int: Number of notifications processed
    """
    count = process_scheduled_notifications()
    return count


@shared_task
def cleanup_old_notifications_task(days=30):
    """
    Periodic task to cleanup old notifications
    Should be run via Celery Beat
    
    Args:
        days: Number of days to keep notifications
    
    Returns:
        int: Number of notifications deleted
    """
    count = cleanup_old_notifications(days=days)
    return count


@shared_task
def send_daily_digest_task():
    """
    Send daily digest to users who have enabled it
    Should be run via Celery Beat
    
    Returns:
        int: Number of digests sent
    """
    from django.contrib.auth import get_user_model
    from .models import NotificationPreference
    from datetime import datetime
    
    User = get_user_model()
    current_time = timezone.now().time()
    
    # Find users with daily digest enabled at this time
    preferences = NotificationPreference.objects.filter(
        enable_daily_digest=True,
        daily_digest_time__hour=current_time.hour
    )
    
    count = 0
    for preference in preferences:
        user = preference.user
        
        # Get unread notifications
        unread = Notification.objects.for_user(user).unread()
        
        if unread.exists():
            # Create digest message
            message = f"You have {unread.count()} unread notifications:\n\n"
            for notification in unread[:10]:  # Limit to 10
                message += f"- {notification.title}\n"
            
            # Send digest
            send_notification(
                recipient=user,
                title="Daily Notification Digest",
                message=message,
                notification_type='info',
                channels=['email']
            )
            count += 1
    
    return count


@shared_task
def send_email_notification_task(notification_id):
    """
    Async task to send email notification
    
    Args:
        notification_id: Notification ID
    
    Returns:
        bool: Success status
    """
    from .utils import send_email_notification
    
    try:
        notification = Notification.objects.get(id=notification_id)
        send_email_notification(notification)
        return True
    except Notification.DoesNotExist:
        return False
    except Exception as e:
        return False


@shared_task
def send_sms_notification_task(notification_id):
    """
    Async task to send SMS notification
    
    Args:
        notification_id: Notification ID
    
    Returns:
        bool: Success status
    """
    from .utils import send_sms_notification
    
    try:
        notification = Notification.objects.get(id=notification_id)
        send_sms_notification(notification)
        return True
    except Notification.DoesNotExist:
        return False
    except Exception as e:
        return False


@shared_task
def send_push_notification_task(notification_id):
    """
    Async task to send push notification
    
    Args:
        notification_id: Notification ID
    
    Returns:
        bool: Success status
    """
    from .utils import send_push_notification
    
    try:
        notification = Notification.objects.get(id=notification_id)
        send_push_notification(notification)
        return True
    except Notification.DoesNotExist:
        return False
    except Exception as e:
        return False


# Celery Beat Schedule (add to settings.py)
"""
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'process-scheduled-notifications': {
        'task': 'apps.notifications.tasks.process_scheduled_notifications_task',
        'schedule': crontab(minute='*/5'),  # Every 5 minutes
    },
    'cleanup-old-notifications': {
        'task': 'apps.notifications.tasks.cleanup_old_notifications_task',
        'schedule': crontab(hour=2, minute=0),  # Daily at 2 AM
        'kwargs': {'days': 30}
    },
    'send-daily-digest': {
        'task': 'apps.notifications.tasks.send_daily_digest_task',
        'schedule': crontab(minute=0),  # Every hour
    },
}
"""
