from rest_framework import serializers
from ..models.category import Category

class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'color', 'description']
    
    def validate_color(self, value):
        if value and not value.startswith('#'):
            raise serializers.ValidationError("Color must be a valid hex code starting with '#'.")
        if value and len(value) != 7:
            raise serializers.ValidationError("Color must be a 7-character hex code (e.g., #FFFFFF).")
        return value

class CategoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'color', 'description', 'updated_by']
        extra_kwargs = {
            'name': {'required': False},
            'color': {'required': False},
            'description': {'required': False},
        }
    
    def validate_color(self, value):
        if value and not value.startswith('#'):
            raise serializers.ValidationError("Color must be a valid hex code starting with '#'.")
        if value and len(value) != 7:
            raise serializers.ValidationError("Color must be a 7-character hex code (e.g., #FFFFFF).")
        return value

class CategoryResponseSerializer(serializers.ModelSerializer):
    event_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['ukid', 'name', 'color', 'description', 'event_count', 'created_at', 'updated_at']
        read_only_fields = ['ukid', 'created_at', 'updated_at']
    
    def get_event_count(self, obj):
        return obj.events.count()