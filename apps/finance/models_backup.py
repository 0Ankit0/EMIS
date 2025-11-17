"""
Finance models for EMIS
"""
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from apps.core.models import TimeStampedModel, AuditModel


class FeeCategory(models.TextChoices):
    """Fee category choices"""
    TUITION = 'tuition', 'Tuition Fee'
    EXAM = 'exam', 'Exam Fee'
    LIBRARY = 'library', 'Library Fee'
    LAB = 'lab', 'Laboratory Fee'
    HOSTEL = 'hostel', 'Hostel Fee'
    TRANSPORT = 'transport', 'Transport Fee'
    SPORTS = 'sports', 'Sports Fee'
    MISCELLANEOUS = 'miscellaneous', 'Miscellaneous'


class PaymentStatus(models.TextChoices):
    """Payment status choices"""
    PENDING = 'pending', 'Pending'
    PAID = 'paid', 'Paid'
    PARTIAL = 'partial', 'Partially Paid'
    OVERDUE = 'overdue', 'Overdue'
    CANCELLED = 'cancelled', 'Cancelled'


class PaymentMethod(models.TextChoices):
    """Payment method choices"""
    CASH = 'cash', 'Cash'
    CHEQUE = 'cheque', 'Cheque'
    CARD = 'card', 'Debit/Credit Card'
    ONLINE = 'online', 'Online Payment'
    UPI = 'upi', 'UPI'
    BANK_TRANSFER = 'bank_transfer', 'Bank Transfer'


class FeeStructure(AuditModel):
    """Fee structure for different programs/courses"""
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=20, choices=FeeCategory.choices)
    
    # Program/Course details
    program = models.ForeignKey('core.Program', on_delete=models.CASCADE, related_name='fee_structures', null=True, blank=True)
    semester = models.IntegerField(validators=[MinValueValidator(1)], null=True, blank=True)
    year = models.IntegerField(validators=[MinValueValidator(1)], null=True, blank=True)
    
    # Fee details
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    late_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    # Validity
    valid_from = models.DateField()
    valid_to = models.DateField()
    is_active = models.BooleanField(default=True)
    
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'fee_structures'
        ordering = ['name']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class FeePayment(AuditModel):
    """Student fee payment records"""
    receipt_number = models.CharField(max_length=50, unique=True)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='fee_payments')
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.PROTECT, related_name='payments')
    
    # Payment details
    amount_due = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    late_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    # Status
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices, blank=True, null=True)
    
    # Dates
    due_date = models.DateField()
    payment_date = models.DateTimeField(blank=True, null=True)
    
    # Payment reference
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    
    remarks = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'fee_payments'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['receipt_number']),
            models.Index(fields=['student']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.receipt_number} - {self.student.student_number}: {self.amount_paid}/{self.amount_due}"
    
    @property
    def balance(self):
        """Calculate outstanding balance"""
        return self.amount_due - self.amount_paid + self.late_fee
    
    @property
    def is_fully_paid(self):
        """Check if fully paid"""
        return self.amount_paid >= self.amount_due
    
    def save(self, *args, **kwargs):
        """Auto-generate receipt number and update status"""
        if not self.receipt_number:
            from datetime import datetime
            year = datetime.now().year
            count = FeePayment.objects.filter(created_at__year=year).count() + 1
            self.receipt_number = f"RCP-{year}-{count:06d}"
        
        # Update status
        if self.amount_paid >= self.amount_due:
            self.status = PaymentStatus.PAID
        elif self.amount_paid > 0:
            self.status = PaymentStatus.PARTIAL
        elif self.due_date < datetime.now().date() and self.amount_paid == 0:
            self.status = PaymentStatus.OVERDUE
        
        super().save(*args, **kwargs)


class Invoice(AuditModel):
    """Invoice for various charges"""
    invoice_number = models.CharField(max_length=50, unique=True)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='invoices', null=True, blank=True)
    
    # Invoice details
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    # Dates
    invoice_date = models.DateField()
    due_date = models.DateField()
    
    # Status
    is_paid = models.BooleanField(default=False)
    paid_date = models.DateField(blank=True, null=True)
    
    class Meta:
        db_table = 'invoices'
        ordering = ['-invoice_date']
    
    def __str__(self):
        return f"{self.invoice_number} - {self.total_amount}"


class Receipt(AuditModel):
    """Payment receipt"""
    receipt_number = models.CharField(max_length=50, unique=True)
    payment = models.OneToOneField(FeePayment, on_delete=models.CASCADE, related_name='receipt', null=True, blank=True)
    
    # Receipt details
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices)
    payment_date = models.DateTimeField()
    
    remarks = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'receipts'
        ordering = ['-payment_date']
    
    def __str__(self):
        return f"{self.receipt_number} - {self.amount}"
