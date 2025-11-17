from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.finance.api.fee_structures import FeeStructureViewSet
from apps.finance.api.invoices import InvoiceViewSet
from apps.finance.api.payments import PaymentViewSet
from apps.finance.api.reports import ReportViewSet

router = DefaultRouter()
router.register(r'fee-structures', FeeStructureViewSet, basename='fee-structure')
router.register(r'invoices', InvoiceViewSet, basename='invoice')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'reports', ReportViewSet, basename='report')

app_name = 'finance'
urlpatterns = [
    path('', include(router.urls)),
]
