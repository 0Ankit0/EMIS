"""Redirect Serializer"""
from rest_framework import serializers
from ..models import Redirect


class RedirectSerializer(serializers.ModelSerializer):
    redirect_type_display = serializers.CharField(source='get_redirect_type_display', read_only=True)
    
    class Meta:
        model = Redirect
        fields = [
            'id', 'old_path', 'new_path', 'redirect_type', 'redirect_type_display',
            'is_active', 'hit_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'hit_count', 'created_at', 'updated_at']
    
    def validate(self, attrs):
        if attrs['old_path'] == attrs['new_path']:
            raise serializers.ValidationError("Old path and new path cannot be the same")
        return attrs
