"""
Notifications URL Configuration
Complete CRUD and additional operations
"""
from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Notification CRUD Operations
    path('list/', views.notification_list, name='list'),
    path('<int:pk>/', views.notification_detail, name='detail'),
    path('<int:pk>/mark-read/', views.mark_as_read, name='mark_read'),
    path('<int:pk>/mark-unread/', views.mark_as_unread, name='mark_unread'),
    path('<int:pk>/delete/', views.delete_notification, name='delete'),
    path('mark-all-read/', views.mark_all_as_read, name='mark_all_read'),
    
    # Send Notifications (Admin)
    path('send/', views.send_notification_view, name='send'),
    
    # Templates (Admin)
    path('templates/', views.template_list, name='templates'),
    path('templates/<int:pk>/', views.template_detail, name='template_detail'),
    
    # Scheduled Notifications (Admin)
    path('scheduled/', views.scheduled_list, name='scheduled'),
    
    # Preferences
    path('preferences/', views.preferences, name='preferences'),
    
    # Recipients (Admin)
    path('recipients/', views.recipients, name='recipients'),
    
    # Statistics (Admin)
    path('statistics/', views.statistics, name='statistics'),
    
    # Export
    path('export/csv/', views.export_csv, name='export_csv'),
    
    # AJAX API
    path('api/unread-count/', views.get_unread_count, name='api_unread_count'),
    path('api/recent/', views.get_recent_notifications, name='api_recent'),
]
