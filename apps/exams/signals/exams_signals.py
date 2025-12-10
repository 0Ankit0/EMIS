"""
Exams Signals
"""
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Exam, ExamResult, ExamSchedule

@receiver(post_save, sender=Exam)
def exam_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for Exam post_save
    """
    if created:
        # Log exam creation
        print(f"New exam created: {instance.exam_code}")
        # Could send notifications to students/faculty here
    else:
        # Log exam update
        print(f"Exam updated: {instance.exam_code}")

@receiver(post_save, sender=ExamResult)
def exam_result_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for ExamResult post_save
    """
    if created:
        # Log result creation
        print(f"Result created for {instance.student} in {instance.exam}")
    else:
        # Log result update
        print(f"Result updated for {instance.student} in {instance.exam}")

@receiver(pre_delete, sender=Exam)
def exam_pre_delete(sender, instance, **kwargs):
    """
    Signal handler for Exam pre_delete
    """
    # Log before deleting exam
    print(f"Deleting exam: {instance.exam_code}")

@receiver(post_save, sender=ExamSchedule)
def exam_schedule_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for ExamSchedule post_save
    """
    if created and instance.is_published:
        # Notify about new published schedule
        print(f"New exam schedule published: {instance.name}")
    elif not created and instance.is_published:
        # Notify about schedule update
        print(f"Exam schedule updated: {instance.name}")
