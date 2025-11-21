"""
Transport Filters
"""
import django_filters
from .models import Vehicle, Driver, Route, FuelLog, VehicleMaintenance


class VehicleFilter(django_filters.FilterSet):
    """Filter for Vehicle"""
    registration_number = django_filters.CharFilter(lookup_expr='icontains')
    make = django_filters.CharFilter(lookup_expr='icontains')
    model = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Vehicle
        fields = ['status', 'vehicle_type', 'fuel_type', 'assigned_driver']


class DriverFilter(django_filters.FilterSet):
    """Filter for Driver"""
    license_number = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Driver
        fields = ['employment_status', 'license_type']


class RouteFilter(django_filters.FilterSet):
    """Filter for Route"""
    route_number = django_filters.CharFilter(lookup_expr='icontains')
    route_name = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Route
        fields = ['is_active', 'route_type', 'assigned_vehicle', 'assigned_driver']


class FuelLogFilter(django_filters.FilterSet):
    """Filter for Fuel Log"""
    fuel_date = django_filters.DateFilter()
    fuel_date_from = django_filters.DateFilter(field_name='fuel_date', lookup_expr='gte')
    fuel_date_to = django_filters.DateFilter(field_name='fuel_date', lookup_expr='lte')
    
    class Meta:
        model = FuelLog
        fields = ['vehicle', 'driver', 'fuel_type']


class VehicleMaintenanceFilter(django_filters.FilterSet):
    """Filter for Vehicle Maintenance"""
    maintenance_date_from = django_filters.DateFilter(field_name='maintenance_date', lookup_expr='gte')
    maintenance_date_to = django_filters.DateFilter(field_name='maintenance_date', lookup_expr='lte')
    
    class Meta:
        model = VehicleMaintenance
        fields = ['vehicle', 'maintenance_type', 'status']
