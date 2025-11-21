"""
Reports Admin Configuration
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    ReportTemplate, GeneratedReport, ScheduledReport,
    ReportWidget, ReportFavorite, ReportAccessLog
)


@admin.register(ReportTemplate)
class ReportTemplateAdmin(admin.ModelAdmin):
    """Admin interface for ReportTemplate"""
    list_display = ['name', 'code', 'category', 'default_format', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'default_format', 'created_at']
    search_fields = ['name', 'code', 'description']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    ordering = ['category', 'name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'description', 'category')
        }),
        ('Data Configuration', {
            'fields': ('query_sql', 'data_source', 'parameters')
        }),
        ('Template Settings', {
            'fields': ('template_file', 'template_content')
        }),
        ('Format Settings', {
            'fields': ('supported_formats', 'default_format', 'page_size', 'orientation')
        }),
        ('Access Control', {
            'fields': ('roles_allowed', 'is_public')
        }),
        ('Status & Scheduling', {
            'fields': ('is_active', 'is_scheduled')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(GeneratedReport)
class GeneratedReportAdmin(admin.ModelAdmin):
    """Admin interface for GeneratedReport"""
    list_display = ['title', 'template', 'generated_by', 'format', 'status', 'generated_at', 'file_size_display']
    list_filter = ['status', 'format', 'generated_at', 'template__category']
    search_fields = ['title', 'description', 'template__name']
    readonly_fields = ['generated_at', 'file_size', 'generation_time', 'download_count', 'last_downloaded_at']
    date_hierarchy = 'generated_at'
    ordering = ['-generated_at']
    
    fieldsets = (
        ('Report Information', {
            'fields': ('template', 'title', 'description')
        }),
        ('Generation Details', {
            'fields': ('generated_by', 'generated_at', 'parameters')
        }),
        ('Output', {
            'fields': ('format', 'file', 'file_size', 'generation_time')
        }),
        ('Status', {
            'fields': ('status', 'error_message')
        }),
        ('Metadata', {
            'fields': ('record_count', 'download_count', 'last_downloaded_at')
        }),
        ('Archival', {
            'fields': ('expires_at', 'is_archived')
        }),
    )
    
    def file_size_display(self, obj):
        """Display file size in human readable format"""
        if obj.file_size:
            if obj.file_size < 1024:
                return f"{obj.file_size} B"
            elif obj.file_size < 1024 * 1024:
                return f"{obj.file_size / 1024:.2f} KB"
            else:
                return f"{obj.file_size / (1024 * 1024):.2f} MB"
        return "-"
    file_size_display.short_description = 'File Size'


@admin.register(ScheduledReport)
class ScheduledReportAdmin(admin.ModelAdmin):
    """Admin interface for ScheduledReport"""
    list_display = ['name', 'template', 'schedule_type', 'scheduled_time', 'is_active', 'last_run', 'next_run']
    list_filter = ['schedule_type', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'template__name']
    readonly_fields = ['last_run', 'next_run', 'created_at', 'updated_at']
    filter_horizontal = ['recipients']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'template')
        }),
        ('Schedule Configuration', {
            'fields': ('schedule_type', 'cron_expression', 'scheduled_time', 'timezone')
        }),
        ('Parameters', {
            'fields': ('parameters', 'format')
        }),
        ('Distribution', {
            'fields': ('recipients', 'recipient_emails')
        }),
        ('Status', {
            'fields': ('is_active', 'last_run', 'next_run')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ReportWidget)
class ReportWidgetAdmin(admin.ModelAdmin):
    """Admin interface for ReportWidget"""
    list_display = ['name', 'template', 'widget_type', 'order', 'width', 'is_active']
    list_filter = ['widget_type', 'is_active']
    search_fields = ['name', 'template__name']
    ordering = ['order', 'name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'template', 'widget_type')
        }),
        ('Configuration', {
            'fields': ('config', 'default_parameters')
        }),
        ('Layout', {
            'fields': ('order', 'width')
        }),
        ('Access Control', {
            'fields': ('roles_allowed', 'is_active')
        }),
    )


@admin.register(ReportFavorite)
class ReportFavoriteAdmin(admin.ModelAdmin):
    """Admin interface for ReportFavorite"""
    list_display = ['user', 'template', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'template__name']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'


@admin.register(ReportAccessLog)
class ReportAccessLogAdmin(admin.ModelAdmin):
    """Admin interface for ReportAccessLog"""
    list_display = ['user', 'template', 'action', 'ip_address', 'created_at']
    list_filter = ['action', 'created_at']
    search_fields = ['user__username', 'template__name', 'ip_address']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Access Information', {
            'fields': ('user', 'template', 'generated_report', 'action')
        }),
        ('Request Details', {
            'fields': ('ip_address', 'user_agent')
        }),
        ('Metadata', {
            'fields': ('metadata', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
