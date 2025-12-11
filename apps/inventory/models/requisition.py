from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from apps.inventory.models.asset import Asset
from apps.inventory.models.supplier import Supplier
from apps.core.models import TimeStampedModel
User = get_user_model()

class MaintenanceRecord(TimeStampedModel):
    """Asset Maintenance Record"""
    
    class MaintenanceType(models.TextChoices):
        PREVENTIVE = 'preventive', 'Preventive Maintenance'
        CORRECTIVE = 'corrective', 'Corrective Maintenance'
        REPAIR = 'repair', 'Repair'
        CALIBRATION = 'calibration', 'Calibration'
        INSPECTION = 'inspection', 'Inspection'
    
    class Status(models.TextChoices):
        SCHEDULED = 'scheduled', 'Scheduled'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'
    
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='maintenance_records')
    
    maintenance_type = models.CharField(max_length=20, choices=MaintenanceType.choices)
    
    scheduled_date = models.DateField()
    completed_date = models.DateField(null=True, blank=True)
    
    description = models.TextField()
    work_performed = models.TextField(blank=True)
    
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    vendor = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='maintenance_jobs')
    
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='performed_maintenance')
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SCHEDULED)
    
    next_maintenance_date = models.DateField(null=True, blank=True)
    
    class Meta:
        db_table = 'inventory_maintenance'
        ordering = ['-scheduled_date']
        verbose_name = 'Maintenance Record'
        verbose_name_plural = 'Maintenance Records'
    
    def __str__(self):
        return f"{self.asset.asset_number} - {self.maintenance_type} ({self.scheduled_date})"

