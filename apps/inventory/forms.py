"""Inventory Forms"""
from django import forms
from .models import *


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'code', 'description', 'parent_category', 'is_active']


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'code', 'location_type', 'building', 'floor', 'room_number',
                  'capacity', 'in_charge', 'description', 'is_active']


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'code', 'supplier_type', 'contact_person', 'email', 'phone',
                  'address', 'city', 'state', 'pincode', 'gstin', 'pan',
                  'bank_name', 'account_number', 'ifsc_code', 'credit_days', 'rating']


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'code', 'item_type', 'category', 'description', 'specifications',
                  'unit', 'minimum_stock', 'maximum_stock', 'reorder_level',
                  'unit_price', 'manufacturer', 'model_number', 'barcode', 'image']


class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['supplier', 'order_date', 'expected_delivery_date', 'subtotal',
                  'tax_amount', 'shipping_charges', 'discount', 'payment_terms',
                  'delivery_address', 'notes']
        widgets = {
            'order_date': forms.DateInput(attrs={'type': 'date'}),
            'expected_delivery_date': forms.DateInput(attrs={'type': 'date'}),
        }


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['item', 'serial_number', 'location', 'purchase_date', 'purchase_price',
                  'current_value', 'depreciation_rate', 'warranty_expiry_date',
                  'assigned_to', 'status', 'condition', 'notes']
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'warranty_expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }


class RequisitionForm(forms.ModelForm):
    class Meta:
        model = Requisition
        fields = ['department', 'required_date', 'purpose']
        widgets = {
            'required_date': forms.DateInput(attrs={'type': 'date'}),
            'purpose': forms.Textarea(attrs={'rows': 4}),
        }
