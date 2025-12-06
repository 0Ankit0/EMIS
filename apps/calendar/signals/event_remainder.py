from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from apps.calendar.models.event import Event

@receiver(post_save, sender=Event)
def send_event_reminder(sender, instance, created, **kwargs):
    if instance.reminder_enabled and instance.remainder_time_before_event:
        # Calculate reminder time
        reminder_time = None
        if instance.start_date and instance.start_time:
            event_datetime = timezone.make_aware(
                timezone.datetime.combine(instance.start_date, instance.start_time)
            )
            reminder_time = event_datetime - instance.remainder_time_before_event

        # Only schedule if reminder time is in the future
        if reminder_time and reminder_time > timezone.now():
            # Here, you would enqueue a task or send a notification/email
            # For example, using Celery:
            # send_reminder_task.apply_async((instance.ukid,), eta=reminder_time)
            print(f"Reminder scheduled for event '{instance.title}' at {reminder_time}")
