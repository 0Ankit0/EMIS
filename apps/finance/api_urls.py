"""Finance API URLs"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'fee-structures', api_views.FeeStructureViewSet, basename='fee-structure')
router.register(r'invoices', api_views.InvoiceViewSet, basename='invoice')
router.register(r'payments', api_views.PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
]
