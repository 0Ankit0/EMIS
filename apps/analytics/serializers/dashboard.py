"""Dashboard serializers"""
from rest_framework import serializers
from apps.analytics.models import DashboardMetric


class DashboardMetricResponseSerializer(serializers.ModelSerializer):
    """Serializer for dashboard metric responses"""
    
    is_stale = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = DashboardMetric
        fields = [
            'id',
            'metric_key',
            'metric_name',
            'description',
            'computed_value',
            'last_refreshed',
            'refresh_frequency',
            'category',
            'is_active',
            'is_stale',
            'created_at',
            'updated_at',
        ]


class DashboardSummarySerializer(serializers.Serializer):
    """Serializer for complete dashboard summary"""
    
    admissions_metrics = serializers.DictField()
    attendance_metrics = serializers.DictField()
    finance_metrics = serializers.DictField()
    course_metrics = serializers.DictField()
    last_updated = serializers.DateTimeField()
