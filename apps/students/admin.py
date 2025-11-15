"""
Student admin configuration
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Student, StudentStatus


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Admin interface for Student model"""
    
    list_display = [
        'student_number', 'full_name', 'email', 'status_badge',
        'admission_date', 'current_gpa', 'created_at'
    ]
    
    list_filter = [
        'status', 'gender', 'admission_date', 'graduation_date',
        'created_at'
    ]
    
    search_fields = [
        'student_number', 'first_name', 'last_name', 'email',
        'phone', 'city', 'country'
    ]
    
    readonly_fields = [
        'id', 'student_number', 'full_name', 'age', 'is_active',
        'is_graduated', 'created_at', 'updated_at', 'created_by',
        'updated_by'
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'id', 'student_number', 'status', 'user'
            )
        }),
        ('Personal Details', {
            'fields': (
                'first_name', 'middle_name', 'last_name', 'full_name',
                'email', 'phone', 'date_of_birth', 'age', 'gender',
                'nationality'
            )
        }),
        ('Address', {
            'fields': (
                'address', 'city', 'state', 'postal_code', 'country'
            ),
            'classes': ('collapse',)
        }),
        ('Emergency Contact', {
            'fields': (
                'emergency_contact_name', 'emergency_contact_phone',
                'emergency_contact_relationship'
            ),
            'classes': ('collapse',)
        }),
        ('Academic Information', {
            'fields': (
                'admission_date', 'graduation_date', 'degree_earned',
                'honors', 'current_gpa', 'is_active', 'is_graduated'
            )
        }),
        ('Audit Information', {
            'fields': (
                'created_at', 'updated_at', 'created_by', 'updated_by'
            ),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    actions = ['admit_students', 'suspend_students', 'make_active']
    
    def status_badge(self, obj):
        """Display status as colored badge"""
        colors = {
            StudentStatus.APPLICANT: '#6c757d',  # gray
            StudentStatus.ACTIVE: '#28a745',     # green
            StudentStatus.SUSPENDED: '#ffc107',  # yellow
            StudentStatus.WITHDRAWN: '#dc3545',  # red
            StudentStatus.GRADUATED: '#007bff',  # blue
            StudentStatus.ALUMNI: '#6610f2',     # purple
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def full_name(self, obj):
        """Display full name"""
        return obj.get_full_name()
    full_name.short_description = 'Full Name'
    
    @admin.action(description='Admit selected students')
    def admit_students(self, request, queryset):
        """Bulk admit students"""
        count = 0
        errors = []
        
        for student in queryset:
            try:
                student.admit()
                count += 1
            except ValueError as e:
                errors.append(f"{student.student_number}: {str(e)}")
        
        if count:
            self.message_user(request, f"Successfully admitted {count} student(s).")
        if errors:
            self.message_user(
                request,
                f"Errors: {'; '.join(errors)}",
                level='ERROR'
            )
    
    @admin.action(description='Suspend selected students')
    def suspend_students(self, request, queryset):
        """Bulk suspend students"""
        count = 0
        errors = []
        
        for student in queryset:
            try:
                student.suspend()
                count += 1
            except ValueError as e:
                errors.append(f"{student.student_number}: {str(e)}")
        
        if count:
            self.message_user(request, f"Successfully suspended {count} student(s).")
        if errors:
            self.message_user(
                request,
                f"Errors: {'; '.join(errors)}",
                level='ERROR'
            )
    
    @admin.action(description='Make selected students active')
    def make_active(self, request, queryset):
        """Bulk make students active"""
        count = queryset.update(status=StudentStatus.ACTIVE)
        self.message_user(request, f"Successfully made {count} student(s) active.")
    
    def has_delete_permission(self, request, obj=None):
        """Restrict deletion - only superusers can delete"""
        return request.user.is_superuser
