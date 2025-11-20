"""
Authentication Admin Configuration
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Role, UserRole, LoginAttempt, PasswordResetToken,
    UserSession, SecurityLog, APIKey
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Enhanced User admin"""
    list_display = [
        'email', 'username', 'first_name', 'last_name',
        'account_status', 'two_factor_enabled', 'is_staff', 'created_at'
    ]
    list_filter = [
        'account_status', 'is_staff', 'is_superuser',
        'two_factor_enabled', 'email_verified', 'created_at'
    ]
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-created_at']
    readonly_fields = [
        'id', 'created_at', 'updated_at', 'last_login',
        'password_changed_at', 'last_activity_at'
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('email', 'username', 'password')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'phone', 'bio', 'profile_photo')
        }),
        ('User Types', {
            'fields': ('is_student', 'is_faculty', 'is_parent', 'is_admin')
        }),
        ('Security', {
            'fields': (
                'two_factor_enabled', 'two_factor_secret',
                'password_changed_at', 'password_reset_required',
                'failed_login_attempts', 'account_locked_until',
                'email_verified'
            )
        }),
        ('Account Status', {
            'fields': (
                'account_status', 'suspension_reason', 'suspended_until',
                'is_active', 'is_staff', 'is_superuser'
            )
        }),
        ('Permissions', {
            'fields': ('groups', 'user_permissions')
        }),
        ('Session Info', {
            'fields': (
                'last_login', 'last_login_ip', 'last_activity_at',
                'max_concurrent_sessions'
            )
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at', 'created_by'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """Role admin"""
    list_display = ['name', 'is_system_role', 'priority', 'is_active', 'created_at']
    list_filter = ['is_system_role', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['-priority', 'name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    """User Role assignment admin"""
    list_display = ['user', 'role', 'assigned_by', 'assigned_at', 'expires_at', 'is_active']
    list_filter = ['role', 'is_active', 'assigned_at']
    search_fields = ['user__email', 'user__username', 'role__name']
    ordering = ['-assigned_at']
    readonly_fields = ['assigned_at']


@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    """Login attempt tracking admin"""
    list_display = [
        'email', 'ip_address', 'success', 'failure_reason',
        'two_factor_required', 'attempted_at'
    ]
    list_filter = [
        'success', 'two_factor_required', 'two_factor_verified', 'attempted_at'
    ]
    search_fields = ['email', 'ip_address']
    ordering = ['-attempted_at']
    readonly_fields = ['attempted_at']
    
    def has_add_permission(self, request):
        return False


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    """Password reset token admin"""
    list_display = ['user', 'is_used', 'created_at', 'expires_at']
    list_filter = ['is_used', 'created_at']
    search_fields = ['user__email', 'token']
    ordering = ['-created_at']
    readonly_fields = ['token', 'created_at', 'used_at']
    
    def has_add_permission(self, request):
        return False


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    """User session admin"""
    list_display = [
        'user', 'device_type', 'ip_address', 'is_active',
        'last_activity', 'created_at'
    ]
    list_filter = ['is_active', 'device_type', 'created_at']
    search_fields = ['user__email', 'ip_address', 'session_key']
    ordering = ['-last_activity']
    readonly_fields = ['session_key', 'created_at', 'last_activity']
    
    def has_add_permission(self, request):
        return False


@admin.register(SecurityLog)
class SecurityLogAdmin(admin.ModelAdmin):
    """Security log admin"""
    list_display = [
        'user', 'event_type', 'severity', 'risk_score',
        'ip_address', 'created_at'
    ]
    list_filter = ['event_type', 'severity', 'created_at']
    search_fields = ['user__email', 'description', 'ip_address']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    """API Key admin"""
    list_display = [
        'user', 'name', 'is_active', 'usage_count',
        'last_used_at', 'created_at', 'expires_at'
    ]
    list_filter = ['is_active', 'created_at']
    search_fields = ['user__email', 'name', 'key']
    ordering = ['-created_at']
    readonly_fields = ['key', 'usage_count', 'last_used_at', 'created_at']
