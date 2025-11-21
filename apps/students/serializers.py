"""
Students Serializers
"""
from rest_framework import serializers
from .models import StudentsItem


class StudentsItemSerializer(serializers.ModelSerializer):
    """
    Serializer for StudentsItem
    """
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = StudentsItem
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


class StudentsItemListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing students items
    """
    class Meta:
        model = StudentsItem
        fields = ['id', 'name', 'status', 'created_at']
