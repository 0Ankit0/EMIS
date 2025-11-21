"""HR Custom Permissions"""
from rest_framework import permissions


class IsHRAdmin(permissions.BasePermission):
    """Permission for HR administrators"""
    
    def has_permission(self, request, view):
        return request.user and (
            request.user.is_staff or
            request.user.groups.filter(name='HR Admin').exists()
        )


class IsHRManager(permissions.BasePermission):
    """Permission for HR managers"""
    
    def has_permission(self, request, view):
        return request.user and (
            request.user.is_staff or
            request.user.groups.filter(name__in=['HR Admin', 'HR Manager']).exists()
        )


class CanManagePayroll(permissions.BasePermission):
    """Permission to manage payroll"""
    
    def has_permission(self, request, view):
        return request.user and (
            request.user.is_staff or
            request.user.groups.filter(name__in=['HR Admin', 'Payroll Manager']).exists()
        )


class CanApproveLeaves(permissions.BasePermission):
    """Permission to approve leaves"""
    
    def has_permission(self, request, view):
        return request.user and (
            request.user.is_staff or
            request.user.groups.filter(name__in=['HR Manager', 'Department Head']).exists()
        )


class IsEmployeeOwner(permissions.BasePermission):
    """Permission for employee to access own data"""
    
    def has_object_permission(self, request, view, obj):
        # Read permissions for employee owner
        if request.method in permissions.SAFE_METHODS:
            return obj.user == request.user or request.user.is_staff
        
        # Write permissions only for staff
        return request.user.is_staff


class CanViewRecruitment(permissions.BasePermission):
    """Permission to view recruitment data"""
    
    def has_permission(self, request, view):
        return request.user and (
            request.user.is_staff or
            request.user.groups.filter(name__in=['HR Admin', 'Recruitment Team']).exists()
        )


class CanConductReviews(permissions.BasePermission):
    """Permission to conduct performance reviews"""
    
    def has_permission(self, request, view):
        return request.user and (
            request.user.is_staff or
            request.user.groups.filter(name__in=['HR Manager', 'Department Head']).exists()
        )
