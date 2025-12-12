"""
LMS API Permissions
"""
from rest_framework import permissions


class IsLmsOwner(permissions.BasePermission):
    """
    Permission to check if user is the owner of the LMS object
    """
    def has_object_permission(self, request, view, obj):
        # Allow read for safe methods
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Check if user owns the object
        if hasattr(obj, 'student'):
            return obj.student == request.user
        if hasattr(obj, 'user'):
            return obj.user == request.user
        if hasattr(obj, 'instructor'):
            return obj.instructor == request.user
        
        return False


class CanLmsManage(permissions.BasePermission):
    """
    Permission to check if user can manage LMS content
    """
    def has_permission(self, request, view):
        # Staff and instructors can manage
        return request.user.is_staff or hasattr(request.user, 'is_instructor')
    
    def has_object_permission(self, request, view, obj):
        # Staff can manage everything
        if request.user.is_staff:
            return True
        
        # Instructors can manage their own content
        if hasattr(obj, 'instructor'):
            return obj.instructor == request.user
        
        return False
