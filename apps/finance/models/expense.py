"""Expense model for finance app"""
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from apps.core.models import TimeStampedModel


class ExpenseCategory(TimeStampedModel):
    """Categories for expenses"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subcategories'
    )
    
    class Meta:
        db_table = 'finance_expense_categories'
        verbose_name_plural = 'Expense Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Expense(TimeStampedModel):
    """Expense/Expenditure tracking"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('paid', 'Paid'),
        ('rejected', 'Rejected'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    expense_number = models.CharField(max_length=50, unique=True, db_index=True)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.PROTECT, related_name='expenses')
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    
    expense_date = models.DateField(default=timezone.now)
    payment_date = models.DateField(null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', db_index=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    
    vendor_name = models.CharField(max_length=200, blank=True)
    vendor_contact = models.CharField(max_length=100, blank=True)
    invoice_number = models.CharField(max_length=100, blank=True)
    
    payment_method = models.CharField(max_length=50, blank=True)
    transaction_reference = models.CharField(max_length=100, blank=True)
    
    requested_by = models.ForeignKey('authentication.User', on_delete=models.SET_NULL, null=True, related_name='requested_expenses')
    approved_by = models.ForeignKey('authentication.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_expenses')
    approval_date = models.DateTimeField(null=True, blank=True)
    
    attachment = models.FileField(upload_to='finance/expenses/%Y/%m/', blank=True, null=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'finance_expenses'
        ordering = ['-expense_date', '-created_at']
        indexes = [
            models.Index(fields=['expense_number']),
            models.Index(fields=['category', 'status']),
            models.Index(fields=['expense_date']),
        ]
    
    def __str__(self):
        return f"{self.expense_number} - {self.title} (${self.total_amount})"
    
    def save(self, *args, **kwargs):
        if not self.expense_number:
            year = timezone.now().year
            count = Expense.objects.filter(created_at__year=year).count() + 1
            self.expense_number = f"EXP-{year}-{count:06d}"
        
        self.total_amount = self.amount + self.tax_amount
        super().save(*args, **kwargs)
