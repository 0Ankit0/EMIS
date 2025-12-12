"""
Notifications API Permissions
"""
from rest_framework import permissions


class IsNotificationsOwner(permissions.BasePermission):
    """
    Permission to check if user is the owner of the notification
    """
    def has_object_permission(self, request, view, obj):
        # Allow read for safe methods
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Check if user owns the notification
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        return False


class CanNotificationsManage(permissions.BasePermission):
    """
    Permission to check if user can manage notifications
    """
    def has_permission(self, request, view):
        # Staff can manage notifications
        return request.user.is_staff
    
    def has_object_permission(self, request, view, obj):
        # Staff can manage everything
        return request.user.is_staff
