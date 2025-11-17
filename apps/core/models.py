"""
Base models for EMIS
"""
from django.db import models
from django.contrib.auth import get_user_model
import uuid


class TimeStampedModel(models.Model):
    """Abstract base model with created and updated timestamps"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class SoftDeleteModel(models.Model):
    """Abstract base model with soft delete"""
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """Soft delete"""
        from django.utils import timezone
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        """Permanent delete"""
        super().delete()


class AuditModel(TimeStampedModel):
    """Abstract base model with audit fields"""
    created_by = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_created'
    )
    updated_by = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_updated'
    )

    class Meta:
        abstract = True


class Program(TimeStampedModel):
    """Academic program/degree model"""
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    degree_type = models.CharField(max_length=50)  # e.g., Bachelor, Master, Diploma
    duration_years = models.IntegerField(default=4)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'programs'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.code} - {self.name}"
