"""
Notifications Utility Functions
"""
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from .models import Notification, NotificationLog


def send_notification(recipient, title, message, **kwargs):
    """
    Send notification to a single recipient
    
    Args:
        recipient: User to receive notification
        title: Notification title
        message: Notification message
        **kwargs: Additional notification fields
    
    Returns:
        Notification: Created notification instance
    """
    notification = Notification.objects.create_notification(
        recipient=recipient,
        title=title,
        message=message,
        **kwargs
    )
    
    # Send through configured channels
    channels = kwargs.get('channels', ['in_app'])
    
    for channel in channels:
        try:
            if channel == 'email':
                send_email_notification(notification)
            elif channel == 'sms':
                send_sms_notification(notification)
            elif channel == 'push':
                send_push_notification(notification)
            
            # Log successful delivery
            NotificationLog.objects.create(
                notification=notification,
                channel=channel,
                is_successful=True
            )
        except Exception as e:
            # Log failed delivery
            NotificationLog.objects.create(
                notification=notification,
                channel=channel,
                is_successful=False,
                error_message=str(e)
            )
    
    return notification


def send_bulk_notifications(recipients, title, message, **kwargs):
    """
    Send notifications to multiple recipients
    
    Args:
        recipients: List of users
        title: Notification title
        message: Notification message
        **kwargs: Additional notification fields
    
    Returns:
        int: Number of notifications created
    """
    notifications = Notification.objects.bulk_create_notifications(
        recipients=recipients,
        title=title,
        message=message,
        **kwargs
    )
    
    return len(notifications)


def send_email_notification(notification):
    """Send notification via email"""
    if not notification.recipient.email:
        raise ValueError("Recipient has no email address")
    
    subject = notification.title
    message_text = notification.message
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [notification.recipient.email]
    
    send_mail(subject, message_text, from_email, recipient_list)
    
    notification.email_sent = True
    notification.email_sent_at = timezone.now()
    notification.save(update_fields=['email_sent', 'email_sent_at'])


def send_sms_notification(notification):
    """Send notification via SMS"""
    # Implement SMS sending logic here
    # This is a placeholder - integrate with your SMS provider (Twilio, etc.)
    pass


def send_push_notification(notification):
    """Send push notification"""
    # Implement push notification logic here
    # This is a placeholder - integrate with FCM, APNS, etc.
    pass


def send_notification_from_template(template_code, recipient, context):
    """
    Send notification using a template
    
    Args:
        template_code: Code of the template to use
        recipient: User to receive notification
        context: Context data for template rendering
    
    Returns:
        Notification: Created notification instance
    """
    from .models import NotificationTemplate
    
    template = NotificationTemplate.objects.by_code(template_code)
    if not template:
        raise ValueError(f"Template '{template_code}' not found")
    
    if not template.is_active:
        raise ValueError(f"Template '{template_code}' is not active")
    
    # Render template
    rendered = template.render(context)
    
    # Create notification
    return send_notification(
        recipient=recipient,
        title=rendered['title'],
        message=rendered['message'],
        notification_type=rendered['notification_type'],
        channels=rendered['channels']
    )


def check_user_preferences(user, notification_type, channel):
    """
    Check if user wants to receive notifications of this type through this channel
    
    Args:
        user: User instance
        notification_type: Type of notification
        channel: Delivery channel
    
    Returns:
        bool: True if user wants to receive notification
    """
    from .models import NotificationPreference
    
    try:
        preference = user.notification_preference
    except NotificationPreference.DoesNotExist:
        return True  # Default to sending if no preference set
    
    # Check channel preferences
    if channel == 'email' and not preference.enable_email:
        return False
    elif channel == 'sms' and not preference.enable_sms:
        return False
    elif channel == 'push' and not preference.enable_push:
        return False
    elif channel == 'in_app' and not preference.enable_in_app:
        return False
    
    # Check quiet hours
    if preference.quiet_hours_enabled:
        current_time = timezone.now().time()
        if preference.quiet_hours_start and preference.quiet_hours_end:
            if preference.quiet_hours_start <= current_time <= preference.quiet_hours_end:
                return False
    
    return True


def cleanup_old_notifications(days=30):
    """
    Delete old read notifications
    
    Args:
        days: Number of days to keep notifications
    
    Returns:
        int: Number of deleted notifications
    """
    cutoff_date = timezone.now() - timezone.timedelta(days=days)
    deleted_count = Notification.objects.filter(
        is_read=True,
        read_at__lt=cutoff_date
    ).delete()[0]
    
    return deleted_count


def get_unread_count(user):
    """Get count of unread notifications for user"""
    return Notification.objects.for_user(user).unread().count()


def mark_notifications_as_read_for_object(user, content_object):
    """Mark all notifications for a specific object as read"""
    from django.contrib.contenttypes.models import ContentType
    
    content_type = ContentType.objects.get_for_model(content_object)
    Notification.objects.filter(
        recipient=user,
        content_type=content_type,
        object_id=content_object.id,
        is_read=False
    ).mark_all_as_read()


def process_scheduled_notifications():
    """
    Process and send scheduled notifications that are due
    This should be called by a periodic task (Celery, cron, etc.)
    """
    from .models import ScheduledNotification
    
    now = timezone.now()
    due_notifications = ScheduledNotification.objects.filter(
        scheduled_for__lte=now,
        is_sent=False,
        is_active=True
    )
    
    sent_count = 0
    
    for scheduled in due_notifications:
        try:
            with transaction.atomic():
                # Get recipients
                recipients = list(scheduled.recipients.all())
                
                # Create notifications
                if scheduled.template:
                    # Use template
                    for recipient in recipients:
                        send_notification_from_template(
                            template_code=scheduled.template.code,
                            recipient=recipient,
                            context=scheduled.template_context
                        )
                else:
                    # Use direct content
                    send_bulk_notifications(
                        recipients=recipients,
                        title=scheduled.title,
                        message=scheduled.message,
                        notification_type=scheduled.notification_type,
                        channels=scheduled.channels,
                        action_url=scheduled.action_url
                    )
                
                # Mark as sent
                scheduled.is_sent = True
                scheduled.sent_at = now
                scheduled.save(update_fields=['is_sent', 'sent_at'])
                
                # Handle recurring
                if scheduled.is_recurring:
                    # Create next occurrence
                    next_scheduled = ScheduledNotification.objects.create(
                        title=scheduled.title,
                        message=scheduled.message,
                        notification_type=scheduled.notification_type,
                        scheduled_for=calculate_next_occurrence(now, scheduled.recurrence_pattern),
                        channels=scheduled.channels,
                        action_url=scheduled.action_url,
                        template=scheduled.template,
                        template_context=scheduled.template_context,
                        is_recurring=True,
                        recurrence_pattern=scheduled.recurrence_pattern,
                        is_active=True,
                        created_by=scheduled.created_by
                    )
                    next_scheduled.recipients.set(recipients)
                
                sent_count += 1
        except Exception as e:
            # Log error but continue processing
            print(f"Error processing scheduled notification {scheduled.id}: {str(e)}")
    
    return sent_count


def calculate_next_occurrence(current_time, pattern):
    """Calculate next occurrence for recurring notification"""
    from datetime import timedelta
    
    if pattern == 'daily':
        return current_time + timedelta(days=1)
    elif pattern == 'weekly':
        return current_time + timedelta(weeks=1)
    elif pattern == 'monthly':
        return current_time + timedelta(days=30)
    
    return current_time
