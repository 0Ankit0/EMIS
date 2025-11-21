"""Budget model for finance app"""
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from apps.core.models import TimeStampedModel


class Budget(TimeStampedModel):
    """Annual/Periodic budget planning"""
    
    PERIOD_CHOICES = [
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('half_yearly', 'Half Yearly'),
        ('annual', 'Annual'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('archived', 'Archived'),
    ]
    
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    
    period_type = models.CharField(max_length=20, choices=PERIOD_CHOICES, default='annual')
    fiscal_year = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    
    total_allocated = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    total_spent = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', db_index=True)
    
    department = models.ForeignKey('faculty.Department', on_delete=models.SET_NULL, null=True, blank=True, related_name='budgets')
    
    created_by = models.ForeignKey('authentication.User', on_delete=models.SET_NULL, null=True, related_name='created_budgets')
    approved_by = models.ForeignKey('authentication.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_budgets')
    
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'finance_budgets'
        ordering = ['-fiscal_year', '-start_date']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['fiscal_year']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.code} - {self.name} ({self.fiscal_year})"
    
    @property
    def balance(self):
        return self.total_allocated - self.total_spent
    
    @property
    def utilization_percentage(self):
        if self.total_allocated > 0:
            return (self.total_spent / self.total_allocated) * 100
        return 0


class BudgetAllocation(TimeStampedModel):
    """Category-wise budget allocation"""
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='allocations')
    category = models.ForeignKey('finance.ExpenseCategory', on_delete=models.PROTECT, related_name='budget_allocations')
    
    allocated_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    spent_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'finance_budget_allocations'
        unique_together = ['budget', 'category']
        ordering = ['budget', 'category']
    
    def __str__(self):
        return f"{self.budget.code} - {self.category.name}: ${self.allocated_amount}"
    
    @property
    def balance(self):
        return self.allocated_amount - self.spent_amount
    
    @property
    def utilization_percentage(self):
        if self.allocated_amount > 0:
            return (self.spent_amount / self.allocated_amount) * 100
        return 0
