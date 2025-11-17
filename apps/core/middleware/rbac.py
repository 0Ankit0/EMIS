"""
Role-Based Access Control (RBAC) middleware and decorators
"""
from functools import wraps
from django.core.exceptions import PermissionDenied
from apps.authentication.models import Permission, RolePermission
from apps.core.exceptions import AuthorizationException


def has_permission(user, resource_group_name: str, action: str) -> bool:
    """
    Check if user has permission for a specific action on a resource group
    
    Args:
        user: User instance
        resource_group_name: Resource group name (e.g., 'students.records')
        action: Action to check (e.g., 'view', 'create', 'update', 'delete')
    
    Returns:
        True if user has permission, False otherwise
    """
    if not user or not user.is_authenticated:
        return False
    
    # Superusers have all permissions
    if user.is_superuser:
        return True
    
    # Get user's roles
    user_roles = user.user_roles.select_related('role').filter(role__is_active=True)
    
    if not user_roles.exists():
        return False
    
    # Check if any of user's roles have the required permission
    for user_role in user_roles:
        role_permissions = RolePermission.objects.filter(
            role=user_role.role,
            permission__resource_group__name=resource_group_name,
            permission__action=action
        ).exists()
        
        if role_permissions:
            return True
    
    return False


def require_permission(resource_group: str, action: str):
    """
    Decorator to require specific permission for a view
    
    Usage:
        @require_permission('students.records', 'view')
        def my_view(request):
            ...
    
    Args:
        resource_group: Resource group name
        action: Required action
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if not has_permission(request.user, resource_group, action):
                raise AuthorizationException(
                    f"Permission denied: {resource_group}:{action}",
                    code='AUTH_002',
                    details={
                        'resource_group': resource_group,
                        'action': action,
                        'user': str(request.user),
                    }
                )
            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator


def require_any_permission(*permissions):
    """
    Decorator to require any of the specified permissions
    
    Usage:
        @require_any_permission(
            ('students.records', 'view'),
            ('students.records', 'update'),
        )
        def my_view(request):
            ...
    
    Args:
        permissions: Tuple of (resource_group, action) pairs
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            for resource_group, action in permissions:
                if has_permission(request.user, resource_group, action):
                    return view_func(request, *args, **kwargs)
            
            raise AuthorizationException(
                "Permission denied: insufficient privileges",
                code='AUTH_018',
                details={'required_permissions': [f"{rg}:{a}" for rg, a in permissions]}
            )
        return wrapped_view
    return decorator


def require_all_permissions(*permissions):
    """
    Decorator to require all of the specified permissions
    
    Usage:
        @require_all_permissions(
            ('students.records', 'view'),
            ('students.records', 'update'),
        )
        def my_view(request):
            ...
    
    Args:
        permissions: Tuple of (resource_group, action) pairs
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            missing = []
            for resource_group, action in permissions:
                if not has_permission(request.user, resource_group, action):
                    missing.append(f"{resource_group}:{action}")
            
            if missing:
                raise AuthorizationException(
                    "Permission denied: missing required permissions",
                    code='AUTH_018',
                    details={'missing_permissions': missing}
                )
            
            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator


class RBACMiddleware:
    """
    Middleware to add permission checking helpers to request
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Add permission checking method to request
        request.has_permission = lambda rg, action: has_permission(request.user, rg, action)
        
        response = self.get_response(request)
        return response
