"""
Transport Utility Functions
"""
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Sum, Avg, Count
from datetime import datetime, timedelta
import csv
from io import StringIO


def calculate_fuel_efficiency(vehicle, start_date=None, end_date=None):
    """
    Calculate fuel efficiency for a vehicle
    
    Args:
        vehicle: Vehicle object
        start_date: Start date for calculation
        end_date: End date for calculation
    
    Returns:
        dict: Fuel efficiency metrics
    """
    from .models import FuelLog
    
    fuel_logs = FuelLog.objects.filter(vehicle=vehicle)
    
    if start_date:
        fuel_logs = fuel_logs.filter(fuel_date__gte=start_date)
    
    if end_date:
        fuel_logs = fuel_logs.filter(fuel_date__lte=end_date)
    
    fuel_logs = fuel_logs.order_by('odometer_reading')
    
    if fuel_logs.count() < 2:
        return {
            'total_fuel': 0,
            'total_distance': 0,
            'efficiency': 0,
            'total_cost': 0
        }
    
    total_fuel = fuel_logs.aggregate(total=Sum('quantity_liters'))['total'] or 0
    total_cost = fuel_logs.aggregate(total=Sum('total_cost'))['total'] or 0
    
    first_log = fuel_logs.first()
    last_log = fuel_logs.last()
    
    total_distance = last_log.odometer_reading - first_log.odometer_reading
    efficiency = (total_distance / total_fuel) if total_fuel > 0 else 0
    
    return {
        'total_fuel': float(total_fuel),
        'total_distance': total_distance,
        'efficiency': round(efficiency, 2),  # km per liter
        'total_cost': float(total_cost)
    }


def get_maintenance_due(days_ahead=30):
    """
    Get vehicles with maintenance due in the next X days
    
    Args:
        days_ahead: Number of days to look ahead
    
    Returns:
        QuerySet: Vehicles needing maintenance
    """
    from .models import VehicleMaintenance
    
    target_date = timezone.now().date() + timedelta(days=days_ahead)
    
    due_maintenance = VehicleMaintenance.objects.filter(
        status='scheduled',
        next_service_date__lte=target_date,
        next_service_date__gte=timezone.now().date()
    ).select_related('vehicle')
    
    return due_maintenance


def validate_route_assignment(route, vehicle, driver):
    """
    Validate if a vehicle and driver can be assigned to a route
    
    Args:
        route: Route object
        vehicle: Vehicle object
        driver: Driver object
    
    Returns:
        tuple: (is_valid, error_message)
    """
    errors = []
    
    # Check vehicle status
    if vehicle.status != 'active':
        errors.append(f"Vehicle {vehicle.registration_number} is not active")
    
    # Check driver status
    if driver.employment_status != 'active':
        errors.append(f"Driver {driver.user.get_full_name()} is not active")
    
    # Check if driver's license is not expired
    if driver.license_expiry_date < timezone.now().date():
        errors.append(f"Driver's license has expired")
    
    if errors:
        return False, '; '.join(errors)
    
    return True, None


def generate_transport_report(start_date, end_date):
    """
    Generate comprehensive transport report
    
    Args:
        start_date: Start date for report
        end_date: End date for report
    
    Returns:
        dict: Report data
    """
    from .models import FuelLog, VehicleMaintenance, RouteTracking, Vehicle
    
    # Fuel consumption
    fuel_data = FuelLog.objects.filter(
        fuel_date__range=[start_date, end_date]
    ).aggregate(
        total_liters=Sum('quantity_liters'),
        total_cost=Sum('total_cost'),
        avg_price=Avg('price_per_liter')
    )
    
    # Maintenance costs
    maintenance_data = VehicleMaintenance.objects.filter(
        maintenance_date__range=[start_date, end_date],
        status='completed'
    ).aggregate(
        total_cost=Sum('cost'),
        count=Count('id')
    )
    
    # Route statistics
    route_data = RouteTracking.objects.filter(
        trip_date__range=[start_date, end_date]
    ).aggregate(
        total_trips=Count('id'),
        completed_trips=Count('id', filter=models.Q(status='completed')),
        total_students=Sum('students_count')
    )
    
    # Vehicle utilization
    total_vehicles = Vehicle.objects.filter(status='active').count()
    
    return {
        'period': {
            'start': start_date,
            'end': end_date
        },
        'fuel': {
            'total_liters': float(fuel_data['total_liters'] or 0),
            'total_cost': float(fuel_data['total_cost'] or 0),
            'avg_price_per_liter': float(fuel_data['avg_price'] or 0)
        },
        'maintenance': {
            'total_cost': float(maintenance_data['total_cost'] or 0),
            'count': maintenance_data['count'] or 0
        },
        'routes': {
            'total_trips': route_data['total_trips'] or 0,
            'completed_trips': route_data['completed_trips'] or 0,
            'total_students_transported': route_data['total_students'] or 0
        },
        'fleet': {
            'total_active_vehicles': total_vehicles
        }
    }


def export_transport_data_to_csv(model_name, queryset):
    """
    Export transport data to CSV
    
    Args:
        model_name: Name of the model
        queryset: QuerySet to export
    
    Returns:
        str: CSV data
    """
    output = StringIO()
    writer = csv.writer(output)
    
    if model_name == 'Vehicle':
        writer.writerow(['Registration', 'Make', 'Model', 'Type', 'Status', 'Capacity'])
        for obj in queryset:
            writer.writerow([
                obj.registration_number,
                obj.make,
                obj.model,
                obj.vehicle_type,
                obj.status,
                obj.seating_capacity
            ])
    
    elif model_name == 'Driver':
        writer.writerow(['Name', 'License Number', 'Type', 'Status', 'Experience'])
        for obj in queryset:
            writer.writerow([
                obj.user.get_full_name(),
                obj.license_number,
                obj.license_type,
                obj.employment_status,
                obj.experience_years
            ])
    
    elif model_name == 'Route':
        writer.writerow(['Number', 'Name', 'From', 'To', 'Distance', 'Active'])
        for obj in queryset:
            writer.writerow([
                obj.route_number,
                obj.route_name,
                obj.start_point,
                obj.end_point,
                obj.total_distance_km,
                obj.is_active
            ])
    
    return output.getvalue()


def check_vehicle_availability(vehicle, date):
    """
    Check if a vehicle is available on a specific date
    
    Args:
        vehicle: Vehicle object
        date: Date to check
    
    Returns:
        bool: True if available
    """
    from .models import VehicleMaintenance, RouteTracking
    
    # Check if under maintenance
    maintenance_conflict = VehicleMaintenance.objects.filter(
        vehicle=vehicle,
        maintenance_date=date,
        status__in=['scheduled', 'in_progress']
    ).exists()
    
    if maintenance_conflict:
        return False
    
    return True


def get_route_revenue(route, start_date, end_date):
    """
    Calculate revenue from a route
    
    Args:
        route: Route object
        start_date: Start date
        end_date: End date
    
    Returns:
        dict: Revenue data
    """
    from .models import StudentTransportAssignment
    
    assignments = StudentTransportAssignment.objects.filter(
        route=route,
        is_active=True,
        start_date__lte=end_date
    ).filter(
        models.Q(end_date__isnull=True) | models.Q(end_date__gte=start_date)
    )
    
    total_revenue = assignments.aggregate(total=Sum('monthly_fee'))['total'] or 0
    paid_count = assignments.filter(payment_status='paid').count()
    pending_count = assignments.filter(payment_status='pending').count()
    
    return {
        'total_students': assignments.count(),
        'total_revenue': float(total_revenue),
        'paid_count': paid_count,
        'pending_count': pending_count
    }
