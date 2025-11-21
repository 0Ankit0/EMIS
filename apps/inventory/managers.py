"""Inventory Custom Managers"""
from django.db import models
from django.utils import timezone


class ItemQuerySet(models.QuerySet):
    """Custom queryset for Item"""
    
    def active(self):
        return self.filter(is_active=True)
    
    def consumables(self):
        return self.filter(item_type='consumable')
    
    def assets(self):
        return self.filter(item_type='asset')
    
    def low_stock(self):
        """Items below reorder level"""
        from .models import Stock
        items_with_low_stock = []
        for item in self.all():
            total_stock = Stock.objects.filter(item=item).aggregate(
                total=models.Sum('quantity')
            )['total'] or 0
            if total_stock <= item.reorder_level:
                items_with_low_stock.append(item.pk)
        return self.filter(pk__in=items_with_low_stock)


class ItemManager(models.Manager):
    def get_queryset(self):
        return ItemQuerySet(self.model, using=self._db)
    
    def active(self):
        return self.get_queryset().active()
    
    def consumables(self):
        return self.get_queryset().consumables()
    
    def low_stock(self):
        return self.get_queryset().low_stock()


class PurchaseOrderQuerySet(models.QuerySet):
    """Custom queryset for PurchaseOrder"""
    
    def draft(self):
        return self.filter(status='draft')
    
    def pending(self):
        return self.filter(status='pending')
    
    def approved(self):
        return self.filter(status='approved')
    
    def ordered(self):
        return self.filter(status='ordered')
    
    def received(self):
        return self.filter(status='received')


class PurchaseOrderManager(models.Manager):
    def get_queryset(self):
        return PurchaseOrderQuerySet(self.model, using=self._db)
    
    def draft(self):
        return self.get_queryset().draft()
    
    def pending(self):
        return self.get_queryset().pending()
    
    def approved(self):
        return self.get_queryset().approved()


class AssetQuerySet(models.QuerySet):
    """Custom queryset for Asset"""
    
    def available(self):
        return self.filter(status='available')
    
    def in_use(self):
        return self.filter(status='in_use')
    
    def under_maintenance(self):
        return self.filter(status__in=['maintenance', 'repair'])
    
    def warranty_expiring_soon(self, days=30):
        """Assets with warranty expiring in next N days"""
        from datetime import timedelta
        future_date = timezone.now().date() + timedelta(days=days)
        return self.filter(
            warranty_expiry_date__lte=future_date,
            warranty_expiry_date__gte=timezone.now().date()
        )


class AssetManager(models.Manager):
    def get_queryset(self):
        return AssetQuerySet(self.model, using=self._db)
    
    def available(self):
        return self.get_queryset().available()
    
    def in_use(self):
        return self.get_queryset().in_use()
    
    def warranty_expiring_soon(self, days=30):
        return self.get_queryset().warranty_expiring_soon(days)


class RequisitionQuerySet(models.QuerySet):
    """Custom queryset for Requisition"""
    
    def pending(self):
        return self.filter(status='pending')
    
    def approved(self):
        return self.filter(status='approved')
    
    def fulfilled(self):
        return self.filter(status='fulfilled')


class RequisitionManager(models.Manager):
    def get_queryset(self):
        return RequisitionQuerySet(self.model, using=self._db)
    
    def pending(self):
        return self.get_queryset().pending()
    
    def approved(self):
        return self.get_queryset().approved()
