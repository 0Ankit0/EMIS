"""
Faculty URL Configuration
"""
from django.urls import path
from . import views

app_name = 'faculty'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Faculty CRUD
    path('list/', views.faculty_list, name='list'),
    path('create/', views.faculty_create, name='create'),
    path('<uuid:pk>/', views.faculty_detail, name='detail'),
    path('<uuid:pk>/update/', views.faculty_update, name='update'),
    path('<uuid:pk>/delete/', views.faculty_delete, name='delete'),
    
    # Attendance
    path('attendance/', views.attendance_list, name='attendance_list'),
    
    # Leaves
    path('leaves/', views.leave_list, name='leave_list'),
    
    # Export
    path('export/csv/', views.export_csv, name='export_csv'),
]
