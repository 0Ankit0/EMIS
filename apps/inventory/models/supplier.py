from django.db import models
from apps.core.models import TimeStampedModel


class Supplier(TimeStampedModel):
    """Supplier/Vendor Information"""
    
    class SupplierType(models.TextChoices):
        MANUFACTURER = 'manufacturer', 'Manufacturer'
        DISTRIBUTOR = 'distributor', 'Distributor'
        RETAILER = 'retailer', 'Retailer'
        SERVICE_PROVIDER = 'service_provider', 'Service Provider'
    
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True, db_index=True)
    supplier_type = models.CharField(max_length=30, choices=SupplierType.choices)
    contact_person = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    alternate_phone = models.CharField(max_length=20, blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    country = models.CharField(max_length=100, default='India')
    website = models.URLField(blank=True)
    gstin = models.CharField(max_length=15, blank=True, help_text="GST Identification Number")
    pan = models.CharField(max_length=10, blank=True)
    bank_name = models.CharField(max_length=200, blank=True)
    account_number = models.CharField(max_length=50, blank=True)
    ifsc_code = models.CharField(max_length=20, blank=True)
    credit_days = models.IntegerField(default=0)
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    rating = models.IntegerField(default=3)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'inventory_suppliers'
        ordering = ['name']
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'
    
    def __str__(self):
        return f"{self.code} - {self.name}"

