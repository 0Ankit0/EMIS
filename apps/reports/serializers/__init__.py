"""
Reports Serializers
"""
from rest_framework import serializers
from ..models import (
    ReportTemplate, GeneratedReport, ScheduledReport,
    ReportWidget, ReportFavorite, ReportAccessLog
)


class ReportTemplateSerializer(serializers.ModelSerializer):
    """Serializer for ReportTemplate"""
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = ReportTemplate
        fields = [
            'id', 'name', 'code', 'description', 'category',
            'query_sql', 'data_source', 'parameters',
            'template_file', 'template_content',
            'supported_formats', 'default_format', 'page_size', 'orientation',
            'roles_allowed', 'is_public', 'is_active', 'is_scheduled',
            'created_by', 'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ReportTemplateListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing report templates"""
    class Meta:
        model = ReportTemplate
        fields = ['id', 'name', 'code', 'category', 'description', 'default_format', 'is_active']


class GeneratedReportSerializer(serializers.ModelSerializer):
    """Serializer for GeneratedReport"""
    template_name = serializers.CharField(source='template.name', read_only=True)
    generated_by_name = serializers.CharField(source='generated_by.get_full_name', read_only=True)
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = GeneratedReport
        fields = [
            'id', 'template', 'template_name', 'title', 'description',
            'generated_by', 'generated_by_name', 'generated_at',
            'parameters', 'format', 'file', 'file_url', 'file_size',
            'status', 'error_message', 'record_count', 'generation_time',
            'download_count', 'last_downloaded_at', 'expires_at', 'is_archived'
        ]
        read_only_fields = [
            'id', 'generated_at', 'file_size', 'generation_time',
            'download_count', 'last_downloaded_at'
        ]
    
    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
        return None


class GeneratedReportListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing generated reports"""
    template_name = serializers.CharField(source='template.name', read_only=True)
    
    class Meta:
        model = GeneratedReport
        fields = [
            'id', 'template_name', 'title', 'format', 'status',
            'generated_at', 'file_size', 'download_count'
        ]


class ScheduledReportSerializer(serializers.ModelSerializer):
    """Serializer for ScheduledReport"""
    template_name = serializers.CharField(source='template.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = ScheduledReport
        fields = [
            'id', 'template', 'template_name', 'name', 'description',
            'schedule_type', 'cron_expression', 'scheduled_time', 'timezone',
            'parameters', 'format', 'recipients', 'recipient_emails',
            'is_active', 'last_run', 'next_run',
            'created_by', 'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'last_run', 'next_run', 'created_at', 'updated_at']


class ReportWidgetSerializer(serializers.ModelSerializer):
    """Serializer for ReportWidget"""
    template_name = serializers.CharField(source='template.name', read_only=True)
    
    class Meta:
        model = ReportWidget
        fields = [
            'id', 'name', 'template', 'template_name', 'widget_type',
            'config', 'default_parameters', 'order', 'width',
            'roles_allowed', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ReportFavoriteSerializer(serializers.ModelSerializer):
    """Serializer for ReportFavorite"""
    template_name = serializers.CharField(source='template.name', read_only=True)
    template_category = serializers.CharField(source='template.category', read_only=True)
    
    class Meta:
        model = ReportFavorite
        fields = [
            'id', 'user', 'template', 'template_name', 'template_category',
            'custom_parameters', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ReportAccessLogSerializer(serializers.ModelSerializer):
    """Serializer for ReportAccessLog"""
    template_name = serializers.CharField(source='template.name', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = ReportAccessLog
        fields = [
            'id', 'template', 'template_name', 'generated_report',
            'user', 'user_name', 'action', 'ip_address', 'user_agent',
            'metadata', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
