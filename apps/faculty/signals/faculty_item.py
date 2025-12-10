"""
FacultyItem Signals
"""
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import FacultyItem

@receiver(post_save, sender=FacultyItem)
def faculty_item_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for FacultyItem post_save
    """
    if created:
        # Do something when item is created
        pass
    else:
        # Do something when item is updated
        pass

@receiver(pre_delete, sender=FacultyItem)
def faculty_item_pre_delete(sender, instance, **kwargs):
    """
    Signal handler for FacultyItem pre_delete
    """
    # Do something before item is deleted
    pass
