"""
Transport Admin Configuration
"""
from django.contrib import admin
from .models import (
    Driver, Vehicle, Route, RouteStop,
    StudentTransportAssignment, VehicleMaintenance,
    FuelLog, RouteTracking
)


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    """Admin for Driver"""
    list_display = ['user', 'license_number', 'license_type', 'employment_status', 'date_of_joining']
    list_filter = ['employment_status', 'license_type', 'date_of_joining']
    search_fields = ['user__first_name', 'user__last_name', 'license_number']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['user__first_name']


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    """Admin for Vehicle"""
    list_display = ['registration_number', 'make', 'model', 'vehicle_type', 'status', 'assigned_driver']
    list_filter = ['status', 'vehicle_type', 'fuel_type']
    search_fields = ['registration_number', 'make', 'model']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['registration_number']
    
    fieldsets = (
        ('Vehicle Details', {
            'fields': ('registration_number', 'make', 'model', 'year', 'vehicle_type', 'seating_capacity')
        }),
        ('Status & Assignment', {
            'fields': ('status', 'assigned_driver')
        }),
        ('Insurance & Registration', {
            'fields': ('insurance_number', 'insurance_expiry_date', 'registration_expiry_date')
        }),
        ('Additional Info', {
            'fields': ('color', 'fuel_type', 'purchase_date', 'purchase_price', 'notes')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    """Admin for Route"""
    list_display = ['route_number', 'route_name', 'assigned_vehicle', 'assigned_driver', 'is_active']
    list_filter = ['is_active', 'route_type']
    search_fields = ['route_number', 'route_name', 'start_point', 'end_point']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['route_number']


@admin.register(RouteStop)
class RouteStopAdmin(admin.ModelAdmin):
    """Admin for Route Stop"""
    list_display = ['route', 'sequence_number', 'stop_name', 'arrival_time', 'fare_amount']
    list_filter = ['route', 'is_active']
    search_fields = ['stop_name', 'stop_address']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['route', 'sequence_number']


@admin.register(StudentTransportAssignment)
class StudentTransportAssignmentAdmin(admin.ModelAdmin):
    """Admin for Student Transport Assignment"""
    list_display = ['student', 'route', 'pickup_stop', 'drop_stop', 'payment_status', 'is_active']
    list_filter = ['is_active', 'payment_status', 'route']
    search_fields = ['student__user__first_name', 'student__user__last_name', 'student__student_id']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'start_date'
    ordering = ['-created_at']


@admin.register(VehicleMaintenance)
class VehicleMaintenanceAdmin(admin.ModelAdmin):
    """Admin for Vehicle Maintenance"""
    list_display = ['vehicle', 'maintenance_type', 'maintenance_date', 'cost', 'status']
    list_filter = ['status', 'maintenance_type', 'maintenance_date']
    search_fields = ['vehicle__registration_number', 'description']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'maintenance_date'
    ordering = ['-maintenance_date']


@admin.register(FuelLog)
class FuelLogAdmin(admin.ModelAdmin):
    """Admin for Fuel Log"""
    list_display = ['vehicle', 'driver', 'fuel_date', 'quantity_liters', 'total_cost', 'odometer_reading']
    list_filter = ['fuel_type', 'fuel_date']
    search_fields = ['vehicle__registration_number', 'fuel_station']
    readonly_fields = ['total_cost', 'created_at', 'updated_at']
    date_hierarchy = 'fuel_date'
    ordering = ['-fuel_date']


@admin.register(RouteTracking)
class RouteTrackingAdmin(admin.ModelAdmin):
    """Admin for Route Tracking"""
    list_display = ['route', 'vehicle', 'driver', 'trip_date', 'status', 'students_count']
    list_filter = ['status', 'trip_date']
    search_fields = ['route__route_number', 'vehicle__registration_number']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'trip_date'
    ordering = ['-trip_date']
