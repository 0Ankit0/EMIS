"""
Reports Custom Permissions
"""
from rest_framework import permissions


class ReportPermission(permissions.BasePermission):
    """
    Custom permission for reports
    """
    
    def has_permission(self, request, view):
        # All authenticated users can list and view
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        
        # Only staff can create/update/delete templates
        if view.basename == 'reporttemplate':
            return request.user.is_staff
        
        # Users can manage their own generated reports and schedules
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Staff can do anything
        if request.user.is_staff:
            return True
        
        # For templates, check if user has access
        if hasattr(obj, 'is_public'):
            if obj.is_public:
                return True
            
            # Check roles
            user_roles = []
            if hasattr(request.user, 'student'):
                user_roles.append('student')
            if hasattr(request.user, 'faculty'):
                user_roles.append('faculty')
            
            if any(role in obj.roles_allowed for role in user_roles):
                return True
        
        # For generated reports and schedules, check ownership
        if hasattr(obj, 'generated_by'):
            return obj.generated_by == request.user
        
        if hasattr(obj, 'created_by'):
            return obj.created_by == request.user
        
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        return False


class IsReportsOwner(permissions.BasePermission):
    """
    Permission to only allow owners to edit
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner
        if hasattr(obj, 'created_by'):
            return obj.created_by == request.user
        if hasattr(obj, 'generated_by'):
            return obj.generated_by == request.user
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return False


class CanReportsManage(permissions.BasePermission):
    """
    Permission for managing reports items
    """
    def has_permission(self, request, view):
        # Check if user has manage permission
        return request.user and request.user.is_staff


class CanGenerateReport(permissions.BasePermission):
    """Permission to generate reports"""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Check if user can access the template
        if obj.is_public:
            return True
        
        if request.user.is_staff:
            return True
        
        user_roles = []
        if hasattr(request.user, 'student'):
            user_roles.append('student')
        if hasattr(request.user, 'faculty'):
            user_roles.append('faculty')
        
        return any(role in obj.roles_allowed for role in user_roles)


class CanViewGeneratedReport(permissions.BasePermission):
    """Permission to view generated reports"""
    
    def has_object_permission(self, request, view, obj):
        # Staff can view all
        if request.user.is_staff:
            return True
        
        # Users can view their own reports
        return obj.generated_by == request.user
