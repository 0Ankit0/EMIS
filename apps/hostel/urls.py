"""Hostel URL Configuration"""
from django.urls import path
from . import views

app_name = 'hostel'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Hostels
    path('hostels/', views.hostel_list, name='hostel_list'),
    path('hostels/<uuid:pk>/', views.hostel_detail, name='hostel_detail'),
    
    # Rooms
    path('rooms/', views.room_list, name='room_list'),
    
    # Allocations
    path('allocations/', views.allocation_list, name='allocation_list'),
    path('allocations/create/', views.room_allocation_create, name='allocation_create'),
    
    # Complaints
    path('complaints/', views.complaint_list, name='complaint_list'),
    path('complaints/create/', views.complaint_create, name='complaint_create'),
    
    # Outing Requests
    path('outings/', views.outing_request_list, name='outing_request_list'),
    path('outings/create/', views.outing_request_create, name='outing_request_create'),
    
    # Mess Menu
    path('hostels/<uuid:hostel_id>/mess-menu/', views.mess_menu, name='mess_menu'),
    
    # Visitor Logs
    path('hostels/<uuid:hostel_id>/visitors/', views.visitor_logs, name='visitor_logs'),
    
    # Export
    path('export/allocations/csv/', views.export_allocations_csv, name='export_allocations_csv'),
]
