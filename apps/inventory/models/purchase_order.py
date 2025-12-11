from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from apps.inventory.models.supplier import Supplier
from apps.core.models import TimeStampedModel

User = get_user_model()

class PurchaseOrder(TimeStampedModel):
    """Purchase Order"""
    
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PENDING = 'pending', 'Pending Approval'
        APPROVED = 'approved', 'Approved'
        ORDERED = 'ordered', 'Ordered'
        PARTIALLY_RECEIVED = 'partially_received', 'Partially Received'
        RECEIVED = 'received', 'Received'
        CANCELLED = 'cancelled', 'Cancelled'
    
    po_number = models.CharField(max_length=50, unique=True, db_index=True)
    
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='purchase_orders')
    
    order_date = models.DateField(default=timezone.now)
    expected_delivery_date = models.DateField(null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True)
    
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    shipping_charges = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    payment_terms = models.CharField(max_length=200, blank=True)
    delivery_address = models.TextField(blank=True)
    
    notes = models.TextField(blank=True)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_pos')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_pos')
    approval_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'inventory_purchase_orders'
        ordering = ['-order_date']
        verbose_name = 'Purchase Order'
        verbose_name_plural = 'Purchase Orders'
        indexes = [
            models.Index(fields=['po_number']),
            models.Index(fields=['supplier', 'status']),
        ]
    
    def __str__(self):
        return f"{self.po_number} - {self.supplier.name}"
    
    def save(self, *args, **kwargs):
        # Auto-generate PO number if not set
        if not self.po_number:
            year = timezone.now().year
            from django.db.models import Count
            count = PurchaseOrder.objects.filter(created_at__year=year).count() + 1
            self.po_number = f"PO-{year}-{count:06d}"
        
        # Calculate total
        self.total_amount = self.subtotal + self.tax_amount + self.shipping_charges - self.discount
        
        super().save(*args, **kwargs)

