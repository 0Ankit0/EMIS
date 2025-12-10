from django.db import models
from django.utils import timezone
from apps.core.models import TimeStampedModel
from django.contrib.auth import get_user_model
from .room import Room
from .managers import RoomAllocationManager

User = get_user_model()

class RoomAllocation(TimeStampedModel):
    """Student Room Allocation"""
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        VACATED = 'vacated', 'Vacated'
        TRANSFERRED = 'transferred', 'Transferred'
        TERMINATED = 'terminated', 'Terminated'
    
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='room_allocations')
    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name='allocations')
    bed_number = models.CharField(max_length=10, blank=True)
    allocation_date = models.DateField(default=timezone.now)
    vacate_date = models.DateField(null=True, blank=True)
    academic_year = models.CharField(max_length=20)
    semester = models.CharField(max_length=50, blank=True)
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, validators=[models.Min(0)])
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[models.Min(0)])
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE, db_index=True)
    allocated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='allocated_rooms')
    remarks = models.TextField(blank=True)
    
    class Meta:
        db_table = 'hostel_room_allocations'
        ordering = ['-allocation_date']
        verbose_name = 'Room Allocation'
        verbose_name_plural = 'Room Allocations'
        indexes = [
            models.Index(fields=['student', 'status']),
            models.Index(fields=['room', 'status']),
            models.Index(fields=['allocation_date']),
        ]
    
    def __str__(self):
        return f"{self.student.user.email} - {self.room.room_number}"
