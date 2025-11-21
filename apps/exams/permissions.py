"""
Exams Custom Permissions
"""
from rest_framework import permissions


class IsExamCreator(permissions.BasePermission):
    """
    Permission to only allow exam creators to edit
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the creator
        return obj.created_by == request.user


class CanManageExams(permissions.BasePermission):
    """
    Permission for managing exams
    """
    def has_permission(self, request, view):
        # Check if user has manage permission (staff or faculty)
        return request.user and (request.user.is_staff or hasattr(request.user, 'faculty'))


class CanViewResults(permissions.BasePermission):
    """
    Permission for viewing exam results
    """
    def has_permission(self, request, view):
        # Students can view their own results, faculty and staff can view all
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Staff and faculty can view all results
        if request.user.is_staff or hasattr(request.user, 'faculty'):
            return True
        
        # Students can only view their own results
        if hasattr(request.user, 'student'):
            return obj.student == request.user.student
        
        return False


class CanEnterResults(permissions.BasePermission):
    """
    Permission for entering/editing exam results
    """
    def has_permission(self, request, view):
        # Only staff and faculty can enter results
        return request.user and (request.user.is_staff or hasattr(request.user, 'faculty'))
