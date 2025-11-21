"""Finance Custom Permissions"""
from rest_framework import permissions


class IsFinanceAdmin(permissions.BasePermission):
    """Permission for finance administrators"""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class CanManageInvoices(permissions.BasePermission):
    """Permission to manage invoices"""
    
    def has_permission(self, request, view):
        return request.user and (
            request.user.is_staff or 
            request.user.groups.filter(name='Finance Manager').exists()
        )


class CanProcessPayments(permissions.BasePermission):
    """Permission to process payments"""
    
    def has_permission(self, request, view):
        return request.user and (
            request.user.is_staff or
            request.user.groups.filter(name__in=['Finance Manager', 'Cashier']).exists()
        )


class CanApproveExpenses(permissions.BasePermission):
    """Permission to approve expenses"""
    
    def has_permission(self, request, view):
        return request.user and (
            request.user.is_staff or
            request.user.groups.filter(name__in=['Finance Manager', 'Department Head']).exists()
        )


class CanManageBudgets(permissions.BasePermission):
    """Permission to manage budgets"""
    
    def has_permission(self, request, view):
        return request.user and (
            request.user.is_staff or
            request.user.groups.filter(name='Finance Manager').exists()
        )


class CanViewFinancialReports(permissions.BasePermission):
    """Permission to view financial reports"""
    
    def has_permission(self, request, view):
        return request.user and (
            request.user.is_staff or
            request.user.groups.filter(name__in=['Finance Manager', 'Administrator']).exists()
        )


class IsInvoiceOwner(permissions.BasePermission):
    """Permission for invoice owner (student)"""
    
    def has_object_permission(self, request, view, obj):
        # Read permissions for invoice owner
        if request.method in permissions.SAFE_METHODS:
            return obj.student.user == request.user or request.user.is_staff
        
        # Write permissions only for staff
        return request.user.is_staff


class IsExpenseRequester(permissions.BasePermission):
    """Permission for expense requester"""
    
    def has_object_permission(self, request, view, obj):
        # Read permissions for requester or approvers
        if request.method in permissions.SAFE_METHODS:
            return (
                obj.requested_by == request.user or
                request.user.is_staff or
                request.user.groups.filter(name__in=['Finance Manager', 'Department Head']).exists()
            )
        
        # Update permissions
        if request.method in ['PUT', 'PATCH']:
            # Only requester can update draft expenses
            if obj.status == 'draft':
                return obj.requested_by == request.user
            # Approvers can update other statuses
            return request.user.is_staff or request.user.groups.filter(name='Finance Manager').exists()
        
        return False


class CanManageScholarships(permissions.BasePermission):
    """Permission to manage scholarships"""
    
    def has_permission(self, request, view):
        return request.user and (
            request.user.is_staff or
            request.user.groups.filter(name__in=['Finance Manager', 'Academic Affairs']).exists()
        )


class IsScholarshipApplicant(permissions.BasePermission):
    """Permission for scholarship applicant"""
    
    def has_object_permission(self, request, view, obj):
        # Read permissions for applicant or reviewers
        if request.method in permissions.SAFE_METHODS:
            return (
                obj.student.user == request.user or
                request.user.is_staff
            )
        
        # Only applicant can update submitted applications
        if obj.status == 'submitted':
            return obj.student.user == request.user
        
        # Reviewers can update other statuses
        return request.user.is_staff
