"""
Transport Views - Complete Implementation
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count, Avg
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db import transaction
from datetime import datetime, timedelta
import csv
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from .models import (
    Driver, Vehicle, Route, RouteStop,
    StudentTransportAssignment, VehicleMaintenance,
    FuelLog, RouteTracking
)
from .forms import (
    DriverForm, VehicleForm, RouteForm, RouteStopForm,
    StudentTransportAssignmentForm, VehicleMaintenanceForm,
    FuelLogForm, RouteTrackingForm
)


# ============================================================================
# Dashboard
# ============================================================================

@login_required
def dashboard(request):
    """Transport dashboard"""
    stats = {
        'total_vehicles': Vehicle.objects.filter(status='active').count(),
        'total_drivers': Driver.objects.filter(employment_status='active').count(),
        'total_routes': Route.objects.filter(is_active=True).count(),
        'total_students': StudentTransportAssignment.objects.filter(is_active=True).count(),
    }
    
    # Recent maintenance
    recent_maintenance = VehicleMaintenance.objects.select_related('vehicle').order_by('-maintenance_date')[:5]
    
    # Vehicles needing maintenance
    upcoming_maintenance = VehicleMaintenance.objects.filter(
        status='scheduled',
        maintenance_date__gte=timezone.now().date()
    ).select_related('vehicle')[:5]
    
    # Recent fuel logs
    recent_fuel = FuelLog.objects.select_related('vehicle', 'driver').order_by('-fuel_date')[:5]
    
    context = {
        'stats': stats,
        'recent_maintenance': recent_maintenance,
        'upcoming_maintenance': upcoming_maintenance,
        'recent_fuel': recent_fuel,
        'title': 'Transport Dashboard',
    }
    
    return render(request, transport/dashboard.htmltransport/'transport/dashboard.html, context)


# ============================================================================
# Vehicle Management
# ============================================================================

@login_required
def vehicle_list(request):
    """List all vehicles"""
    vehicles = Vehicle.objects.all().select_related('assigned_driver')
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        vehicles = vehicles.filter(
            Q(registration_number__icontains=search_query) |
            Q(make__icontains=search_query) |
            Q(model__icontains=search_query)
        )
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        vehicles = vehicles.filter(status=status)
    
    # Pagination
    paginator = Paginator(vehicles, 20)
    page = request.GET.get('page')
    vehicles_page = paginator.get_page(page)
    
    context = {
        'vehicles': vehicles_page,
        'search_query': search_query,
        'title': 'Vehicles',
    }
    
    return render(request, transport/vehicle_management.htmltransport/'transport/vehicle_management.html, context)


@login_required
def vehicle_create(request):
    """Create vehicle"""
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehicle created successfully!')
            return redirect('transport:vehicle_list')
    else:
        form = VehicleForm()
    
    context = {
        'form': form,
        'action': 'Create',
        'title': 'Create Vehicle',
    }
    
    return render(request, transport/vehicle_form.htmltransport/'transport/vehicle_form.html, context)


@login_required
def vehicle_update(request, pk):
    """Update vehicle"""
    vehicle = get_object_or_404(Vehicle, pk=pk)
    
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehicle updated successfully!')
            return redirect('transport:vehicle_list')
    else:
        form = VehicleForm(instance=vehicle)
    
    context = {
        'form': form,
        'vehicle': vehicle,
        'action': 'Update',
        'title': 'Update Vehicle',
    }
    
    return render(request, transport/vehicle_form.htmltransport/'transport/vehicle_form.html, context)


@login_required
@require_http_methods(["POST"])
def vehicle_delete(request, pk):
    """Delete vehicle"""
    vehicle = get_object_or_404(Vehicle, pk=pk)
    vehicle.delete()
    messages.success(request, 'Vehicle deleted successfully!')
    return redirect('transport:vehicle_list')


# ============================================================================
# Driver Management
# ============================================================================

@login_required
def driver_list(request):
    """List all drivers"""
    drivers = Driver.objects.all().select_related('user')
    
    # Filter
    status = request.GET.get('status')
    if status:
        drivers = drivers.filter(employment_status=status)
    
    # Pagination
    paginator = Paginator(drivers, 20)
    page = request.GET.get('page')
    drivers_page = paginator.get_page(page)
    
    context = {
        'drivers': drivers_page,
        'title': 'Drivers',
    }
    
    return render(request, transport/driver_management.htmltransport/'transport/driver_management.html, context)


@login_required
def driver_create(request):
    """Create driver"""
    if request.method == 'POST':
        form = DriverForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Driver created successfully!')
            return redirect('transport:driver_list')
    else:
        form = DriverForm()
    
    context = {
        'form': form,
        'action': 'Create',
        'title': 'Create Driver',
    }
    
    return render(request, transport/driver_form.htmltransport/'transport/driver_form.html, context)


# ============================================================================
# Route Management
# ============================================================================

@login_required
def route_list(request):
    """List all routes"""
    routes = Route.objects.all().select_related('assigned_vehicle', 'assigned_driver')
    
    # Filter
    if request.GET.get('active_only'):
        routes = routes.filter(is_active=True)
    
    # Pagination
    paginator = Paginator(routes, 20)
    page = request.GET.get('page')
    routes_page = paginator.get_page(page)
    
    context = {
        'routes': routes_page,
        'title': 'Routes',
    }
    
    return render(request, transport/route_management.htmltransport/'transport/route_management.html, context)


@login_required
def route_create(request):
    """Create route"""
    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Route created successfully!')
            return redirect('transport:route_list')
    else:
        form = RouteForm()
    
    context = {
        'form': form,
        'action': 'Create',
        'title': 'Create Route',
    }
    
    return render(request, transport/route_form.htmltransport/'transport/route_form.html, context)


@login_required
def route_detail(request, pk):
    """View route details with stops"""
    route = get_object_or_404(Route, pk=pk)
    stops = route.stops.all().order_by('sequence_number')
    
    context = {
        'route': route,
        'stops': stops,
        'title': f'Route: {route.route_number}',
    }
    
    return render(request, transport/route_detail.htmltransport/'transport/route_detail.html, context)


# ============================================================================
# Student Assignment
# ============================================================================

@login_required
def student_assignment_list(request):
    """List student transport assignments"""
    assignments = StudentTransportAssignment.objects.select_related(
        'student', 'route', 'pickup_stop', 'drop_stop'
    ).filter(is_active=True)
    
    # Filter by route
    route_id = request.GET.get('route')
    if route_id:
        assignments = assignments.filter(route_id=route_id)
    
    # Pagination
    paginator = Paginator(assignments, 30)
    page = request.GET.get('page')
    assignments_page = paginator.get_page(page)
    
    routes = Route.objects.filter(is_active=True)
    
    context = {
        'assignments': assignments_page,
        'routes': routes,
        'title': 'Student Assignments',
    }
    
    return render(request, transport/student_assignment.htmltransport/'transport/student_assignment.html, context)


@login_required
def student_assignment_create(request):
    """Assign student to route"""
    if request.method == 'POST':
        form = StudentTransportAssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student assigned to route successfully!')
            return redirect('transport:student_assignment_list')
    else:
        form = StudentTransportAssignmentForm()
    
    context = {
        'form': form,
        'action': 'Create',
        'title': 'Assign Student',
    }
    
    return render(request, transport/student_assignment_form.htmltransport/'transport/student_assignment_form.html, context)


# ============================================================================
# Maintenance Management
# ============================================================================

@login_required
def maintenance_list(request):
    """List maintenance records"""
    maintenance_records = VehicleMaintenance.objects.select_related('vehicle').order_by('-maintenance_date')
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        maintenance_records = maintenance_records.filter(status=status)
    
    # Pagination
    paginator = Paginator(maintenance_records, 20)
    page = request.GET.get('page')
    records_page = paginator.get_page(page)
    
    context = {
        'records': records_page,
        'title': 'Vehicle Maintenance',
    }
    
    return render(request, transport/maintenance.htmltransport/'transport/maintenance.html, context)


@login_required
def maintenance_create(request):
    """Create maintenance record"""
    if request.method == 'POST':
        form = VehicleMaintenanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Maintenance record created successfully!')
            return redirect('transport:maintenance_list')
    else:
        form = VehicleMaintenanceForm()
    
    context = {
        'form': form,
        'action': 'Create',
        'title': 'Create Maintenance Record',
    }
    
    return render(request, transport/maintenance_form.htmltransport/'transport/maintenance_form.html, context)


# ============================================================================
# Fuel Log
# ============================================================================

@login_required
def fuel_log_list(request):
    """List fuel logs"""
    fuel_logs = FuelLog.objects.select_related('vehicle', 'driver').order_by('-fuel_date')
    
    # Filter by vehicle
    vehicle_id = request.GET.get('vehicle')
    if vehicle_id:
        fuel_logs = fuel_logs.filter(vehicle_id=vehicle_id)
    
    # Pagination
    paginator = Paginator(fuel_logs, 30)
    page = request.GET.get('page')
    logs_page = paginator.get_page(page)
    
    vehicles = Vehicle.objects.filter(status='active')
    
    context = {
        'logs': logs_page,
        'vehicles': vehicles,
        'title': 'Fuel Logs',
    }
    
    return render(request, transport/fuel_log.htmltransport/'transport/fuel_log.html, context)


@login_required
def fuel_log_create(request):
    """Create fuel log"""
    if request.method == 'POST':
        form = FuelLogForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fuel log created successfully!')
            return redirect('transport:fuel_log_list')
    else:
        form = FuelLogForm()
    
    context = {
        'form': form,
        'action': 'Create',
        'title': 'Create Fuel Log',
    }
    
    return render(request, transport/fuel_log_form.htmltransport/'transport/fuel_log_form.html, context)


# ============================================================================
# Route Tracking
# ============================================================================

@login_required
def route_tracking_list(request):
    """List route tracking logs"""
    tracking_logs = RouteTracking.objects.select_related(
        'route', 'vehicle', 'driver'
    ).order_by('-trip_date')
    
    # Filter by date
    date_from = request.GET.get('date_from')
    if date_from:
        tracking_logs = tracking_logs.filter(trip_date__gte=date_from)
    
    # Pagination
    paginator = Paginator(tracking_logs, 30)
    page = request.GET.get('page')
    logs_page = paginator.get_page(page)
    
    context = {
        'logs': logs_page,
        'title': 'Route Tracking',
    }
    
    return render(request, transport/route_tracking.htmltransport/'transport/route_tracking.html, context)


@login_required
def route_tracking_create(request):
    """Create route tracking log"""
    if request.method == 'POST':
        form = RouteTrackingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Route tracking log created successfully!')
            return redirect('transport:route_tracking_list')
    else:
        form = RouteTrackingForm()
    
    context = {
        'form': form,
        'action': 'Create',
        'title': 'Create Route Tracking',
    }
    
    return render(request, transport/route_tracking_form.htmltransport/'transport/route_tracking_form.html, context)


# ============================================================================
# Reports
# ============================================================================

@login_required
def reports(request):
    """Transport reports"""
    # Fuel consumption by vehicle
    fuel_by_vehicle = FuelLog.objects.values('vehicle__registration_number').annotate(
        total_liters=Sum('quantity_liters'),
        total_cost=Sum('total_cost'),
        avg_price=Avg('price_per_liter')
    )
    
    # Maintenance costs by vehicle
    maintenance_by_vehicle = VehicleMaintenance.objects.values('vehicle__registration_number').annotate(
        total_cost=Sum('cost'),
        count=Count('id')
    )
    
    context = {
        'fuel_by_vehicle': fuel_by_vehicle,
        'maintenance_by_vehicle': maintenance_by_vehicle,
        'title': 'Transport Reports',
    }
    
    return render(request, transport/reports.htmltransport/'transport/reports.html, context)


# ============================================================================
# Export Operations
# ============================================================================

@login_required
def export_vehicles_csv(request):
    """Export vehicles to CSV"""
    vehicles = Vehicle.objects.all()
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="vehicles_{timezone.now().strftime("%Y%m%d")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Registration', 'Make', 'Model', 'Type', 'Status', 'Capacity'])
    
    for vehicle in vehicles:
        writer.writerow([
            vehicle.registration_number,
            vehicle.make,
            vehicle.model,
            vehicle.vehicle_type,
            vehicle.status,
            vehicle.seating_capacity,
        ])
    
    return response


@login_required
def export_fuel_logs_csv(request):
    """Export fuel logs to CSV"""
    logs = FuelLog.objects.select_related('vehicle', 'driver').all()
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="fuel_logs_{timezone.now().strftime("%Y%m%d")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Date', 'Vehicle', 'Driver', 'Quantity (L)', 'Price/L', 'Total Cost', 'Odometer'])
    
    for log in logs:
        writer.writerow([
            log.fuel_date,
            log.vehicle.registration_number,
            log.driver.user.get_full_name() if log.driver else 'N/A',
            log.quantity_liters,
            log.price_per_liter,
            log.total_cost,
            log.odometer_reading,
        ])
    
    return response
