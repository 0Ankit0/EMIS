"""Hostel Admin Configuration"""
from django.contrib import admin
from .models import (
    Hostel, Floor, Room, RoomAllocation, HostelFee, MessMenu,
    VisitorLog, Complaint, OutingRequest, Attendance
)


@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'hostel_type', 'total_capacity', 'occupied_capacity',
                    'available_capacity', 'occupancy_percentage', 'status']
    list_filter = ['hostel_type', 'status', 'is_active']
    search_fields = ['name', 'code', 'city']
    readonly_fields = ['occupied_capacity', 'available_capacity', 'occupancy_percentage',
                       'created_at', 'updated_at']
    ordering = ['name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'hostel_type', 'warden')
        }),
        ('Location', {
            'fields': ('address', 'city', 'pincode')
        }),
        ('Capacity', {
            'fields': ('total_floors', 'total_rooms', 'total_capacity',
                      'occupied_capacity', 'available_capacity', 'occupancy_percentage')
        }),
        ('Contact', {
            'fields': ('contact_number', 'email')
        }),
        ('Details', {
            'fields': ('amenities', 'facilities', 'rules_and_regulations'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('status', 'is_active', 'established_date')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ['hostel', 'floor_number', 'total_rooms']
    list_filter = ['hostel']
    ordering = ['hostel', 'floor_number']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'hostel', 'floor', 'room_type', 'capacity',
                    'occupied_beds', 'available_beds', 'monthly_rent', 'status']
    list_filter = ['hostel', 'room_type', 'status', 'has_ac']
    search_fields = ['room_number']
    readonly_fields = ['available_beds', 'created_at', 'updated_at']
    ordering = ['hostel', 'floor', 'room_number']


@admin.register(RoomAllocation)
class RoomAllocationAdmin(admin.ModelAdmin):
    list_display = ['student', 'room', 'bed_number', 'allocation_date',
                    'vacate_date', 'status', 'monthly_rent']
    list_filter = ['status', 'academic_year', 'allocation_date']
    search_fields = ['student__user__email', 'room__room_number']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'allocation_date'
    ordering = ['-allocation_date']


@admin.register(HostelFee)
class HostelFeeAdmin(admin.ModelAdmin):
    list_display = ['hostel', 'room_type', 'fee_type', 'total_fee',
                    'academic_year', 'is_active']
    list_filter = ['hostel', 'room_type', 'fee_type', 'is_active']
    readonly_fields = ['total_fee', 'created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(MessMenu)
class MessMenuAdmin(admin.ModelAdmin):
    list_display = ['hostel', 'day_of_week', 'meal_type', 'timing', 'is_active']
    list_filter = ['hostel', 'day_of_week', 'meal_type', 'is_active']
    ordering = ['hostel', 'day_of_week', 'meal_type']


@admin.register(VisitorLog)
class VisitorLogAdmin(admin.ModelAdmin):
    list_display = ['visitor_name', 'student', 'hostel', 'purpose',
                    'entry_time', 'exit_time']
    list_filter = ['hostel', 'purpose', 'entry_time']
    search_fields = ['visitor_name', 'visitor_phone', 'student__user__email']
    date_hierarchy = 'entry_time'
    ordering = ['-entry_time']


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['complaint_number', 'title', 'hostel', 'student', 'category',
                    'priority', 'status', 'submitted_date']
    list_filter = ['hostel', 'category', 'priority', 'status']
    search_fields = ['complaint_number', 'title', 'student__user__email']
    readonly_fields = ['complaint_number', 'created_at', 'updated_at']
    date_hierarchy = 'submitted_date'
    ordering = ['-submitted_date']


@admin.register(OutingRequest)
class OutingRequestAdmin(admin.ModelAdmin):
    list_display = ['student', 'hostel', 'out_date', 'expected_return_date',
                    'destination', 'status']
    list_filter = ['hostel', 'status', 'out_date']
    search_fields = ['student__user__email', 'destination']
    date_hierarchy = 'out_date'
    ordering = ['-created_at']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'hostel', 'date', 'status', 'marked_by']
    list_filter = ['hostel', 'status', 'date']
    search_fields = ['student__user__email']
    date_hierarchy = 'date'
    ordering = ['-date']
