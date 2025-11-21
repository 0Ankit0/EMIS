"""
Timetable Admin Configuration
"""
from django.contrib import admin
from .models import (
    AcademicYear, Semester, TimeSlot, Room,
    TimetableEntry, TimetableException
)


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    """Admin for Academic Year"""
    list_display = ['name', 'start_date', 'end_date', 'is_active', 'created_at']
    list_filter = ['is_active', 'start_date']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-start_date']


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    """Admin for Semester"""
    list_display = ['name', 'academic_year', 'semester_number', 'start_date', 'end_date', 'is_active']
    list_filter = ['is_active', 'academic_year', 'start_date']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-start_date']


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    """Admin for Time Slot"""
    list_display = ['name', 'day_of_week', 'start_time', 'end_time', 'is_active']
    list_filter = ['is_active', 'day_of_week']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['day_of_week', 'start_time']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """Admin for Room"""
    list_display = ['name', 'room_number', 'building', 'capacity', 'room_type', 'is_active']
    list_filter = ['is_active', 'room_type', 'building']
    search_fields = ['name', 'room_number', 'building']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['building', 'name']


@admin.register(TimetableEntry)
class TimetableEntryAdmin(admin.ModelAdmin):
    """Admin for Timetable Entry"""
    list_display = ['course', 'time_slot', 'room', 'instructor', 'section', 'session_type', 'is_active']
    list_filter = ['is_active', 'session_type', 'semester', 'is_recurring']
    search_fields = ['course__code', 'course__title', 'section', 'batch']
    readonly_fields = ['created_at', 'updated_at', 'created_by']
    date_hierarchy = 'start_date'
    ordering = ['-start_date']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('semester', 'course', 'time_slot', 'room', 'instructor')
        }),
        ('Class Details', {
            'fields': ('section', 'batch', 'session_type')
        }),
        ('Schedule', {
            'fields': ('is_recurring', 'start_date', 'end_date')
        }),
        ('Additional', {
            'fields': ('notes', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TimetableException)
class TimetableExceptionAdmin(admin.ModelAdmin):
    """Admin for Timetable Exception"""
    list_display = ['timetable_entry', 'date', 'exception_type', 'is_active']
    list_filter = ['is_active', 'exception_type', 'date']
    search_fields = ['timetable_entry__course__code', 'reason']
    readonly_fields = ['created_at', 'updated_at', 'created_by']
    date_hierarchy = 'date'
    ordering = ['-date']
