"""
Role and Permission management service
"""
from django.db import transaction
from apps.authentication.models import Role, Permission, ResourceGroup, RolePermission, UserRole
from apps.core.exceptions import NotFoundException, ValidationException
from apps.authentication.models import AuditLog


class RoleService:
    """Service for role and permission management"""
    
    @staticmethod
    def create_role(name, description='', actor=None):
        """Create a new role"""
        if Role.objects.filter(name=name).exists():
            raise ValidationException(f"Role '{name}' already exists", code='CORE_003')
        
        role = Role.objects.create(
            name=name,
            description=description,
            is_active=True
        )
        
        if actor:
            AuditLog.objects.create(
                actor=actor,
                action='create',
                target_model='Role',
                target_id=str(role.id),
                outcome='success',
                details={'role_name': name}
            )
        
        return role
    
    @staticmethod
    def get_role_by_id(role_id):
        """Get role by ID"""
        try:
            return Role.objects.prefetch_related('role_permissions__permission').get(id=role_id)
        except Role.DoesNotExist:
            raise NotFoundException(f"Role with ID {role_id} not found", code='AUTH_015')
    
    @staticmethod
    def get_all_roles(is_active=None):
        """Get all roles"""
        queryset = Role.objects.prefetch_related('role_permissions__permission')
        
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)
        
        return queryset.order_by('name')
    
    @staticmethod
    @transaction.atomic
    def assign_permissions_to_role(role_id, permission_ids, actor=None):
        """Assign multiple permissions to a role"""
        role = RoleService.get_role_by_id(role_id)
        
        # Remove existing permissions
        RolePermission.objects.filter(role=role).delete()
        
        # Add new permissions
        for permission_id in permission_ids:
            try:
                permission = Permission.objects.get(id=permission_id)
                RolePermission.objects.create(
                    role=role,
                    permission=permission,
                    created_by=actor
                )
            except Permission.DoesNotExist:
                raise NotFoundException(f"Permission {permission_id} not found", code='AUTH_016')
        
        if actor:
            AuditLog.objects.create(
                actor=actor,
                action='permission_change',
                target_model='Role',
                target_id=str(role.id),
                outcome='success',
                details={'permission_count': len(permission_ids)}
            )
        
        return role
    
    @staticmethod
    def assign_role_to_user(user, role_id, actor=None):
        """Assign a role to a user"""
        role = RoleService.get_role_by_id(role_id)
        
        # Check if already assigned
        if UserRole.objects.filter(user=user, role=role).exists():
            raise ValidationException(f"User already has role '{role.name}'", code='CORE_003')
        
        user_role = UserRole.objects.create(user=user, role=role)
        
        if actor:
            AuditLog.objects.create(
                actor=actor,
                action='role_change',
                target_model='User',
                target_id=str(user.id),
                outcome='success',
                details={'role_assigned': role.name}
            )
        
        return user_role
    
    @staticmethod
    def remove_role_from_user(user, role_id, actor=None):
        """Remove a role from a user"""
        role = RoleService.get_role_by_id(role_id)
        
        user_role = UserRole.objects.filter(user=user, role=role).first()
        if not user_role:
            raise NotFoundException(f"User does not have role '{role.name}'", code='CORE_002')
        
        user_role.delete()
        
        if actor:
            AuditLog.objects.create(
                actor=actor,
                action='role_change',
                target_model='User',
                target_id=str(user.id),
                outcome='success',
                details={'role_removed': role.name}
            )
        
        return True
    
    @staticmethod
    def create_resource_group(name, description, module, actor=None):
        """Create a new resource group"""
        if ResourceGroup.objects.filter(name=name).exists():
            raise ValidationException(f"Resource group '{name}' already exists", code='CORE_003')
        
        resource_group = ResourceGroup.objects.create(
            name=name,
            description=description,
            module=module
        )
        
        if actor:
            AuditLog.objects.create(
                actor=actor,
                action='create',
                target_model='ResourceGroup',
                target_id=str(resource_group.id),
                outcome='success'
            )
        
        return resource_group
    
    @staticmethod
    def create_permission(resource_group_id, action, description='', actor=None):
        """Create a new permission"""
        try:
            resource_group = ResourceGroup.objects.get(id=resource_group_id)
        except ResourceGroup.DoesNotExist:
            raise NotFoundException("Resource group not found", code='CORE_002')
        
        # Check if permission already exists
        if Permission.objects.filter(resource_group=resource_group, action=action).exists():
            raise ValidationException(
                f"Permission '{resource_group.name}:{action}' already exists",
                code='CORE_003'
            )
        
        permission = Permission.objects.create(
            resource_group=resource_group,
            action=action,
            description=description
        )
        
        if actor:
            AuditLog.objects.create(
                actor=actor,
                action='create',
                target_model='Permission',
                target_id=str(permission.id),
                outcome='success'
            )
        
        return permission
