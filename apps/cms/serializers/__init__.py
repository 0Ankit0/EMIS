"""
Cms Serializers
"""
from rest_framework import serializers
from .models import CmsItem


class CmsItemSerializer(serializers.ModelSerializer):
    """
    Serializer for CmsItem
    """
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = CmsItem
        fields = [
            'id', 'name', 'description', 'status',
            'created_by', 'created_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_name(self, value):
        """Validate name field"""
        if len(value) < 3:
            raise serializers.ValidationError("Name must be at least 3 characters long")
        return value


class CmsItemListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing cms items
    """
    class Meta:
        model = CmsItem
        fields = ['id', 'name', 'status', 'created_at']
