"""
Students Admin Configuration
"""
from django.contrib import admin
from .models import Student, Enrollment, AttendanceRecord, Transcript


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """
    Admin interface for Student
    """
    list_display = ['student_id', 'first_name', 'last_name', 'email', 'student_status', 'program', 'admission_year', 'created_at']
    list_filter = ['student_status', 'program', 'admission_year', 'batch', 'created_at']
    search_fields = ['student_id', 'first_name', 'last_name', 'email', 'phone']
    readonly_fields = ['student_id', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('student_id', 'first_name', 'last_name', 'email', 'phone')
        }),
        ('Academic Information', {
            'fields': ('program', 'batch', 'section', 'admission_year', 'student_status')
        }),
        ('Guardian Information', {
            'fields': ('guardian_name', 'guardian_phone', 'guardian_email', 'guardian_relation')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    """
    Admin interface for Enrollment
    """
    list_display = ['student', 'program', 'batch', 'status', 'start_date', 'created_at']
    list_filter = ['status', 'program', 'batch', 'start_date']
    search_fields = ['student__student_id', 'student__first_name', 'student__last_name', 'program']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'start_date'
    ordering = ['-start_date']


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    """
    Admin interface for AttendanceRecord
    """
    list_display = ['student', 'course', 'session_date', 'status', 'marked_at']
    list_filter = ['status', 'session_date', 'marked_at']
    search_fields = ['student__student_id', 'student__first_name', 'student__last_name']
    readonly_fields = ['marked_at', 'created_at', 'updated_at']
    date_hierarchy = 'session_date'
    ordering = ['-session_date']


@admin.register(Transcript)
class TranscriptAdmin(admin.ModelAdmin):
    """
    Admin interface for Transcript
    """
    list_display = ['student', 'transcript_type', 'cumulative_gpa', 'generated_at', 'is_certified']
    list_filter = ['transcript_type', 'is_certified', 'generated_at']
    search_fields = ['student__student_id', 'student__first_name', 'student__last_name']
    readonly_fields = ['generated_at', 'created_at', 'updated_at']
    date_hierarchy = 'generated_at'
    ordering = ['-generated_at']

