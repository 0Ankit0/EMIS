"""
Timetable Serializers
"""
from rest_framework import serializers
from .models import TimetableItem


class TimetableItemSerializer(serializers.ModelSerializer):
    """
    Serializer for TimetableItem
    """
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = TimetableItem
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


class TimetableItemListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing timetable items
    """
    class Meta:
        model = TimetableItem
        fields = ['id', 'name', 'status', 'created_at']
