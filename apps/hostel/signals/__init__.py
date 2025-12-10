"""Hostel Signals"""
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import RoomAllocation, Complaint


@receiver(post_save, sender=RoomAllocation)
def update_room_on_allocation(sender, instance, created, **kwargs):
    """Update room occupancy when allocation is created/updated"""
    if created and instance.status == 'active':
        room = instance.room
        # Occupancy is updated in the API view
        pass


@receiver(pre_delete, sender=RoomAllocation)
def update_room_on_allocation_delete(sender, instance, **kwargs):
    """Update room occupancy when allocation is deleted"""
    if instance.status == 'active':
        room = instance.room
        room.occupied_beds = max(0, room.occupied_beds - 1)
        if room.occupied_beds < room.capacity:
            room.status = 'available'
        room.save()
        
        # Update hostel occupancy
        hostel = room.hostel
        hostel.occupied_capacity = max(0, hostel.occupied_capacity - 1)
        hostel.save()


@receiver(post_save, sender=Complaint)
def notify_on_complaint_status_change(sender, instance, created, **kwargs):
    """Send notification when complaint status changes"""
    if not created:
        # TODO: Send email/SMS notification to student
        pass


@receiver(post_save, sender=Complaint)
def auto_assign_urgent_complaints(sender, instance, created, **kwargs):
    """Auto-assign urgent complaints to warden"""
    if created and instance.priority == 'urgent':
        # TODO: Assign to warden or send notification
        pass
