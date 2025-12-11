"""HR Payroll Model"""
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import TimeStampedModel
from .employee import Employee

User = get_user_model()

class Payroll(TimeStampedModel):
    """Monthly Payroll"""
    
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PROCESSED = 'processed', 'Processed'
        PAID = 'paid', 'Paid'
        ON_HOLD = 'on_hold', 'On Hold'
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='payrolls')
    
    month = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    year = models.IntegerField(validators=[MinValueValidator(2000)])
    
    # Earnings
    basic_salary = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    hra = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    da = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    other_allowances = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    overtime_pay = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    bonus = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    gross_salary = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    
    # Deductions
    pf = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    esi = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    professional_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tds = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    loan_deduction = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    other_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    total_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    net_salary = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    
    # Attendance details
    working_days = models.IntegerField(validators=[MinValueValidator(0)])
    present_days = models.IntegerField(validators=[MinValueValidator(0)])
    leave_days = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True)
    
    payment_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    transaction_reference = models.CharField(max_length=100, blank=True)
    
    remarks = models.TextField(blank=True)
    
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='processed_payrolls')
    
    class Meta:
        db_table = 'hr_payrolls'
        unique_together = ['employee', 'month', 'year']
        ordering = ['-year', '-month']
        verbose_name = 'Payroll'
        verbose_name_plural = 'Payrolls'
        indexes = [
            models.Index(fields=['employee', 'year', 'month']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.employee.employee_id} - {self.month}/{self.year}"
    
    def save(self, *args, **kwargs):
        """Calculate gross, deductions and net salary"""
        self.gross_salary = (
            self.basic_salary + self.hra + self.da + 
            self.other_allowances + self.overtime_pay + self.bonus
        )
        
        self.total_deductions = (
            self.pf + self.esi + self.professional_tax + 
            self.tds + self.loan_deduction + self.other_deductions
        )
        
        self.net_salary = self.gross_salary - self.total_deductions
        
        super().save(*args, **kwargs)
