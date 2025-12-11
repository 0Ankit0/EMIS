from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from apps.core.models import TimeStampedModel
from apps.inventory.models.item import Item
from apps.inventory.models.location import Location
User = get_user_model()

class StockTransaction(TimeStampedModel):
    """Stock Movement/Transaction"""
    
    class TransactionType(models.TextChoices):
        PURCHASE = 'purchase', 'Purchase/Receipt'
        ISSUE = 'issue', 'Issue/Consumption'
        TRANSFER = 'transfer', 'Transfer'
        ADJUSTMENT = 'adjustment', 'Adjustment'
        RETURN = 'return', 'Return'
        DAMAGE = 'damage', 'Damage/Loss'
    
    transaction_number = models.CharField(max_length=50, unique=True, db_index=True)
    transaction_type = models.CharField(max_length=20, choices=TransactionType.choices)
    
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='transactions')
    
    from_location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='outgoing_transactions'
    )
    to_location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='incoming_transactions'
    )
    
    quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    reference_number = models.CharField(max_length=100, blank=True, help_text="PO/Invoice/Requisition number")
    
    transaction_date = models.DateTimeField(default=timezone.now)
    
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='stock_transactions')
    
    remarks = models.TextField(blank=True)
    
    class Meta:
        db_table = 'inventory_transactions'
        ordering = ['-transaction_date']
        verbose_name = 'Stock Transaction'
        verbose_name_plural = 'Stock Transactions'
        indexes = [
            models.Index(fields=['transaction_number']),
            models.Index(fields=['item', 'transaction_date']),
        ]
    
    def __str__(self):
        return f"{self.transaction_number} - {self.transaction_type}"
    
    def save(self, *args, **kwargs):
        if not self.transaction_number:
            year = timezone.now().year
            from django.db.models import Count
            count = StockTransaction.objects.filter(created_at__year=year).count() + 1
            self.transaction_number = f"TXN-{year}-{count:06d}"
        super().save(*args, **kwargs)

