"""
Reports URL Configuration
"""
from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Report Templates
    path('templates/', views.template_list, name='template_list'),
    path('templates/create/', views.template_create, name='template_create'),
    path('templates/<int:pk>/', views.template_detail, name='template_detail'),
    path('templates/<int:pk>/update/', views.template_update, name='template_update'),
    path('templates/<int:pk>/delete/', views.template_delete, name='template_delete'),
    
    # Report Generation
    path('generate/<int:template_id>/', views.generate_report, name='generate_report'),
    
    # Generated Reports
    path('generated/', views.generated_list, name='generated_list'),
    path('generated/<int:pk>/', views.generated_detail, name='generated_detail'),
    path('generated/<int:pk>/download/', views.download_report, name='download_report'),
    path('generated/<int:pk>/delete/', views.delete_generated, name='delete_generated'),
    
    # Scheduled Reports
    path('scheduled/', views.scheduled_list, name='scheduled_list'),
    path('scheduled/create/', views.scheduled_create, name='scheduled_create'),
    path('scheduled/<int:pk>/update/', views.scheduled_update, name='scheduled_update'),
    path('scheduled/<int:pk>/delete/', views.scheduled_delete, name='scheduled_delete'),
    
    # Favorites
    path('favorites/', views.favorites_list, name='favorites_list'),
    path('favorites/toggle/<int:template_id>/', views.toggle_favorite, name='toggle_favorite'),
    
    # API-style endpoints
    path('api/categories/', views.template_categories, name='template_categories'),
    path('api/stats/', views.report_stats, name='report_stats'),
]
