from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import TimeStampedModel
from ..managers import HostelManager
from decimal import Decimal

User = get_user_model()

class Hostel(TimeStampedModel):
    """Hostel/Dormitory Building"""
    class HostelType(models.TextChoices):
        BOYS = 'boys', "Boys' Hostel"
        GIRLS = 'girls', "Girls' Hostel"
        MIXED = 'mixed', 'Co-ed Hostel'
    
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        MAINTENANCE = 'maintenance', 'Under Maintenance'
        CLOSED = 'closed', 'Closed'
    
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True, db_index=True)
    hostel_type = models.CharField(max_length=20, choices=HostelType.choices)
    address = models.TextField()
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    total_floors = models.IntegerField(validators=[MinValueValidator(1)])
    total_rooms = models.IntegerField(validators=[MinValueValidator(1)])
    total_capacity = models.IntegerField(validators=[MinValueValidator(1)])
    occupied_capacity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    warden = models.ForeignKey(
        'faculty.Faculty',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_hostels'
    )
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    amenities = models.JSONField(
        default=list,
        help_text="List of amenities: ['WiFi', 'Laundry', 'Gym', etc.]"
    )
    facilities = models.TextField(blank=True, help_text="Description of facilities")
    rules_and_regulations = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE, db_index=True)
    is_active = models.BooleanField(default=True)
    established_date = models.DateField(null=True, blank=True)
    
    class Meta:
        db_table = 'hostels'
        ordering = ['name']
        verbose_name = 'Hostel'
        verbose_name_plural = 'Hostels'
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['hostel_type', 'status']),
        ]
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    @property
    def available_capacity(self):
        return self.total_capacity - self.occupied_capacity
    
    @property
    def occupancy_percentage(self):
        if self.total_capacity > 0:
            return (self.occupied_capacity / self.total_capacity) * 100
        return 0

