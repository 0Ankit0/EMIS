"""Inventory Admin Configuration"""
from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'parent_category', 'is_active']
    search_fields = ['name', 'code']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'location_type', 'in_charge', 'is_active']
    list_filter = ['location_type', 'is_active']


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'supplier_type', 'contact_person', 'email', 'phone', 'is_active']
    list_filter = ['supplier_type', 'is_active']
    search_fields = ['name', 'code', 'email']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'category', 'item_type', 'unit', 'unit_price', 'is_active']
    list_filter = ['category', 'item_type', 'is_active']
    search_fields = ['name', 'code']


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['item', 'location', 'quantity', 'reserved_quantity', 'available_quantity']


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['po_number', 'supplier', 'order_date', 'total_amount', 'status']
    list_filter = ['status']


@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_number', 'transaction_type', 'item', 'quantity', 'transaction_date']
    list_filter = ['transaction_type']


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['asset_number', 'item', 'location', 'status', 'assigned_to']
    list_filter = ['status']


@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = ['asset', 'maintenance_type', 'scheduled_date', 'status']
    list_filter = ['maintenance_type', 'status']


@admin.register(Requisition)
class RequisitionAdmin(admin.ModelAdmin):
    list_display = ['requisition_number', 'requested_by', 'request_date', 'status']
    list_filter = ['status']
