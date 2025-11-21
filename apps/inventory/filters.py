"""Inventory Filters"""
import django_filters
from .models import Item, Stock, PurchaseOrder, Asset, Requisition


class ItemFilter(django_filters.FilterSet):
    item_type = django_filters.ChoiceFilter(choices=Item.ITEM_TYPE_CHOICES)
    
    class Meta:
        model = Item
        fields = ['category', 'item_type', 'is_active']


class StockFilter(django_filters.FilterSet):
    class Meta:
        model = Stock
        fields = ['item', 'location']


class PurchaseOrderFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=PurchaseOrder.STATUS_CHOICES)
    
    class Meta:
        model = PurchaseOrder
        fields = ['supplier', 'status']


class AssetFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Asset.STATUS_CHOICES)
    
    class Meta:
        model = Asset
        fields = ['status', 'location']


class RequisitionFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Requisition.STATUS_CHOICES)
    
    class Meta:
        model = Requisition
        fields = ['status', 'requested_by']
