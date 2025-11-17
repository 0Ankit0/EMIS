"""
LMS models for EMIS
"""
from django.db import models
from apps.core.models import TimeStampedModel, AuditModel


class Course(AuditModel):
    """Course model for LMS"""
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    credits = models.IntegerField(default=3)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'lms_courses'
        ordering = ['code']
    
    def __str__(self):
        return f"{self.code} - {self.name}"
