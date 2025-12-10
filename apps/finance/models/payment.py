"""Payment model for finance app"""
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from apps.core.models import TimeStampedModel


class Payment(TimeStampedModel):
    """
    Payment model for recording student fee payments with method, timestamp, and late fee tracking
    """
    
    class Method(models.TextChoices):
        CASH = 'cash', 'Cash'
        CHEQUE = 'cheque', 'Cheque'
        CARD = 'card', 'Debit/Credit Card'
        ONLINE = 'online', 'Online Payment'
        UPI = 'upi', 'UPI'
        BANK_TRANSFER = 'bank_transfer', 'Bank Transfer'
    
    # Payment identification
    receipt_number = models.CharField(max_length=50, unique=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Invoice association
    invoice = models.ForeignKey(
        'finance.Invoice',
        on_delete=models.CASCADE,
        related_name='payments'
    )
    
    # Student (for quick access)
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.CASCADE,
        related_name='payments'
    )
    
    # Payment details
    amount_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    late_fee_applied = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    
    # Payment method
    method = models.CharField(max_length=20, choices=Method.choices)
    
    # Payment timestamp
    payment_date = models.DateTimeField(default=timezone.now)
    
    # Additional payment details
    reference_number = models.CharField(max_length=100, blank=True)
    remarks = models.TextField(blank=True)
    
    # Processed by (staff member)
    processed_by = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='processed_payments'
    )
    
    class Meta:
        db_table = 'finance_payments'
        ordering = ['-payment_date']
        indexes = [
            models.Index(fields=['receipt_number']),
            models.Index(fields=['invoice']),
            models.Index(fields=['student']),
            models.Index(fields=['payment_date']),
        ]
    
    def __str__(self):
        return f"{self.receipt_number} - ${self.amount_paid}"
    
    def save(self, *args, **kwargs):
        """Auto-generate receipt number"""
        if not self.receipt_number:
            from datetime import datetime
            year = datetime.now().year
            count = Payment.objects.filter(created_at__year=year).count() + 1
            self.receipt_number = f"RCP-{year}-{count:06d}"
        
        # Set student from invoice if not set
        if not self.student_id and self.invoice:
            self.student = self.invoice.student
        
        super().save(*args, **kwargs)
        
        # Update invoice after payment
        if self.invoice:
            self.invoice.amount_paid = sum(
                p.amount_paid for p in self.invoice.payments.all()
            )
            self.invoice.save()
