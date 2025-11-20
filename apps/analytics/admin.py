"""
Analytics Admin Configuration
"""
from django.contrib import admin
from .models import DashboardMetric, Report, AnalyticsQuery


@admin.register(DashboardMetric)
class DashboardMetricAdmin(admin.ModelAdmin):
    """
    Admin interface for DashboardMetric
    """
    list_display = ['metric_name', 'category', 'is_active', 'last_computed_at']
    list_filter = ['category', 'is_active', 'last_computed_at']
    search_fields = ['metric_key', 'metric_name']
    readonly_fields = ['last_computed_at', 'created_at', 'updated_at']
    ordering = ['category', 'metric_name']
    
    fieldsets = (
        ('Metric Information', {
            'fields': ('metric_key', 'metric_name', 'category')
        }),
        ('Data', {
            'fields': ('computed_value', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('last_computed_at', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """
    Admin interface for Report
    """
    list_display = ['title', 'report_type', 'format', 'status', 'generated_by', 'created_at']
    list_filter = ['report_type', 'status', 'format', 'is_scheduled', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    filter_horizontal = ['shared_with']
    
    fieldsets = (
        ('Report Details', {
            'fields': ('title', 'report_type', 'description')
        }),
        ('Configuration', {
            'fields': ('parameters', 'filters', 'format')
        }),
        ('Status', {
            'fields': ('status', 'error_message')
        }),
        ('Generated Data', {
            'fields': ('report_data', 'file_path')
        }),
        ('Access Control', {
            'fields': ('generated_by', 'shared_with')
        }),
        ('Scheduling', {
            'fields': ('is_scheduled', 'schedule_frequency', 'next_run')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AnalyticsQuery)
class AnalyticsQueryAdmin(admin.ModelAdmin):
    """
    Admin interface for AnalyticsQuery
    """
    list_display = ['name', 'query_type', 'is_public', 'is_featured', 'usage_count', 'created_by']
    list_filter = ['query_type', 'is_public', 'is_featured', 'created_at']
    search_fields = ['name', 'description', 'query_type']
    readonly_fields = ['usage_count', 'last_used_at', 'created_at', 'updated_at']
    ordering = ['-usage_count', '-created_at']
    
    fieldsets = (
        ('Query Information', {
            'fields': ('name', 'description', 'query_type')
        }),
        ('Configuration', {
            'fields': ('query_config', 'visualization_config')
        }),
        ('Access & Visibility', {
            'fields': ('created_by', 'is_public', 'is_featured')
        }),
        ('Usage Statistics', {
            'fields': ('usage_count', 'last_used_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
