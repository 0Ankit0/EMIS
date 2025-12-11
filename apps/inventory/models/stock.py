from django.db import models
from apps.core.models import TimeStampedModel
from apps.inventory.models.item import Item
from apps.inventory.models.location import Location
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Stock(TimeStampedModel):
    """Stock/Inventory Levels per Location"""
    
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='stock_records')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='stock_items')
    
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    reserved_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    last_updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_stocks')
    
    class Meta:
        db_table = 'inventory_stock'
        unique_together = ['item', 'location']
        ordering = ['item', 'location']
        verbose_name = 'Stock'
        verbose_name_plural = 'Stock Records'
        indexes = [
            models.Index(fields=['item', 'location']),
        ]
    
    def __str__(self):
        return f"{self.item.code} @ {self.location.code} - Qty: {self.quantity}"
    
    @property
    def available_quantity(self):
        return self.quantity - self.reserved_quantity

