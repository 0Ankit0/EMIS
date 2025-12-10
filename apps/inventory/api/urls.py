"""Inventory API URLs"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'categories', api_views.CategoryViewSet, basename='category')
router.register(r'locations', api_views.LocationViewSet, basename='location')
router.register(r'suppliers', api_views.SupplierViewSet, basename='supplier')
router.register(r'items', api_views.ItemViewSet, basename='item')
router.register(r'stock', api_views.StockViewSet, basename='stock')
router.register(r'purchase-orders', api_views.PurchaseOrderViewSet, basename='purchase-order')
router.register(r'transactions', api_views.StockTransactionViewSet, basename='transaction')
router.register(r'assets', api_views.AssetViewSet, basename='asset')
router.register(r'maintenance', api_views.MaintenanceRecordViewSet, basename='maintenance')
router.register(r'requisitions', api_views.RequisitionViewSet, basename='requisition')

urlpatterns = [path('', include(router.urls))]
