"""
Faculty Admin Configuration
"""
from django.contrib import admin
from .models import (
    Department, Faculty, FacultyQualification, FacultyExperience,
    FacultyAttendance, FacultyLeave, FacultyPublication, FacultyAward
)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """Admin interface for Department"""
    list_display = ['code', 'name', 'head', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'code', 'description']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['code']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('code', 'name', 'description', 'head', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    """Admin interface for Faculty"""
    list_display = ['employee_id', 'get_full_name', 'department', 'designation', 
                    'status', 'official_email', 'phone']
    list_filter = ['status', 'department', 'designation', 'employment_type', 
                   'is_teaching', 'is_research_active', 'is_hod']
    search_fields = ['employee_id', 'first_name', 'last_name', 'official_email', 
                     'phone', 'personal_email']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date_of_joining'
    ordering = ['employee_id']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'employee_id', 'first_name', 'middle_name', 'last_name',
                      'date_of_birth', 'gender', 'blood_group', 'nationality', 
                      'religion', 'caste_category')
        }),
        ('Contact Information', {
            'fields': ('phone', 'alternate_phone', 'personal_email', 'official_email')
        }),
        ('Address', {
            'fields': ('current_address', 'permanent_address', 'city', 'state', 
                      'pincode', 'country'),
            'classes': ('collapse',)
        }),
        ('Government IDs', {
            'fields': ('aadhar_number', 'pan_number', 'passport_number'),
            'classes': ('collapse',)
        }),
        ('Professional Information', {
            'fields': ('department', 'designation', 'specialization', 'employment_type',
                      'date_of_joining', 'date_of_leaving', 'probation_period_months',
                      'is_probation_completed', 'confirmation_date')
        }),
        ('Status & Roles', {
            'fields': ('status', 'is_teaching', 'is_research_active', 'is_hod')
        }),
        ('Salary Information', {
            'fields': ('basic_salary', 'grade_pay', 'pay_scale', 'bank_name',
                      'bank_account_number', 'ifsc_code'),
            'classes': ('collapse',)
        }),
        ('Teaching & Research', {
            'fields': ('max_weekly_hours', 'current_weekly_hours', 'research_interests',
                      'publications_count', 'projects_count')
        }),
        ('Documents', {
            'fields': ('photo', 'resume', 'id_proof'),
            'classes': ('collapse',)
        }),
        ('Social Links', {
            'fields': ('linkedin_url', 'google_scholar_url', 'research_gate_url', 'orcid_id'),
            'classes': ('collapse',)
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Set created_by if not set"""
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(FacultyQualification)
class FacultyQualificationAdmin(admin.ModelAdmin):
    """Admin interface for FacultyQualification"""
    list_display = ['faculty', 'degree', 'degree_name', 'institution', 
                    'year_of_passing', 'is_verified']
    list_filter = ['degree', 'is_verified', 'year_of_passing']
    search_fields = ['degree_name', 'institution', 'university', 'specialization']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-year_of_passing']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('faculty', 'degree', 'degree_name', 'specialization')
        }),
        ('Institution Details', {
            'fields': ('institution', 'university', 'year_of_passing',
                      'percentage_or_cgpa', 'grade_system')
        }),
        ('Verification', {
            'fields': ('certificate', 'is_verified')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(FacultyExperience)
class FacultyExperienceAdmin(admin.ModelAdmin):
    """Admin interface for FacultyExperience"""
    list_display = ['faculty', 'designation', 'organization', 'experience_type',
                    'start_date', 'end_date', 'is_current']
    list_filter = ['experience_type', 'is_current', 'start_date']
    search_fields = ['organization', 'designation', 'location']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-start_date']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('faculty', 'organization', 'designation', 'experience_type')
        }),
        ('Duration', {
            'fields': ('start_date', 'end_date', 'is_current')
        }),
        ('Details', {
            'fields': ('responsibilities', 'location', 'certificate')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(FacultyAttendance)
class FacultyAttendanceAdmin(admin.ModelAdmin):
    """Admin interface for FacultyAttendance"""
    list_display = ['faculty', 'date', 'status', 'check_in_time', 
                    'check_out_time', 'working_hours', 'marked_by']
    list_filter = ['status', 'date']
    search_fields = ['faculty__first_name', 'faculty__last_name', 'faculty__employee_id']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'
    ordering = ['-date']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('faculty', 'date', 'status')
        }),
        ('Timing', {
            'fields': ('check_in_time', 'check_out_time', 'working_hours')
        }),
        ('Additional', {
            'fields': ('remarks', 'marked_by')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(FacultyLeave)
class FacultyLeaveAdmin(admin.ModelAdmin):
    """Admin interface for FacultyLeave"""
    list_display = ['faculty', 'leave_type', 'start_date', 'end_date',
                    'number_of_days', 'status', 'approved_by']
    list_filter = ['leave_type', 'status', 'start_date']
    search_fields = ['faculty__first_name', 'faculty__last_name', 
                     'faculty__employee_id', 'reason']
    readonly_fields = ['number_of_days', 'created_at', 'updated_at']
    date_hierarchy = 'start_date'
    ordering = ['-start_date']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('faculty', 'leave_type', 'start_date', 'end_date', 'number_of_days')
        }),
        ('Details', {
            'fields': ('reason', 'supporting_document')
        }),
        ('Approval', {
            'fields': ('status', 'approved_by', 'approval_date', 'rejection_reason')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(FacultyPublication)
class FacultyPublicationAdmin(admin.ModelAdmin):
    """Admin interface for FacultyPublication"""
    list_display = ['title', 'faculty', 'publication_type', 'year', 
                    'citation_count', 'is_indexed']
    list_filter = ['publication_type', 'year', 'is_indexed']
    search_fields = ['title', 'authors', 'journal_or_conference', 'keywords']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-year', '-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('faculty', 'title', 'publication_type', 'authors', 'year')
        }),
        ('Publication Details', {
            'fields': ('journal_or_conference', 'volume', 'issue', 'pages',
                      'doi', 'isbn_issn', 'url')
        }),
        ('Content', {
            'fields': ('abstract', 'keywords'),
            'classes': ('collapse',)
        }),
        ('Metrics', {
            'fields': ('citation_count', 'impact_factor', 'is_indexed')
        }),
        ('Document', {
            'fields': ('document',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(FacultyAward)
class FacultyAwardAdmin(admin.ModelAdmin):
    """Admin interface for FacultyAward"""
    list_display = ['title', 'faculty', 'awarding_body', 'date_received', 'category']
    list_filter = ['category', 'date_received']
    search_fields = ['title', 'awarding_body', 'description']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date_received'
    ordering = ['-date_received']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('faculty', 'title', 'awarding_body', 'date_received', 'category')
        }),
        ('Details', {
            'fields': ('description', 'certificate')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

