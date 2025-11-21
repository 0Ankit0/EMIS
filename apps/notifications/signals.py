"""
Notifications Signals
"""
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Notification, NotificationPreference, ScheduledNotification

User = get_user_model()


@receiver(post_save, sender=User)
def create_notification_preference(sender, instance, created, **kwargs):
    """
    Create notification preference for new users
    """
    if created:
        NotificationPreference.objects.get_or_create(user=instance)


@receiver(post_save, sender=Notification)
def notification_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for Notification post_save
    """
    if created:
        # Send notifications through configured channels
        from .utils import send_email_notification, send_sms_notification, send_push_notification, NotificationLog
        
        for channel in instance.channels:
            try:
                if channel == 'email' and not instance.email_sent:
                    send_email_notification(instance)
                elif channel == 'sms' and not instance.sms_sent:
                    send_sms_notification(instance)
                elif channel == 'push' and not instance.push_sent:
                    send_push_notification(instance)
            except Exception as e:
                # Log the error
                NotificationLog.objects.create(
                    notification=instance,
                    channel=channel,
                    is_successful=False,
                    error_message=str(e)
                )


@receiver(pre_delete, sender=Notification)
def notification_pre_delete(sender, instance, **kwargs):
    """
    Signal handler for Notification pre_delete
    Clean up related data if necessary
    """
    pass


@receiver(post_save, sender=ScheduledNotification)
def scheduled_notification_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for ScheduledNotification post_save
    """
    if created and instance.is_active:
        # Optionally trigger scheduling system
        pass
