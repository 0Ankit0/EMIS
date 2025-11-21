"""
Notifications Custom Permissions
"""
from rest_framework import permissions


class IsNotificationsOwner(permissions.BasePermission):
    """Permission to only allow notification recipients to access"""
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to notification recipient
        if request.method in permissions.SAFE_METHODS:
            return obj.recipient == request.user
        
        # Write permissions are only allowed to the recipient
        return obj.recipient == request.user


class CanNotificationsManage(permissions.BasePermission):
    """Permission for managing notifications (admin only)"""
    
    def has_permission(self, request, view):
        # Check if user has manage permission
        return request.user and request.user.is_staff
    
    def has_object_permission(self, request, view, obj):
        # Staff can manage all notifications
        return request.user and request.user.is_staff


class IsNotificationRecipient(permissions.BasePermission):
    """Permission to check if user is the notification recipient"""
    
    def has_object_permission(self, request, view, obj):
        return obj.recipient == request.user
