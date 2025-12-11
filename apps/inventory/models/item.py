from django.db import models
from apps.core.models import TimeStampedModel
from .category import Category


class Item(TimeStampedModel):
    """Inventory Item/Product"""
    
    class ItemType(models.TextChoices):
        CONSUMABLE = 'consumable', 'Consumable'
        NON_CONSUMABLE = 'non_consumable', 'Non-Consumable'
        ASSET = 'asset', 'Asset'
        EQUIPMENT = 'equipment', 'Equipment'
    
    class Unit(models.TextChoices):
        PCS = 'pcs', 'Pieces'
        KG = 'kg', 'Kilograms'
        G = 'g', 'Grams'
        L = 'l', 'Liters'
        ML = 'ml', 'Milliliters'
        M = 'm', 'Meters'
        CM = 'cm', 'Centimeters'
        BOX = 'box', 'Box'
        SET = 'set', 'Set'
        DOZEN = 'dozen', 'Dozen'
    
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True, db_index=True)
    item_type = models.CharField(max_length=20, choices=ItemType.choices)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='items')
    description = models.TextField(blank=True)
    specifications = models.TextField(blank=True)
    unit = models.CharField(max_length=20, choices=Unit.choices)
    minimum_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    maximum_stock = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    reorder_level = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    manufacturer = models.CharField(max_length=200, blank=True)
    model_number = models.CharField(max_length=100, blank=True)
    barcode = models.CharField(max_length=100, blank=True, unique=True, null=True)
    image = models.ImageField(upload_to='inventory/items/%Y/', blank=True, null=True)
    datasheet = models.FileField(upload_to='inventory/datasheets/%Y/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'inventory_items'
        ordering = ['name']
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
    
    def __str__(self):
        return f"{self.code} - {self.name}"

