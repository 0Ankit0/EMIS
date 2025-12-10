"""
Transport Serializers
"""
from rest_framework import serializers
from .models import TransportItem


class TransportItemSerializer(serializers.ModelSerializer):
    """
    Serializer for TransportItem
    """
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = TransportItem
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


class TransportItemListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing transport items
    """
    class Meta:
        model = TransportItem
        fields = ['id', 'name', 'status', 'created_at']
