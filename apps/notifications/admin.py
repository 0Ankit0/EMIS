"""
Notifications Admin Configuration
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Notification, NotificationTemplate, NotificationPreference,
    ScheduledNotification, NotificationLog
)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin interface for Notification"""
    
    list_display = [
        'title', 'recipient', 'notification_type', 'is_read',
        'channels_display', 'created_at'
    ]
    list_filter = ['notification_type', 'is_read', 'created_at', 'email_sent', 'sms_sent']
    search_fields = ['title', 'message', 'recipient__username', 'recipient__email']
    readonly_fields = ['created_at', 'updated_at', 'read_at', 'email_sent_at', 'sms_sent_at', 'push_sent_at']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('recipient', 'sender', 'title', 'message', 'notification_type')
        }),
        ('Delivery', {
            'fields': ('channels', 'action_url', 'expires_at')
        }),
        ('Status', {
            'fields': ('is_read', 'read_at')
        }),
        ('Channel Status', {
            'fields': (
                ('email_sent', 'email_sent_at'),
                ('sms_sent', 'sms_sent_at'),
                ('push_sent', 'push_sent_at')
            )
        }),
        ('Related Object', {
            'fields': ('content_type', 'object_id'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('metadata', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def channels_display(self, obj):
        """Display channels as badges"""
        if not obj.channels:
            return '-'
        badges = []
        for channel in obj.channels:
            badges.append(f'<span class="badge">{channel}</span>')
        return format_html(' '.join(badges))
    channels_display.short_description = 'Channels'
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        """Mark selected notifications as read"""
        count = 0
        for notification in queryset:
            if not notification.is_read:
                notification.mark_as_read()
                count += 1
        self.message_user(request, f'{count} notifications marked as read')
    mark_as_read.short_description = 'Mark selected as read'
    
    def mark_as_unread(self, request, queryset):
        """Mark selected notifications as unread"""
        count = 0
        for notification in queryset:
            if notification.is_read:
                notification.mark_as_unread()
                count += 1
        self.message_user(request, f'{count} notifications marked as unread')
    mark_as_unread.short_description = 'Mark selected as unread'


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    """Admin interface for NotificationTemplate"""
    
    list_display = ['name', 'code', 'notification_type', 'is_active', 'created_at']
    list_filter = ['notification_type', 'is_active', 'created_at']
    search_fields = ['name', 'code', 'description']
    readonly_fields = ['created_at', 'updated_at']
    prepopulated_fields = {'code': ('name',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'description', 'is_active')
        }),
        ('Template Content', {
            'fields': ('title_template', 'message_template', 'template_variables')
        }),
        ('Settings', {
            'fields': ('notification_type', 'default_channels')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    """Admin interface for NotificationPreference"""
    
    list_display = [
        'user', 'enable_email', 'enable_sms', 'enable_push',
        'enable_in_app', 'quiet_hours_enabled'
    ]
    list_filter = ['enable_email', 'enable_sms', 'enable_push', 'enable_in_app']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Channel Preferences', {
            'fields': ('enable_email', 'enable_sms', 'enable_push', 'enable_in_app')
        }),
        ('Quiet Hours', {
            'fields': ('quiet_hours_enabled', 'quiet_hours_start', 'quiet_hours_end')
        }),
        ('Digest', {
            'fields': ('enable_daily_digest', 'daily_digest_time')
        }),
        ('Advanced', {
            'fields': ('notification_types',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ScheduledNotification)
class ScheduledNotificationAdmin(admin.ModelAdmin):
    """Admin interface for ScheduledNotification"""
    
    list_display = [
        'title', 'notification_type', 'scheduled_for', 'is_sent',
        'is_recurring', 'is_active', 'created_by'
    ]
    list_filter = ['notification_type', 'is_sent', 'is_recurring', 'is_active', 'scheduled_for']
    search_fields = ['title', 'message']
    readonly_fields = ['created_at', 'updated_at', 'sent_at']
    date_hierarchy = 'scheduled_for'
    filter_horizontal = ['recipients']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'message', 'notification_type')
        }),
        ('Recipients', {
            'fields': ('recipients', 'recipient_groups')
        }),
        ('Scheduling', {
            'fields': ('scheduled_for', 'is_sent', 'sent_at')
        }),
        ('Delivery', {
            'fields': ('channels', 'action_url')
        }),
        ('Template', {
            'fields': ('template', 'template_context'),
            'classes': ('collapse',)
        }),
        ('Recurrence', {
            'fields': ('is_recurring', 'recurrence_pattern')
        }),
        ('Status', {
            'fields': ('is_active', 'created_by')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Set created_by if not set"""
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    """Admin interface for NotificationLog"""
    
    list_display = ['notification', 'channel', 'is_successful', 'created_at']
    list_filter = ['channel', 'is_successful', 'created_at']
    search_fields = ['notification__title', 'error_message']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Notification', {
            'fields': ('notification', 'channel')
        }),
        ('Status', {
            'fields': ('is_successful', 'error_message')
        }),
        ('Metadata', {
            'fields': ('metadata', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

