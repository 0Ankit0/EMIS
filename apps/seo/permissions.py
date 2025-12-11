"""SEO Permissions"""
from rest_framework import permissions


class CanManageSEO(permissions.BasePermission):
    """Permission to manage SEO settings"""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user and (
            request.user.is_staff or
            request.user.is_superuser or
            request.user.has_perm('seo.change_seometadata')
        )


class CanViewSEOMetadata(permissions.BasePermission):
    """Permission to view SEO metadata"""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class CanManageRedirects(permissions.BasePermission):
    """Permission to manage redirects"""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user and (
            request.user.is_staff or
            request.user.has_perm('seo.change_redirect')
        )
