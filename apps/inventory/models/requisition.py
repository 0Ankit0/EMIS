from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from apps.core.models import TimeStampedModel

User = get_user_model()


class Requisition(TimeStampedModel):
    """Stock/Item Requisition"""
    
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
        PARTIALLY_FULFILLED = 'partially_fulfilled', 'Partially Fulfilled'
        FULFILLED = 'fulfilled', 'Fulfilled'
        CANCELLED = 'cancelled', 'Cancelled'
    
    requisition_number = models.CharField(max_length=50, unique=True, db_index=True)
    
    requested_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='requisitions')
    department = models.CharField(max_length=200)
    
    request_date = models.DateField(default=timezone.now)
    required_date = models.DateField()
    
    purpose = models.TextField()
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True)
    
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_requisitions')
    approval_date = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    
    class Meta:
        db_table = 'inventory_requisitions'
        ordering = ['-request_date']
        verbose_name = 'Requisition'
        verbose_name_plural = 'Requisitions'
        indexes = [
            models.Index(fields=['requisition_number']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.requisition_number} - {self.requested_by.get_full_name()}"
    
    def save(self, *args, **kwargs):
        if not self.requisition_number:
            year = timezone.now().year
            from django.db.models import Count
            count = Requisition.objects.filter(created_at__year=year).count() + 1
            self.requisition_number = f"REQ-{year}-{count:06d}"
        super().save(*args, **kwargs)

