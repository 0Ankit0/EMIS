"""
Courses URL Configuration
Complete CRUD and additional operations
"""
from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Course CRUD Operations
    path('list/', views.item_list, name='list'),
    path('create/', views.item_create, name='create'),
    path('<uuid:pk>/', views.item_detail, name='detail'),
    path('<uuid:pk>/update/', views.item_update, name='update'),
    path('<uuid:pk>/delete/', views.item_delete, name='delete'),
    
    # Module Management
    path('<uuid:course_pk>/modules/', views.module_list, name='module_list'),
    path('<uuid:course_pk>/modules/create/', views.module_create, name='module_create'),
    path('modules/<uuid:pk>/', views.module_detail, name='module_detail'),
    path('modules/<uuid:pk>/update/', views.module_update, name='module_update'),
    path('modules/<uuid:pk>/delete/', views.module_delete, name='module_delete'),
    
    # Assignment Management
    path('<uuid:course_pk>/assignments/', views.assignment_list, name='assignment_list'),
    path('<uuid:course_pk>/assignments/create/', views.assignment_create, name='assignment_create'),
    path('assignments/<uuid:pk>/', views.assignment_detail, name='assignment_detail'),
    path('assignments/<uuid:pk>/update/', views.assignment_update, name='assignment_update'),
    path('assignments/<uuid:pk>/delete/', views.assignment_delete, name='assignment_delete'),
    
    # Bulk Operations
    path('bulk-delete/', views.bulk_delete, name='bulk_delete'),
    path('bulk-update-status/', views.bulk_update_status, name='bulk_update_status'),
    
    # Export Operations
    path('export/csv/', views.export_csv, name='export_csv'),
    path('export/pdf/', views.export_pdf, name='export_pdf'),
    
    # AJAX/API Operations
    path('<uuid:pk>/data/', views.get_item_data, name='get_data'),
    path('<uuid:pk>/toggle-status/', views.toggle_status, name='toggle_status'),
    
    # Statistics and Reports
    path('statistics/', views.statistics, name='statistics'),
    path('search/', views.search, name='search'),
    
    # Additional Pages
    path('programs/', views.programs, name='programs'),
    path('syllabus/', views.syllabus_view, name='syllabus'),
    path('enrollments/', views.enrollments, name='enrollments'),
    path('materials/', views.course_materials, name='materials'),
    path('prerequisites/', views.prerequisites, name='prerequisites'),
    path('curriculum/', views.curriculum, name='curriculum'),
]
