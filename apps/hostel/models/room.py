from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import TimeStampedModel
from ..managers import RoomManager

class Room(TimeStampedModel):
    """Room in a Hostel"""
    class RoomType(models.TextChoices):
        SINGLE = 'single', 'Single'
        DOUBLE = 'double', 'Double'
        TRIPLE = 'triple', 'Triple'
        QUAD = 'quad', 'Quad'
        DORMITORY = 'dormitory', 'Dormitory'
    
    class Status(models.TextChoices):
        AVAILABLE = 'available', 'Available'
        OCCUPIED = 'occupied', 'Occupied'
        FULL = 'full', 'Full'
        MAINTENANCE = 'maintenance', 'Under Maintenance'
        RESERVED = 'reserved', 'Reserved'
    
    hostel = models.ForeignKey('hostel.Hostel', on_delete=models.CASCADE, related_name='rooms')
    floor = models.ForeignKey('hostel.Floor', on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=20, db_index=True)
    room_type = models.CharField(max_length=20, choices=RoomType.choices)
    capacity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    occupied_beds = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    area_sqft = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    has_attached_bathroom = models.BooleanField(default=True)
    has_balcony = models.BooleanField(default=False)
    has_ac = models.BooleanField(default=False)
    furniture = models.JSONField(
        default=list,
        help_text="List of furniture: ['Bed', 'Study Table', 'Chair', 'Wardrobe']"
    )
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE, db_index=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'hostel_rooms'
        unique_together = ['hostel', 'room_number']
        ordering = ['hostel', 'floor', 'room_number']
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'
        indexes = [
            models.Index(fields=['hostel', 'status']),
            models.Index(fields=['room_number']),
        ]
    
    def __str__(self):
        return f"{self.hostel.code} - Room {self.room_number}"
    
    @property
    def available_beds(self):
        return self.capacity - self.occupied_beds
    
    @property
    def is_available(self):
        return self.status == Status.AVAILABLE and self.available_beds > 0

