"""
Transport URL Configuration
"""
from django.urls import path
from . import views

app_name = 'transport'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Vehicles
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/create/', views.vehicle_create, name='vehicle_create'),
    path('vehicles/<uuid:pk>/update/', views.vehicle_update, name='vehicle_update'),
    path('vehicles/<uuid:pk>/delete/', views.vehicle_delete, name='vehicle_delete'),
    
    # Drivers
    path('drivers/', views.driver_list, name='driver_list'),
    path('drivers/create/', views.driver_create, name='driver_create'),
    
    # Routes
    path('routes/', views.route_list, name='route_list'),
    path('routes/create/', views.route_create, name='route_create'),
    path('routes/<uuid:pk>/', views.route_detail, name='route_detail'),
    
    # Student Assignments
    path('assignments/', views.student_assignment_list, name='student_assignment_list'),
    path('assignments/create/', views.student_assignment_create, name='student_assignment_create'),
    
    # Maintenance
    path('maintenance/', views.maintenance_list, name='maintenance_list'),
    path('maintenance/create/', views.maintenance_create, name='maintenance_create'),
    
    # Fuel Logs
    path('fuel-logs/', views.fuel_log_list, name='fuel_log_list'),
    path('fuel-logs/create/', views.fuel_log_create, name='fuel_log_create'),
    
    # Route Tracking
    path('tracking/', views.route_tracking_list, name='route_tracking_list'),
    path('tracking/create/', views.route_tracking_create, name='route_tracking_create'),
    
    # Reports
    path('reports/', views.reports, name='reports'),
    
    # Exports
    path('export/vehicles/csv/', views.export_vehicles_csv, name='export_vehicles_csv'),
    path('export/fuel-logs/csv/', views.export_fuel_logs_csv, name='export_fuel_logs_csv'),
]
