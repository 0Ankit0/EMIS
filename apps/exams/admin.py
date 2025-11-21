"""
Exams Admin Configuration
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Exam, ExamResult, ExamSchedule


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    """
    Admin interface for Exam
    """
    list_display = [
        'exam_code', 'exam_name', 'course', 'exam_type',
        'exam_date', 'status_badge', 'total_marks', 'pass_percentage_display'
    ]
    list_filter = ['status', 'exam_type', 'exam_date', 'semester', 'academic_year']
    search_fields = ['exam_code', 'exam_name', 'course__course_name']
    readonly_fields = ['created_at', 'updated_at', 'pass_percentage_display']
    date_hierarchy = 'exam_date'
    ordering = ['-exam_date', '-start_time']
    list_per_page = 25
    
    fieldsets = (
        ('Exam Information', {
            'fields': ('exam_code', 'exam_name', 'course', 'exam_type')
        }),
        ('Academic Period', {
            'fields': ('academic_year', 'semester')
        }),
        ('Schedule', {
            'fields': ('exam_date', 'start_time', 'end_time', 'duration_minutes', 'room_number', 'invigilator')
        }),
        ('Marks', {
            'fields': ('total_marks', 'passing_marks')
        }),
        ('Status & Publishing', {
            'fields': ('status', 'is_published')
        }),
        ('Additional Information', {
            'fields': ('instructions',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at', 'pass_percentage_display'),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        colors = {
            'scheduled': 'blue',
            'ongoing': 'yellow',
            'completed': 'green',
            'cancelled': 'red',
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def pass_percentage_display(self, obj):
        percentage = obj.get_pass_percentage()
        return f"{percentage:.2f}%"
    pass_percentage_display.short_description = 'Pass Percentage'
    
    actions = ['mark_as_completed', 'mark_as_cancelled', 'publish_results']
    
    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
        self.message_user(request, f"{queryset.count()} exam(s) marked as completed.")
    mark_as_completed.short_description = "Mark selected exams as completed"
    
    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
        self.message_user(request, f"{queryset.count()} exam(s) marked as cancelled.")
    mark_as_cancelled.short_description = "Mark selected exams as cancelled"
    
    def publish_results(self, request, queryset):
        queryset.update(is_published=True)
        self.message_user(request, f"Results published for {queryset.count()} exam(s).")
    publish_results.short_description = "Publish results for selected exams"


@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    """
    Admin interface for ExamResult
    """
    list_display = [
        'student', 'exam', 'marks_obtained', 'grade_badge',
        'status_badge', 'percentage_display'
    ]
    list_filter = ['is_passed', 'is_absent', 'grade', 'exam__exam_type', 'exam__academic_year']
    search_fields = [
        'student__first_name', 'student__last_name', 'student__roll_number',
        'exam__exam_code', 'exam__exam_name'
    ]
    readonly_fields = ['grade', 'is_passed', 'created_at', 'updated_at', 'percentage_display']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    list_per_page = 50
    
    fieldsets = (
        ('Exam & Student', {
            'fields': ('exam', 'student')
        }),
        ('Marks', {
            'fields': ('marks_obtained', 'grade', 'is_passed', 'percentage_display')
        }),
        ('Status', {
            'fields': ('is_absent', 'remarks')
        }),
        ('Evaluation', {
            'fields': ('evaluated_by', 'evaluated_at')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def grade_badge(self, obj):
        if obj.is_absent:
            return format_html(
                '<span style="background-color: gray; color: white; padding: 3px 10px; border-radius: 3px;">ABSENT</span>'
            )
        colors = {
            'A+': 'darkgreen',
            'A': 'green',
            'B+': 'lightgreen',
            'B': 'yellowgreen',
            'C+': 'orange',
            'C': 'darkorange',
            'D': 'orangered',
            'F': 'red',
        }
        color = colors.get(obj.grade, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.grade
        )
    grade_badge.short_description = 'Grade'
    
    def status_badge(self, obj):
        if obj.is_absent:
            color = 'gray'
            text = 'Absent'
        elif obj.is_passed:
            color = 'green'
            text = 'Passed'
        else:
            color = 'red'
            text = 'Failed'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            text
        )
    status_badge.short_description = 'Status'
    
    def percentage_display(self, obj):
        return f"{obj.get_percentage():.2f}%"
    percentage_display.short_description = 'Percentage'


@admin.register(ExamSchedule)
class ExamScheduleAdmin(admin.ModelAdmin):
    """
    Admin interface for ExamSchedule
    """
    list_display = ['name', 'academic_year', 'semester', 'start_date', 'end_date', 'is_published_badge']
    list_filter = ['semester', 'academic_year', 'is_published']
    search_fields = ['name', 'description', 'academic_year']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'start_date'
    ordering = ['-start_date']
    
    fieldsets = (
        ('Schedule Information', {
            'fields': ('name', 'description')
        }),
        ('Academic Period', {
            'fields': ('academic_year', 'semester')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date')
        }),
        ('Publishing', {
            'fields': ('is_published',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def is_published_badge(self, obj):
        if obj.is_published:
            return format_html(
                '<span style="background-color: green; color: white; padding: 3px 10px; border-radius: 3px;">Published</span>'
            )
        return format_html(
            '<span style="background-color: orange; color: white; padding: 3px 10px; border-radius: 3px;">Draft</span>'
        )
    is_published_badge.short_description = 'Publication Status'
    
    actions = ['publish_schedules', 'unpublish_schedules']
    
    def publish_schedules(self, request, queryset):
        queryset.update(is_published=True)
        self.message_user(request, f"{queryset.count()} schedule(s) published.")
    publish_schedules.short_description = "Publish selected schedules"
    
    def unpublish_schedules(self, request, queryset):
        queryset.update(is_published=False)
        self.message_user(request, f"{queryset.count()} schedule(s) unpublished.")
    unpublish_schedules.short_description = "Unpublish selected schedules"