from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Role, UserRole


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'is_student', 'is_faculty', 'is_staff']
    list_filter = ['is_student', 'is_faculty', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('phone', 'profile_photo', 'is_student', 'is_faculty', 'is_parent')}),
    )


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'created_at']
    list_filter = ['role']
    search_fields = ['user__username', 'role__name']
