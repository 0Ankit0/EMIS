from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner or admin
        if hasattr(obj, 'user'):
            return obj.user == request.user or request.user.is_staff
        
        return request.user.is_staff


class IsStudentOrAdmin(permissions.BasePermission):
    """
    Custom permission for student-specific views
    """
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            (hasattr(request.user, 'student_profile') or request.user.is_staff)
        )


class IsFacultyOrAdmin(permissions.BasePermission):
    """
    Custom permission for faculty-specific views
    """
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            (hasattr(request.user, 'faculty_profile') or request.user.is_staff)
        )
