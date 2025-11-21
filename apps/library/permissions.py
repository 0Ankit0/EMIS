"""
Library Custom Permissions
"""
from rest_framework import permissions


class IsLibraryStaff(permissions.BasePermission):
    """
    Permission to only allow library staff to manage
    """
    def has_permission(self, request, view):
        return request.user and (request.user.is_staff or request.user.is_superuser)


class CanIssueBook(permissions.BasePermission):
    """
    Permission for issuing books
    """
    def has_permission(self, request, view):
        return request.user and (request.user.is_staff or request.user.is_superuser)
