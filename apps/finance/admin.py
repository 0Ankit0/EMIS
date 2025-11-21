"""Finance Admin Configuration"""
from django.contrib import admin
from .models import (
    FeeStructure, Invoice, Payment, ExpenseCategory, Expense,
    Budget, BudgetAllocation, Scholarship, ScholarshipApplication
)


@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'program', 'academic_year', 'total_amount', 'is_active']
    list_filter = ['is_active', 'program', 'academic_year']
    search_fields = ['name', 'code', 'program']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'student', 'amount_due', 'amount_paid', 'balance', 'status', 'due_date']
    list_filter = ['status', 'academic_year', 'semester']
    search_fields = ['invoice_number', 'student__user__email']
    readonly_fields = ['invoice_number', 'balance', 'created_at', 'updated_at']
    date_hierarchy = 'invoice_date'
    ordering = ['-invoice_date']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['receipt_number', 'invoice', 'student', 'amount_paid', 'method', 'payment_date']
    list_filter = ['method', 'payment_date']
    search_fields = ['receipt_number', 'transaction_id', 'student__user__email']
    readonly_fields = ['receipt_number', 'created_at', 'updated_at']
    date_hierarchy = 'payment_date'
    ordering = ['-payment_date']


@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'parent', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'code']
    ordering = ['name']


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['expense_number', 'title', 'category', 'total_amount', 'status', 'expense_date']
    list_filter = ['status', 'priority', 'category']
    search_fields = ['expense_number', 'title', 'vendor_name']
    readonly_fields = ['expense_number', 'total_amount', 'created_at', 'updated_at']
    date_hierarchy = 'expense_date'
    ordering = ['-expense_date']


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'fiscal_year', 'total_allocated', 'total_spent', 'balance', 'status']
    list_filter = ['status', 'fiscal_year', 'period_type']
    search_fields = ['name', 'code']
    readonly_fields = ['balance', 'utilization_percentage', 'created_at', 'updated_at']
    ordering = ['-fiscal_year']


@admin.register(BudgetAllocation)
class BudgetAllocationAdmin(admin.ModelAdmin):
    list_display = ['budget', 'category', 'allocated_amount', 'spent_amount', 'balance']
    list_filter = ['budget', 'category']
    readonly_fields = ['balance', 'utilization_percentage', 'created_at', 'updated_at']


@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'scholarship_type', 'amount', 'total_slots', 'filled_slots', 'status']
    list_filter = ['status', 'scholarship_type']
    search_fields = ['name', 'code']
    readonly_fields = ['filled_slots', 'available_slots', 'created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(ScholarshipApplication)
class ScholarshipApplicationAdmin(admin.ModelAdmin):
    list_display = ['scholarship', 'student', 'status', 'application_date', 'awarded_amount']
    list_filter = ['status', 'scholarship']
    search_fields = ['student__user__email', 'scholarship__name']
    readonly_fields = ['application_date', 'created_at', 'updated_at']
    date_hierarchy = 'application_date'
    ordering = ['-application_date']
