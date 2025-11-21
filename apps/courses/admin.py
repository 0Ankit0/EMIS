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
    list_display = ['code', 'title', 'department', 'semester', 'credits', 'status', 'created_at']
    list_filter = ['status', 'department', 'semester', 'academic_year']
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
    list_display = ['title', 'course', 'module', 'due_date', 'max_marks', 'status']
    list_filter = ['status', 'course', 'due_date']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'due_date'
    ordering = ['-due_date']


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    """
    Admin interface for Submission
    """
    list_display = ['assignment', 'student', 'submission_date', 'marks_obtained', 'status']
    list_filter = ['status', 'submission_date']
    search_fields = ['student__first_name', 'student__last_name', 'assignment__title']
    readonly_fields = ['submission_date', 'created_at', 'updated_at']
    date_hierarchy = 'submission_date'
    ordering = ['-submission_date']


@admin.register(GradeRecord)
class GradeRecordAdmin(admin.ModelAdmin):
    """
    Admin interface for GradeRecord
    """
    list_display = ['student', 'course', 'marks_obtained', 'total_marks', 'grade', 'semester']
    list_filter = ['grade', 'semester', 'academic_year']
    search_fields = ['student__first_name', 'student__last_name', 'course__title']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-academic_year', 'semester']



