"""Calendar Signals"""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from ..models import Event, EventReminder


@receiver(post_save, sender=Event)
def create_default_reminder(sender, instance, created, **kwargs):
    """Create a default reminder when event is created"""
    if created and instance.send_notifications:
        # Create a default 30-minute reminder for the creator
        EventReminder.objects.create(
            event=instance,
            user=instance.created_by,
            time_value=30,
            time_unit='minutes',
            reminder_type='notification'
        )


@receiver(pre_save, sender=Event)
def validate_event_times(sender, instance, **kwargs):
    """Validate event start and end times"""
    if instance.end_datetime <= instance.start_datetime:
        from django.core.exceptions import ValidationError
        raise ValidationError('End time must be after start time')
