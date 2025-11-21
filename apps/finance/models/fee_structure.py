"""Fee structure model for finance app"""
from django.db import models
from django.core.validators import MinValueValidator
from apps.core.models import TimeStampedModel


class FeeStructure(TimeStampedModel):
    """
    Fee structure model with program-specific components, installment rules, and late fee policy
    """
    
    # Basic information
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, default='')
    
    # Program/Course association
    program = models.CharField(max_length=100, blank=True, default='', help_text="Program name (e.g., 'Computer Science BS')")
    academic_year = models.CharField(max_length=20, blank=True, default='')
    semester = models.CharField(max_length=50, blank=True, default='')
    
    # Fee components (JSON field to store flexible fee breakdown)
    components = models.JSONField(
        default=dict,
        help_text="Fee components as JSON: {'tuition': 5000, 'lab': 500, 'library': 100}"
    )
    
    # Total amount (calculated from components)
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    
    # Installment rules (JSON field)
    installment_rules = models.JSONField(
        default=dict,
        blank=True,
        help_text="Installment rules: {'enabled': true, 'count': 3, 'schedule': [...]}"
    )
    
    # Late fee policy (JSON field)
    late_fee_policy = models.JSONField(
        default=dict,
        blank=True,
        help_text="Late fee policy: {'percentage': 5, 'flat_fee': 100, 'grace_days': 7}"
    )
    
    # Validity period
    valid_from = models.DateField()
    valid_to = models.DateField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'finance_fee_structures'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['program']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    def calculate_total(self):
        """Calculate total amount from components"""
        if not self.components:
            return 0
        return sum(float(value) for value in self.components.values())
