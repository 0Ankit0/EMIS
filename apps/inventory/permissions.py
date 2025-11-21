"""Inventory Custom Permissions"""
from rest_framework import permissions


class IsInventoryManager(permissions.BasePermission):
    """Permission for inventory managers"""
    
    def has_permission(self, request, view):
        return request.user and (
            request.user.is_staff or
            request.user.groups.filter(name__in=['Inventory Manager', 'Store Keeper']).exists()
        )


class CanApprovePurchaseOrders(permissions.BasePermission):
    """Permission to approve purchase orders"""
    
    def has_permission(self, request, view):
        return request.user and (
            request.user.is_staff or
            request.user.groups.filter(name__in=['Purchase Manager', 'Finance Manager']).exists()
        )


class CanManageAssets(permissions.BasePermission):
    """Permission to manage assets"""
    
    def has_permission(self, request, view):
        return request.user and (
            request.user.is_staff or
            request.user.groups.filter(name__in=['Asset Manager', 'Inventory Manager']).exists()
        )


class CanApproveRequisitions(permissions.BasePermission):
    """Permission to approve requisitions"""
    
    def has_permission(self, request, view):
        return request.user and (
            request.user.is_staff or
            request.user.groups.filter(name__in=['Inventory Manager', 'Department Head']).exists()
        )
