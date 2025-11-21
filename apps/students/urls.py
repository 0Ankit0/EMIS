"""
Students URL Configuration
Complete CRUD and additional operations
"""
from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # CRUD Operations
    path('list/', views.item_list, name='list'),
    path('create/', views.item_create, name='create'),
    path('<int:pk>/', views.item_detail, name='detail'),
    path('<int:pk>/update/', views.item_update, name='update'),
    path('<int:pk>/delete/', views.item_delete, name='delete'),
    
    # Bulk Operations
    path('bulk-delete/', views.bulk_delete, name='bulk_delete'),
    path('bulk-update-status/', views.bulk_update_status, name='bulk_update_status'),
    
    # Export Operations
    path('export/csv/', views.export_csv, name='export_csv'),
    path('export/pdf/', views.export_pdf, name='export_pdf'),
    
    # AJAX/API Operations
    path('<int:pk>/data/', views.get_item_data, name='get_data'),
    path('<int:pk>/toggle-status/', views.toggle_status, name='toggle_status'),
    
    # Statistics and Reports
    path('statistics/', views.statistics, name='statistics'),
    path('search/', views.search, name='search'),
]
