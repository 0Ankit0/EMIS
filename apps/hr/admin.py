"""HR Admin Configuration"""
from django.contrib import admin
from .models import *


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'head', 'is_active']
    search_fields = ['name', 'code']


@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ['code', 'title', 'level', 'department', 'is_active']
    list_filter = ['level', 'is_active']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'get_full_name', 'department', 'designation', 'status']
    list_filter = ['department', 'designation', 'employment_type', 'status']
    search_fields = ['employee_id', 'first_name', 'last_name', 'email']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'status', 'working_hours']
    list_filter = ['status', 'date']
    date_hierarchy = 'date'


@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ['employee', 'leave_type', 'start_date', 'end_date', 'number_of_days', 'status']
    list_filter = ['leave_type', 'status']


@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ['employee', 'month', 'year', 'gross_salary', 'net_salary', 'status']
    list_filter = ['month', 'year', 'status']


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ['job_code', 'title', 'department', 'vacancies', 'status']
    list_filter = ['status', 'department']


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'job_posting', 'status', 'application_date']
    list_filter = ['status']


@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = ['employee', 'review_type', 'overall_rating', 'status']
    list_filter = ['review_type', 'status']


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ['code', 'title', 'start_date', 'end_date', 'status']
    list_filter = ['status']


@admin.register(TrainingParticipant)
class TrainingParticipantAdmin(admin.ModelAdmin):
    list_display = ['employee', 'training', 'status', 'certificate_issued']
    list_filter = ['status', 'certificate_issued']
