"""
Permission decorators for role-based access control on views
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def permission_required(allowed_roles=None, resource=None, action=None):
    """
    Decorator to check if user has required permissions
    
    Usage:
        @permission_required(allowed_roles=['is_staff', 'is_faculty'])
        def my_view(request):
            ...
    
    Args:
        allowed_roles: List of role flags ['is_superuser', 'is_staff', 'is_student', 'is_faculty']
        resource: Resource name (e.g., 'students', 'courses', 'finance')
        action: Action name (e.g., 'view', 'create', 'update', 'delete')
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            user = request.user
            
            # Superuser has access to everything
            if user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            # Check role-based permissions
            if allowed_roles:
                has_permission = False
                
                for role in allowed_roles:
                    if role == 'is_staff' and user.is_staff:
                        has_permission = True
                        break
                    elif role == 'is_student' and user.is_student:
                        has_permission = True
                        break
                    elif role == 'is_faculty' and user.is_faculty:
                        has_permission = True
                        break
                    elif role == 'is_parent' and user.is_parent:
                        has_permission = True
                        break
                
                # Also check custom roles from database
                if not has_permission and hasattr(user, 'user_roles'):
                    user_role_names = [ur.role.name.lower() for ur in user.user_roles.all()]
                    for role in allowed_roles:
                        if role.replace('is_', '') in user_role_names:
                            has_permission = True
                            break
                
                if not has_permission:
                    messages.error(
                        request, 
                        f'You do not have permission to access this page. Required role: {", ".join(allowed_roles)}'
                    )
                    return redirect('core:dashboard')
            
            # Check resource-based permissions (with Permission model)
            if resource and action:
                from .permissions_utils import user_has_permission
                if not user_has_permission(user, resource, action):
                    messages.error(
                        request,
                        f'You do not have permission to {action} {resource}.'
                    )
                    return redirect('core:dashboard')
            
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator


def admin_required(view_func):
    """Decorator to require admin/staff access"""
    return permission_required(allowed_roles=['is_staff'])(view_func)


def student_required(view_func):
    """Decorator to require student access"""
    return permission_required(allowed_roles=['is_student'])(view_func)


def faculty_required(view_func):
    """Decorator to require faculty access"""
    return permission_required(allowed_roles=['is_faculty'])(view_func)


def staff_or_faculty_required(view_func):
    """Decorator to require staff or faculty access"""
    return permission_required(allowed_roles=['is_staff', 'is_faculty'])(view_func)


def student_or_faculty_required(view_func):
    """Decorator to require student or faculty access"""
    return permission_required(allowed_roles=['is_student', 'is_faculty'])(view_func)
