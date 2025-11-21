"""Hostel Custom Permissions"""
from rest_framework import permissions


class IsHostelAdmin(permissions.BasePermission):
    """Permission for hostel administrators"""
    
    def has_permission(self, request, view):
        return request.user and (
            request.user.is_staff or
            request.user.groups.filter(name='Hostel Admin').exists()
        )


class IsWarden(permissions.BasePermission):
    """Permission for hostel wardens"""
    
    def has_permission(self, request, view):
        return request.user and (
            request.user.is_staff or
            hasattr(request.user, 'faculty_profile') and
            request.user.faculty_profile.managed_hostels.exists()
        )


class CanAllocateRooms(permissions.BasePermission):
    """Permission to allocate rooms"""
    
    def has_permission(self, request, view):
        return request.user and (
            request.user.is_staff or
            request.user.groups.filter(name__in=['Hostel Admin', 'Warden']).exists()
        )


class IsComplaintOwner(permissions.BasePermission):
    """Permission for complaint owner"""
    
    def has_object_permission(self, request, view, obj):
        # Read permissions for complaint owner or staff
        if request.method in permissions.SAFE_METHODS:
            return (
                obj.student.user == request.user or
                request.user.is_staff
            )
        
        # Write permissions only for staff
        return request.user.is_staff


class IsOutingRequestOwner(permissions.BasePermission):
    """Permission for outing request owner"""
    
    def has_object_permission(self, request, view, obj):
        # Read permissions for request owner or approvers
        if request.method in permissions.SAFE_METHODS:
            return (
                obj.student.user == request.user or
                request.user.is_staff
            )
        
        # Students can only update pending requests
        if obj.status == 'pending':
            return obj.student.user == request.user
        
        # Approvers can update other statuses
        return request.user.is_staff


class CanViewVisitorLogs(permissions.BasePermission):
    """Permission to view visitor logs"""
    
    def has_permission(self, request, view):
        return request.user and (
            request.user.is_staff or
            request.user.groups.filter(name__in=['Hostel Admin', 'Warden', 'Security']).exists()
        )
