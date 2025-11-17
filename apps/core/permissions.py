"""Custom permissions for EMIS"""
from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit objects.
    Read-only access is permitted for authenticated users.
    """
    
    def has_permission(self, request, view):
        # Read permissions are allowed for authenticated users
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Write permissions are only allowed to admins
        return request.user and request.user.is_authenticated and getattr(request.user, 'is_admin', False)


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners or admins to view/edit objects.
    """
    
    def has_object_permission(self, request, view, obj):
        # Admins can do anything
        if hasattr(request.user, 'is_admin') and request.user.is_admin:
            return True
        
        # Check if the object has an owner attribute
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'created_by'):
            return obj.created_by == request.user
        elif hasattr(obj, 'applicant'):
            return obj.applicant == request.user
        
        return False


class IsAuthenticated(permissions.BasePermission):
    """
    Permission that requires user to be authenticated.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class IsAdmin(permissions.BasePermission):
    """
    Permission that requires user to be an admin.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and getattr(request.user, 'is_admin', False)


class IsStaffOrAdmin(permissions.BasePermission):
    """
    Permission that requires user to be staff or admin.
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        return getattr(request.user, 'is_staff', False) or getattr(request.user, 'is_admin', False)


class IsFacultyOrAdmin(permissions.BasePermission):
    """
    Permission that requires user to be faculty or admin.
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Check if user has faculty role
        if hasattr(request.user, 'roles'):
            role_names = [role.name for role in request.user.roles.all()]
            return 'Faculty' in role_names or 'Admin' in role_names
        
        return getattr(request.user, 'is_admin', False)
