"""
Courses Admin Configuration
"""
from django.contrib import admin
from .models import Course, Module, Assignment, Submission, GradeRecord


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Admin interface for Course
    """
    list_display = ['code', 'title', 'department', 'semester', 'credits', 'created_at']
    list_filter = ['department', 'semester', 'academic_year']
    search_fields = ['code', 'title', 'description', 'department']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['code']
    
    fieldsets = (
        ('Course Information', {
            'fields': ('code', 'title', 'description', 'syllabus')
        }),
        ('Academic Details', {
            'fields': ('credits', 'department', 'semester', 'academic_year')
        }),
        ('Prerequisites', {
            'fields': ('prerequisites',),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('status', 'created_by')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    """
    Admin interface for Module
    """
    list_display = ['title', 'course', 'sequence_order', 'content_type', 'duration_minutes', 'is_published']
    list_filter = ['is_published', 'content_type', 'course']
    search_fields = ['title', 'description', 'content']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['course', 'sequence_order']


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    """
    Admin interface for Assignment
    """
    list_display = ['title', 'course', 'due_date']
    list_filter = ['course', 'due_date']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'due_date'
    ordering = ['-due_date']


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    """
    Admin interface for Submission
    """
    list_display = ['assignment', 'student']
    list_filter = ['assignment']
    search_fields = ['student__first_name', 'student__last_name', 'assignment__title']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['assignment']


@admin.register(GradeRecord)
class GradeRecordAdmin(admin.ModelAdmin):
    """
    Admin interface for GradeRecord
    """
    list_display = ['student', 'course', 'semester']
    list_filter = ['semester', 'academic_year']
    search_fields = ['student__first_name', 'student__last_name', 'course__title']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-academic_year', 'semester']



