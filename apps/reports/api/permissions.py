"""
Reports API Permissions
"""
from rest_framework import permissions


class ReportPermission(permissions.BasePermission):
    """
    Permission to check if user can access reports
    """
    def has_permission(self, request, view):
        # Allow read for authenticated users
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        
        # Only staff can create/update/delete reports
        return request.user.is_staff
    
    def has_object_permission(self, request, view, obj):
        # Allow read for authenticated users
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        
        # Only staff can modify reports
        return request.user.is_staff
