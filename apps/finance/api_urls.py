"""Finance API URLs"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import (
    FeeStructureViewSet,
    InvoiceViewSet,
    PaymentViewSet,
    ReportViewSet,
)

router = DefaultRouter()
router.register(r'fee-structures', FeeStructureViewSet, basename='fee-structure')
router.register(r'invoices', InvoiceViewSet, basename='invoice')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'reports', ReportViewSet, basename='report')

urlpatterns = [
    path('', include(router.urls)),
]


