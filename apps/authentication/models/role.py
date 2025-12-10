import uuid
from django.db import models
from .permission import Permission

class Role(models.Model):
    """
    Role model for RBAC
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    permissions = models.ManyToManyField(Permission, through='RolePermission')
    is_system = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'roles'
        ordering = ['name']
    def __str__(self):
        return self.name
