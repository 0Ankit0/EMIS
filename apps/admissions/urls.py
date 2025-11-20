"""
Admissions URL Configuration
Complete CRUD and additional operations
"""
from django.urls import path
from . import views

app_name = 'admissions'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Application CRUD Operations
    path('applications/', views.application_list, name='application_list'),
    path('applications/create/', views.application_create, name='application_create'),
    path('applications/<uuid:pk>/', views.application_detail, name='application_detail'),
    path('applications/<uuid:pk>/update/', views.application_update, name='application_update'),
    path('applications/<uuid:pk>/delete/', views.application_delete, name='application_delete'),
    
    # Bulk Operations
    path('applications/bulk-delete/', views.bulk_delete, name='bulk_delete'),
    path('applications/bulk-update-status/', views.bulk_update_status, name='bulk_update_status'),
    
    # Export Operations
    path('export/csv/', views.export_csv, name='export_csv'),
    path('export/pdf/', views.export_pdf, name='export_pdf'),
    
    # AJAX/API Operations
    path('applications/<uuid:pk>/data/', views.get_application_data, name='get_application_data'),
    path('applications/<uuid:pk>/toggle-status/', views.toggle_status, name='toggle_status'),
    
    # Statistics and Reports
    path('statistics/', views.statistics, name='statistics'),
    path('search/', views.search, name='search'),
    
    # Merit List Operations
    path('merit-lists/', views.merit_list_list, name='merit_list_list'),
    path('merit-lists/create/', views.merit_list_create, name='merit_list_create'),
    path('merit-lists/<uuid:pk>/', views.merit_list_detail, name='merit_list_detail'),
    path('merit-lists/<uuid:pk>/publish/', views.merit_list_publish, name='merit_list_publish'),
]
