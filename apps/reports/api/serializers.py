"""
Reports API Serializers
"""
from rest_framework import serializers
from ..models import ReportTemplate, GeneratedReport


class ReportTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportTemplate
        fields = '__all__'


class ReportTemplateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportTemplate
        fields = ['id', 'name', 'created_at']


class GeneratedReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedReport
        fields = '__all__'


class GeneratedReportListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedReport
        fields = ['id', 'template', 'created_at']


class ScheduledReportSerializer(serializers.Serializer):
    """Placeholder for ScheduledReport"""
    pass


class ReportWidgetSerializer(serializers.Serializer):
    """Placeholder for ReportWidget"""
    pass


class ReportFavoriteSerializer(serializers.Serializer):
    """Placeholder for ReportFavorite"""
    pass


class ReportAccessLogSerializer(serializers.Serializer):
    """Placeholder for ReportAccessLog"""
    pass
