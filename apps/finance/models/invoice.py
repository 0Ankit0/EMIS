"""Invoice model for finance app"""
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from apps.core.models import TimeStampedModel


class Invoice(TimeStampedModel):
    """
    Invoice model for student fee invoices with components, amount due, and status tracking
    """
    
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PARTIAL = 'partial', 'Partially Paid'
        PAID = 'paid', 'Paid'
        OVERDUE = 'overdue', 'Overdue'
        CANCELLED = 'cancelled', 'Cancelled'
    
    # Invoice identification
    invoice_number = models.CharField(max_length=50, unique=True)
    
    # Student association
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.CASCADE,
        related_name='invoices'
    )
    
    # Fee structure reference
    fee_structure = models.ForeignKey(
        'finance.FeeStructure',
        on_delete=models.PROTECT,
        related_name='invoices',
        null=True,
        blank=True
    )
    
    # Fee components breakdown
    fee_components = models.JSONField(
        default=dict,
        help_text="Breakdown of fees: {'tuition': 5000, 'lab': 500}"
    )
    
    # Amount details
    amount_due = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    amount_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    late_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    
    # Dates
    invoice_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    
    # Status
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    
    # Additional details
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    # Academic period
    academic_year = models.CharField(max_length=20, blank=True)
    semester = models.CharField(max_length=50, blank=True)
    
    class Meta:
        db_table = 'finance_invoices'
        ordering = ['-invoice_date']
        indexes = [
            models.Index(fields=['invoice_number']),
            models.Index(fields=['student']),
            models.Index(fields=['status']),
            models.Index(fields=['due_date']),
        ]
    
    def __str__(self):
        return f"{self.invoice_number} - {self.student.user.email}: ${self.amount_due}"
    
    @property
    def balance(self):
        """Calculate outstanding balance including late fees"""
        return self.amount_due + self.late_fee - self.amount_paid
    
    @property
    def is_overdue(self):
        """Check if invoice is overdue"""
        from datetime import date
        return self.due_date < date.today() and self.balance > 0
    
    @property
    def is_paid(self):
        """Check if invoice is fully paid"""
        return self.amount_paid >= (self.amount_due + self.late_fee)
    
    def save(self, *args, **kwargs):
        """Auto-generate invoice number and update status"""
        if not self.invoice_number:
            from datetime import datetime
            year = datetime.now().year
            count = Invoice.objects.filter(created_at__year=year).count() + 1
            self.invoice_number = f"INV-{year}-{count:06d}"
        
        # Update status based on payment
        if self.is_paid:
            self.status = 'paid'
        elif self.amount_paid > 0:
            self.status = 'partial'
        elif self.is_overdue:
            self.status = 'overdue'
        else:
            self.status = 'pending'
        
        super().save(*args, **kwargs)
