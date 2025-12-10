from django.db import models
from apps.core.models import TimeStampedModel

class Department(TimeStampedModel):
    """Academic Department"""
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    head = models.ForeignKey('Faculty', on_delete=models.SET_NULL, null=True, blank=True, related_name='headed_department')
    is_active = models.BooleanField(default=True)
    class Meta:
        db_table = 'faculty_departments'
        ordering = ['name']
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
    def __str__(self):
        return f"{self.code} - {self.name}"
