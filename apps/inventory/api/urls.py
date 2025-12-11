"""Inventory API URLs"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'locations', views.LocationViewSet, basename='location')
router.register(r'suppliers', views.SupplierViewSet, basename='supplier')
router.register(r'items', views.ItemViewSet, basename='item')
router.register(r'stock', views.StockViewSet, basename='stock')
router.register(r'purchase-orders', views.PurchaseOrderViewSet, basename='purchase-order')
router.register(r'transactions', views.StockTransactionViewSet, basename='transaction')
router.register(r'assets', views.AssetViewSet, basename='asset')
router.register(r'maintenance', views.MaintenanceRecordViewSet, basename='maintenance')
router.register(r'requisitions', views.RequisitionViewSet, basename='requisition')

urlpatterns = [path('', include(router.urls))]
