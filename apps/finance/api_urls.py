"""Finance API URLs"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'fee-structures', api_views.FeeStructureViewSet, basename='fee-structure')
router.register(r'invoices', api_views.InvoiceViewSet, basename='invoice')
router.register(r'payments', api_views.PaymentViewSet, basename='payment')
router.register(r'expense-categories', api_views.ExpenseCategoryViewSet, basename='expense-category')
router.register(r'expenses', api_views.ExpenseViewSet, basename='expense')
router.register(r'budgets', api_views.BudgetViewSet, basename='budget')
router.register(r'budget-allocations', api_views.BudgetAllocationViewSet, basename='budget-allocation')
router.register(r'scholarships', api_views.ScholarshipViewSet, basename='scholarship')
router.register(r'scholarship-applications', api_views.ScholarshipApplicationViewSet, basename='scholarship-application')

urlpatterns = [
    path('', include(router.urls)),
]
