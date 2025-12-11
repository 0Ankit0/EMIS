from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from apps.core.models import TimeStampedModel
from .requisition import Requisition
from .item import Item

User = get_user_model()


class RequisitionItem(TimeStampedModel):
    """Requisition Line Items"""
    
    requisition = models.ForeignKey(Requisition, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='requisition_items')
    
    requested_quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    issued_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'inventory_requisition_items'
        ordering = ['requisition', 'id']
        verbose_name = 'Requisition Item'
        verbose_name_plural = 'Requisition Items'
    
    def __str__(self):
        return f"{self.requisition.requisition_number} - {self.item.name}"

