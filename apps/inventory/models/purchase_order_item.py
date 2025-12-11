from django.db import models
from django.core.validators import MinValueValidator
from apps.inventory.models.purchase_order import PurchaseOrder
from apps.inventory.models.item import Item
from apps.core.models import TimeStampedModel


class PurchaseOrderItem(TimeStampedModel):
    """Purchase Order Line Items"""
    
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='po_items')
    
    quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    
    received_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    line_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'inventory_po_items'
        ordering = ['purchase_order', 'id']
        verbose_name = 'PO Item'
        verbose_name_plural = 'PO Items'
    
    def __str__(self):
        return f"{self.purchase_order.po_number} - {self.item.name}"
    
    def save(self, *args, **kwargs):
        self.line_total = self.quantity * self.unit_price
        super().save(*args, **kwargs)

