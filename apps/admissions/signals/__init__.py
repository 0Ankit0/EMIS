"""
Admissions Signals
"""
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import AdmissionsItem


@receiver(post_save, sender=AdmissionsItem)
def admissions_item_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for AdmissionsItem post_save
    """
    if created:
        # Do something when item is created
        pass
    else:
        # Do something when item is updated
        pass


@receiver(pre_delete, sender=AdmissionsItem)
def admissions_item_pre_delete(sender, instance, **kwargs):
    """
    Signal handler for AdmissionsItem pre_delete
    """
    # Do something before item is deleted
    pass
