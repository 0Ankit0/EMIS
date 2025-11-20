"""
Attendance Permissions
"""
from rest_framework import permissions


class CanMarkAttendance(permissions.BasePermission):
    """Permission to mark attendance"""
    
    def has_permission(self, request, view):
        return request.user.is_staff or hasattr(request.user, 'faculty')


class CanViewAttendance(permissions.BasePermission):
    """Permission to view attendance"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated
