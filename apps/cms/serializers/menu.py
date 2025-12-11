"""Menu Serializers"""
from rest_framework import serializers
from ..models import Menu, MenuItem


class MenuItemSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    
    class Meta:
        model = MenuItem
        fields = [
            'id', 'title', 'url', 'page', 'target', 'css_class',
            'order', 'parent', 'children', 'is_active'
        ]
    
    def get_children(self, obj):
        children = obj.children.filter(is_active=True).order_by('order')
        return MenuItemSerializer(children, many=True).data


class MenuSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    
    class Meta:
        model = Menu
        fields = ['id', 'name', 'location', 'is_active', 'items', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_items(self, obj):
        # Only get top-level menu items
        items = obj.items.filter(parent__isnull=True, is_active=True).order_by('order')
        return MenuItemSerializer(items, many=True).data
