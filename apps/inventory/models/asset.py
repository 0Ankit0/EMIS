from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from apps.core.models import TimeStampedModel
from apps.inventory.models.item import Item
from apps.inventory.models.location import Location
from apps.inventory.models.purchase_order import PurchaseOrder
User = get_user_model()

class Asset(TimeStampedModel):
    """Fixed Asset Management"""
    
    class Status(models.TextChoices):
        AVAILABLE = 'available', 'Available'
        IN_USE = 'in_use', 'In Use'
        MAINTENANCE = 'maintenance', 'Under Maintenance'
        REPAIR = 'repair', 'Under Repair'
        RETIRED = 'retired', 'Retired'
        DISPOSED = 'disposed', 'Disposed'
    
    class Condition(models.TextChoices):
        EXCELLENT = 'excellent', 'Excellent'
        GOOD = 'good', 'Good'
        FAIR = 'fair', 'Fair'
        POOR = 'poor', 'Poor'
    
    asset_number = models.CharField(max_length=50, unique=True, db_index=True)
    
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='assets')
    
    serial_number = models.CharField(max_length=100, unique=True, null=True, blank=True)
    
    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='assets')
    
    purchase_date = models.DateField()
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.SET_NULL, null=True, blank=True, related_name='assets')
    
    current_value = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    depreciation_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Annual depreciation rate in percentage"
    )
    
    warranty_expiry_date = models.DateField(null=True, blank=True)
    
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_assets'
    )
    assigned_date = models.DateField(null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE, db_index=True)
    condition = models.CharField(max_length=20, choices=Condition.choices, default=Condition.GOOD)
    
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'inventory_assets'
        ordering = ['asset_number']
        verbose_name = 'Asset'
        verbose_name_plural = 'Assets'
        indexes = [
            models.Index(fields=['asset_number']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.asset_number} - {self.item.name}"

