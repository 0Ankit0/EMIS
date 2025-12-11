from django.db import models
from apps.core.models import TimeStampedModel
from django.contrib.auth import get_user_model

User = get_user_model()


class Location(TimeStampedModel):
    """Storage Location"""
    
    class LocationType(models.TextChoices):
        WAREHOUSE = 'warehouse', 'Warehouse'
        STORE = 'store', 'Store Room'
        DEPARTMENT = 'department', 'Department'
        LAB = 'lab', 'Laboratory'
        OFFICE = 'office', 'Office'
        OTHER = 'other', 'Other'
    
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True, db_index=True)
    location_type = models.CharField(max_length=20, choices=LocationType.choices)
    building = models.CharField(max_length=100, blank=True)
    floor = models.CharField(max_length=50, blank=True)
    room_number = models.CharField(max_length=50, blank=True)
    capacity = models.IntegerField(null=True, blank=True)
    in_charge = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_locations'
    )
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'inventory_locations'
        ordering = ['name']
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'
    
    def __str__(self):
        return f"{self.code} - {self.name}"

