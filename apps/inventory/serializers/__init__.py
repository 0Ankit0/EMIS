"""Inventory Serializers"""
from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    in_charge_name = serializers.CharField(source='in_charge.get_full_name', read_only=True)
    
    class Meta:
        model = Location
        fields = '__all__'


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    total_stock = serializers.SerializerMethodField()
    
    class Meta:
        model = Item
        fields = '__all__'
    
    def get_total_stock(self, obj):
        return Stock.objects.filter(item=obj).aggregate(
            total=models.Sum('quantity')
        )['total'] or 0


class StockSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    location_name = serializers.CharField(source='location.name', read_only=True)
    available_quantity = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Stock
        fields = '__all__'


class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    
    class Meta:
        model = PurchaseOrderItem
        fields = '__all__'
        read_only_fields = ['line_total']


class PurchaseOrderSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    items = PurchaseOrderItemSerializer(many=True, read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = PurchaseOrder
        fields = '__all__'
        read_only_fields = ['po_number', 'total_amount']


class StockTransactionSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    from_location_name = serializers.CharField(source='from_location.name', read_only=True)
    to_location_name = serializers.CharField(source='to_location.name', read_only=True)
    
    class Meta:
        model = StockTransaction
        fields = '__all__'
        read_only_fields = ['transaction_number']


class AssetSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    location_name = serializers.CharField(source='location.name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    
    class Meta:
        model = Asset
        fields = '__all__'


class MaintenanceRecordSerializer(serializers.ModelSerializer):
    asset_number = serializers.CharField(source='asset.asset_number', read_only=True)
    
    class Meta:
        model = MaintenanceRecord
        fields = '__all__'


class RequisitionItemSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    
    class Meta:
        model = RequisitionItem
        fields = '__all__'


class RequisitionSerializer(serializers.ModelSerializer):
    requested_by_name = serializers.CharField(source='requested_by.get_full_name', read_only=True)
    items = RequisitionItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Requisition
        fields = '__all__'
        read_only_fields = ['requisition_number']
