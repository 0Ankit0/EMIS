"""
Student admin configuration
"""
from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin
from .models import Student, Enrollment


@admin.register(Student)
class StudentAdmin(UserAdmin):
    """Admin interface for Student model"""
    
    list_display = [
        'student_id', 'username', 'email', 'student_status',
        'admission_year', 'program'
    ]
    
    list_filter = [
        'student_status', 'admission_year', 'program'
    ]
    
    search_fields = [
        'student_id', 'username', 'email', 'first_name', 'last_name'
    ]
    
    readonly_fields = ['student_id', 'created_at', 'updated_at', 'last_login']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'gender')
        }),
        ('Student Info', {
            'fields': ('student_id', 'student_status', 'admission_year', 'program', 'batch', 'section')
        }),
        ('Guardian Info', {
            'fields': ('guardian_name', 'guardian_phone', 'guardian_email', 'guardian_relation')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    
    ordering = ['-created_at']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    """Admin interface for Enrollment model"""
    
    list_display = ['student', 'program', 'batch', 'status', 'start_date']
    list_filter = ['status', 'program', 'start_date']
    search_fields = ['student__student_id', 'student__username', 'program']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-start_date']

