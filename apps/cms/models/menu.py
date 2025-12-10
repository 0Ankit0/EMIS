import uuid
from django.db import models
from apps.authentication.models import User

class Menu(models.Model):
    """Navigation menus"""
    LOCATIONS = [
        ('header', 'Header'),
        ('footer', 'Footer'),
        ('sidebar', 'Sidebar'),
        ('mobile', 'Mobile'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=20, choices=LOCATIONS)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'cms_menus'
        ordering = ['name']
    def __str__(self):
        return self.name
