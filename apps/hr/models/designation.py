"""HR Designation Model"""
from django.db import models
from django.core.validators import MinValueValidator
from apps.core.models import TimeStampedModel
from .department import Department


class Designation(TimeStampedModel):
    """Job Designation/Position"""
    
    class Level(models.TextChoices):
        ENTRY = 'entry', 'Entry Level'
        JUNIOR = 'junior', 'Junior'
        MID = 'mid', 'Mid Level'
        SENIOR = 'senior', 'Senior'
        LEAD = 'lead', 'Lead'
        MANAGER = 'manager', 'Manager'
        DIRECTOR = 'director', 'Director'
        EXECUTIVE = 'executive', 'Executive'
    
    title = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=50, unique=True, db_index=True)
    description = models.TextField(blank=True)
    
    level = models.CharField(max_length=20, choices=Level.choices)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='designations')
    
    min_salary = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    max_salary = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    
    required_qualifications = models.TextField(blank=True)
    responsibilities = models.TextField(blank=True)
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'hr_designations'
        ordering = ['title']
        verbose_name = 'Designation'
        verbose_name_plural = 'Designations'
    
    def __str__(self):
        return self.title
