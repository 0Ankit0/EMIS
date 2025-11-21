"""
Courses Custom Permissions
"""
from rest_framework import permissions


class IsCoursesOwner(permissions.BasePermission):
    """
    Permission to only allow owners to edit
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner
        return obj.created_by == request.user


class CanCoursesManage(permissions.BasePermission):
    """
    Permission for managing courses items
    """
    def has_permission(self, request, view):
        # Check if user has manage permission
        return request.user and request.user.is_staff
