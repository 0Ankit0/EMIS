import uuid
from django.db import models
from .role import Role
from .permission import Permission
from .user import User

class RolePermission(models.Model):
    """
    Through model for Role-Permission relationship
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    granted_at = models.DateTimeField(auto_now_add=True)
    granted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    class Meta:
        db_table = 'role_permissions'
        unique_together = ['role', 'permission']
    def __str__(self):
        return f"{self.role.name} - {self.permission.name}"
