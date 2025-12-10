"""
Attendance Signals
"""
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import AttendanceRecord


@receiver(post_save, sender=AttendanceRecord)
def update_session_counts(sender, instance, created, **kwargs):
    """Update session counts when attendance is marked"""
    if instance.session:
        instance.session.update_counts()


@receiver(pre_delete, sender=AttendanceRecord)
def update_session_counts_on_delete(sender, instance, **kwargs):
    """Update session counts when attendance is deleted"""
    if instance.session:
        instance.session.update_counts()
