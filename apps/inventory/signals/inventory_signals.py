"""Inventory Signals"""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from ..models import StockTransaction, PurchaseOrderItem, Stock
from django.db import models

@receiver(post_save, sender=StockTransaction)
def update_stock_on_transaction(sender, instance, created, **kwargs):
    """Update stock levels when transaction is created"""
    if created:
        # Update from_location stock (decrease)
        if instance.from_location and instance.transaction_type in ['issue', 'transfer']:
            stock, _ = Stock.objects.get_or_create(
                item=instance.item,
                location=instance.from_location
            )
            stock.quantity -= instance.quantity
            stock.save()
        
        # Update to_location stock (increase)
        if instance.to_location and instance.transaction_type in ['purchase', 'transfer']:
            stock, _ = Stock.objects.get_or_create(
                item=instance.item,
                location=instance.to_location
            )
            stock.quantity += instance.quantity
            stock.save()

@receiver(post_save, sender=PurchaseOrderItem)
def update_po_subtotal(sender, instance, **kwargs):
    """Update PO subtotal when items are added/modified"""
    po = instance.purchase_order
    subtotal = po.items.aggregate(total=models.Sum('line_total'))['total'] or 0
    po.subtotal = subtotal
    po.save()

@receiver(pre_save, sender=Stock)
def validate_stock_quantity(sender, instance, **kwargs):
    """Ensure stock quantity doesn't go negative"""
    if instance.quantity < 0:
        instance.quantity = 0
