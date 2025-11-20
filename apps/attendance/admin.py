"""
Attendance Admin Configuration
"""
from django.contrib import admin
from .models import AttendanceRecord, AttendanceSession, AttendancePolicy, AttendanceReport


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    """
    Admin interface for AttendanceRecord
    """
    list_display = ['student', 'course', 'date', 'status', 'marked_by', 'marked_at']
    list_filter = ['status', 'date', 'course']
    search_fields = ['student__first_name', 'student__last_name', 'course__name']
    readonly_fields = ['marked_by', 'marked_at', 'created_at', 'updated_at']
    date_hierarchy = 'date'
    ordering = ['-date', 'student']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('student', 'course', 'session', 'date')
        }),
        ('Attendance Details', {
            'fields': ('status', 'time_in', 'time_out', 'remarks')
        }),
        ('Leave Documentation', {
            'fields': ('leave_document',)
        }),
        ('Metadata', {
            'fields': ('marked_by', 'marked_at', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AttendanceSession)
class AttendanceSessionAdmin(admin.ModelAdmin):
    """
    Admin interface for AttendanceSession
    """
    list_display = ['title', 'course', 'date', 'session_type', 'status', 'attendance_rate']
    list_filter = ['status', 'session_type', 'date', 'course']
    search_fields = ['title', 'course__name']
    readonly_fields = ['total_students', 'present_count', 'absent_count', 'late_count', 'created_at', 'updated_at']
    date_hierarchy = 'date'
    ordering = ['-date', '-start_time']
    
    fieldsets = (
        ('Session Details', {
            'fields': ('course', 'title', 'session_type')
        }),
        ('Schedule', {
            'fields': ('date', 'start_time', 'end_time', 'status')
        }),
        ('Location', {
            'fields': ('room', 'building')
        }),
        ('Instructor', {
            'fields': ('instructor',)
        }),
        ('Attendance Statistics', {
            'fields': ('total_students', 'present_count', 'absent_count', 'late_count')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def attendance_rate(self, obj):
        return f"{obj.get_attendance_rate()}%"
    attendance_rate.short_description = 'Attendance Rate'


@admin.register(AttendancePolicy)
class AttendancePolicyAdmin(admin.ModelAdmin):
    """
    Admin interface for AttendancePolicy
    """
    list_display = ['name', 'minimum_percentage', 'warning_threshold', 'is_active']
    list_filter = ['is_active', 'applies_to_program']
    search_fields = ['name', 'description']
    ordering = ['name']
    
    fieldsets = (
        ('Policy Information', {
            'fields': ('name', 'description', 'is_active')
        }),
        ('Requirements', {
            'fields': ('minimum_percentage', 'grace_period_days')
        }),
        ('Thresholds', {
            'fields': ('warning_threshold', 'penalty_threshold')
        }),
        ('Applicability', {
            'fields': ('applies_to_program', 'applies_to_year')
        }),
    )


@admin.register(AttendanceReport)
class AttendanceReportAdmin(admin.ModelAdmin):
    """
    Admin interface for AttendanceReport
    """
    list_display = ['title', 'report_type', 'format', 'start_date', 'end_date', 'generated_by', 'created_at']
    list_filter = ['report_type', 'format', 'created_at']
    search_fields = ['title']
    readonly_fields = ['generated_by', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Report Details', {
            'fields': ('title', 'report_type', 'format')
        }),
        ('Date Range', {
            'fields': ('start_date', 'end_date')
        }),
        ('Configuration', {
            'fields': ('filters',)
        }),
        ('Generated Data', {
            'fields': ('report_data', 'file_path')
        }),
        ('Metadata', {
            'fields': ('generated_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
