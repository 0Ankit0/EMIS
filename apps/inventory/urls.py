"""Inventory URL Configuration"""
from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('items/', views.item_list, name='item_list'),
    path('stock/', views.stock_report, name='stock_report'),
    path('purchase-orders/', views.purchase_order_list, name='po_list'),
    path('assets/', views.asset_list, name='asset_list'),
    path('requisitions/', views.requisition_list, name='requisition_list'),
    path('export/stock/', views.export_stock_csv, name='export_stock'),
]
