from django.contrib import admin
from .models import (
    Dashboard, Widget, QuickLink, Announcement, AnnouncementView,
    StudentPortalProfile, FacultyPortalProfile, PortalActivity, PortalSettings
)


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'is_active', 'created_at']
    list_filter = ['role', 'is_active', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = [
        ('Basic Information', {
            'fields': ['user', 'role', 'is_active']
        }),
        ('Configuration', {
            'fields': ['layout_config', 'theme_settings', 'widget_preferences']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at']
        }),
    ]


@admin.register(Widget)
class WidgetAdmin(admin.ModelAdmin):
    list_display = ['name', 'widget_type', 'is_active', 'order', 'created_at']
    list_filter = ['widget_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['order', 'name']


@admin.register(QuickLink)
class QuickLinkAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_external', 'is_active', 'order']
    list_filter = ['category', 'is_external', 'is_active']
    search_fields = ['title', 'description', 'url']
    ordering = ['order', 'title']


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'priority', 'is_published', 'publish_date', 'expiry_date', 'views_count']
    list_filter = ['priority', 'is_published', 'publish_date', 'created_at']
    search_fields = ['title', 'content']
    filter_horizontal = ['target_users']
    readonly_fields = ['views_count', 'created_at', 'updated_at']
    fieldsets = [
        ('Basic Information', {
            'fields': ['title', 'content', 'author', 'priority']
        }),
        ('Targeting', {
            'fields': ['target_roles', 'target_users']
        }),
        ('Publishing', {
            'fields': ['is_published', 'publish_date', 'expiry_date']
        }),
        ('Attachments', {
            'fields': ['attachments']
        }),
        ('Statistics', {
            'fields': ['views_count', 'created_at', 'updated_at']
        }),
    ]


@admin.register(AnnouncementView)
class AnnouncementViewAdmin(admin.ModelAdmin):
    list_display = ['announcement', 'user', 'viewed_at']
    list_filter = ['viewed_at']
    search_fields = ['announcement__title', 'user__username']
    readonly_fields = ['viewed_at']


@admin.register(StudentPortalProfile)
class StudentPortalProfileAdmin(admin.ModelAdmin):
    list_display = ['student', 'last_login', 'login_count', 'created_at']
    list_filter = ['last_login', 'created_at']
    search_fields = ['student__user__username', 'student__registration_number']
    readonly_fields = ['last_login', 'login_count', 'created_at', 'updated_at']


@admin.register(FacultyPortalProfile)
class FacultyPortalProfileAdmin(admin.ModelAdmin):
    list_display = ['faculty', 'last_login', 'login_count', 'created_at']
    list_filter = ['last_login', 'created_at']
    search_fields = ['faculty__user__username', 'faculty__employee_id']
    readonly_fields = ['last_login', 'login_count', 'created_at', 'updated_at']


@admin.register(PortalActivity)
class PortalActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'created_at', 'ip_address']
    list_filter = ['activity_type', 'created_at']
    search_fields = ['user__username', 'description']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'


@admin.register(PortalSettings)
class PortalSettingsAdmin(admin.ModelAdmin):
    list_display = ['key', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['key', 'description']
    readonly_fields = ['created_at', 'updated_at']
