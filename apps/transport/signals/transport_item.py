"""
Transport Signals
"""
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from ..models import VehicleMaintenance, FuelLog

@receiver(post_save, sender=VehicleMaintenance)
def maintenance_post_save(sender, instance, created, **kwargs):
    """
    Update vehicle status when maintenance is scheduled
    """
    if created and instance.status == 'in_progress':
        vehicle = instance.vehicle
        vehicle.status = 'maintenance'
        vehicle.save()

@receiver(post_save, sender=FuelLog)
def fuel_log_post_save(sender, instance, created, **kwargs):
    """
    Track fuel consumption patterns
    """
    if created:
        # Can be used for analytics
        pass
