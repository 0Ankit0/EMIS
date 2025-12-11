from apps.core.models import TimeStampedModel
from django.db import models

class Category(TimeStampedModel):
    """Item Category"""
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=50, unique=True, db_index=True)
    description = models.TextField(blank=True)
    parent_category = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subcategories'
    )
    is_active = models.BooleanField(default=True)
    class Meta:
        db_table = 'inventory_categories'
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    def __str__(self):
        return f"{self.code} - {self.name}"
