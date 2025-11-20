"""
Admissions Admin Configuration
"""
from django.contrib import admin
from .models import Application, MeritList


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """
    Admin interface for Application
    """
    list_display = ['application_number', 'first_name', 'last_name', 'email', 'program', 'status', 'submitted_at', 'merit_score']
    list_filter = ['status', 'program', 'admission_year', 'admission_semester', 'gender']
    search_fields = ['application_number', 'first_name', 'last_name', 'email', 'phone']
    readonly_fields = ['application_number', 'created_at', 'updated_at']
    date_hierarchy = 'submitted_at'
    ordering = ['-submitted_at']
    
    fieldsets = (
        ('Application Information', {
            'fields': ('application_number', 'status', 'submitted_at')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'gender')
        }),
        ('Address', {
            'fields': ('address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country')
        }),
        ('Academic Background', {
            'fields': ('previous_school', 'previous_grade', 'gpa')
        }),
        ('Program Selection', {
            'fields': ('program', 'admission_year', 'admission_semester')
        }),
        ('Review & Merit', {
            'fields': ('reviewed_by', 'reviewed_at', 'review_notes', 'merit_score', 'rank')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(MeritList)
class MeritListAdmin(admin.ModelAdmin):
    """
    Admin interface for MeritList
    """
    list_display = ['name', 'program', 'admission_year', 'admission_semester', 'total_applications', 'is_published', 'published_at']
    list_filter = ['is_published', 'program', 'admission_year', 'admission_semester']
    search_fields = ['name', 'program']
    readonly_fields = ['generation_timestamp', 'created_at', 'updated_at']
    ordering = ['-generation_timestamp']
    
    fieldsets = (
        ('Merit List Information', {
            'fields': ('name', 'program', 'admission_year', 'admission_semester')
        }),
        ('Generation Details', {
            'fields': ('generated_by', 'generation_timestamp', 'criteria', 'version')
        }),
        ('Publication', {
            'fields': ('is_published', 'published_at')
        }),
        ('Statistics', {
            'fields': ('total_applications', 'cutoff_rank', 'cutoff_score')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
