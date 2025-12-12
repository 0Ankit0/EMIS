"""Resource Group Model"""
from django.db import models


class ResourceGroup(models.Model):
    """Resource group for organizing permissions"""
    name = models.CharField(max_length=100, unique=True)
    module = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'resource_groups'
        ordering = ['module', 'name']
    
    def __str__(self):
        return f"{self.module}.{self.name}"
