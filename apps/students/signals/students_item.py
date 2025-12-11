"""
StudentsItem Signals
"""
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import StudentsItem

@receiver(post_save, sender=StudentsItem)
def students_item_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for StudentsItem post_save
    """
    if created:
        # Do something when item is created
        pass
    else:
        # Do something when item is updated
        pass

@receiver(pre_delete, sender=StudentsItem)
def students_item_pre_delete(sender, instance, **kwargs):
    """
    Signal handler for StudentsItem pre_delete
    """
    # Do something before item is deleted
    pass
