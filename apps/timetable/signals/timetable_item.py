"""
Timetable Signals
"""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from ..models import AcademicYear, Semester

@receiver(pre_save, sender=AcademicYear)
def academic_year_pre_save(sender, instance, **kwargs):
    """
    Ensure only one active academic year
    """
    if instance.is_active:
        AcademicYear.objects.filter(is_active=True).exclude(pk=instance.pk).update(is_active=False)

@receiver(post_save, sender=Semester)
def semester_post_save(sender, instance, created, **kwargs):
    """
    Handle semester creation/update
    """
    if created:
        # Can trigger timetable generation here
        pass
