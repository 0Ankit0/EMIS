"""
Library API Permissions
"""
from rest_framework import permissions


class IsLibraryStaff(permissions.BasePermission):
    """
    Permission to check if user is library staff
    """
    def has_permission(self, request, view):
        return request.user.is_staff or getattr(request.user, 'is_library_staff', False)


class CanIssueBook(permissions.BasePermission):
    """
    Permission to check if user can issue books
    """
    def has_permission(self, request, view):
        # Staff and library staff can issue books
        return request.user.is_staff or getattr(request.user, 'is_library_staff', False)
    
    def has_object_permission(self, request, view, obj):
        # Allow read for safe methods
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Staff can manage all issues
        if request.user.is_staff:
            return True
        
        # Users can manage their own issues
        if hasattr(obj, 'member') and hasattr(obj.member, 'user'):
            return obj.member.user == request.user
        
        return False
