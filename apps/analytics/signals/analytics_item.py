"""
Analytics Signals
"""
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import AnalyticsItem

@receiver(post_save, sender=AnalyticsItem)
def analytics_item_post_save(sender, instance, created, **kwargs):
    """
    Signal handler for AnalyticsItem post_save
    """
    if created:
        # Do something when item is created
        pass
    else:
        # Do something when item is updated
        pass

@receiver(pre_delete, sender=AnalyticsItem)
def analytics_item_pre_delete(sender, instance, **kwargs):
    """
    Signal handler for AnalyticsItem pre_delete
    """
    # Do something before item is deleted
    pass
