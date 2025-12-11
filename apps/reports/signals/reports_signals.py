"""
Reports Signals
"""
from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver
from ..models import GeneratedReport, ScheduledReport, ReportTemplate

@receiver(post_save, sender=GeneratedReport)
def generated_report_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for GeneratedReport post_save
    """
    if created:
        # Log report generation
        pass
    else:
        # Handle updates
        pass

@receiver(pre_delete, sender=GeneratedReport)
def generated_report_pre_delete(sender, instance, **kwargs):
    """
    Signal handler for GeneratedReport pre_delete
    Clean up file before deletion
    """
    if instance.file:
        try:
            instance.file.delete(save=False)
        except Exception:
            pass

@receiver(post_save, sender=ScheduledReport)
def scheduled_report_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for ScheduledReport post_save
    Update next run time
    """
    if created and instance.is_active:
        # Schedule the first run
        if not instance.next_run:
            from .utils import calculate_next_run
            instance.next_run = calculate_next_run(
                instance.schedule_type,
                instance.scheduled_time,
                instance.timezone
            )
            instance.save(update_fields=['next_run'])

@receiver(post_delete, sender=ReportTemplate)
def report_template_post_delete(sender, instance, **kwargs):
    """
    Signal handler for ReportTemplate post_delete
    Clean up template file
    """
    if instance.template_file:
        try:
            instance.template_file.delete(save=False)
        except Exception:
            pass
