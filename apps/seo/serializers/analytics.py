"""Analytics Serializer"""
from rest_framework import serializers
from ..models import SEOAnalytics


class SEOAnalyticsSerializer(serializers.ModelSerializer):
    platform_display = serializers.CharField(source='get_platform_display', read_only=True)
    
    class Meta:
        model = SEOAnalytics
        fields = [
            'id', 'name', 'platform', 'platform_display',
            'tracking_id', 'script_code',
            'in_head', 'in_body_start', 'in_body_end',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
