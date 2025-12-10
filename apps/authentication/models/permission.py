import uuid
from django.db import models

class Permission(models.Model):
    """
    Permission model for RBAC
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    resource_group = models.CharField(max_length=100, db_index=True)
    action = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'permissions'
        ordering = ['resource_group', 'action']
        unique_together = ['resource_group', 'action']
    def __str__(self):
        return f"{self.resource_group}:{self.action}"
