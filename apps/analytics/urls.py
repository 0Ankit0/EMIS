"""
Analytics URL Configuration
"""
from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Detailed Analytics
    path('admissions/', views.admissions_analytics, name='admissions_analytics'),
    path('attendance/', views.attendance_analytics, name='attendance_analytics'),
    path('financial/', views.financial_analytics, name='financial_analytics'),
    path('academic/', views.academic_analytics, name='academic_analytics'),
    
    # Reports
    path('reports/', views.report_list, name='report_list'),
    path('reports/create/', views.report_create, name='report_create'),
    path('reports/<uuid:pk>/', views.report_detail, name='report_detail'),
    path('reports/<uuid:pk>/delete/', views.report_delete, name='report_delete'),
    path('reports/<uuid:pk>/download/', views.report_download, name='report_download'),
    
    # Analytics Queries
    path('queries/', views.query_list, name='query_list'),
    path('queries/create/', views.query_create, name='query_create'),
    path('queries/<uuid:pk>/', views.query_detail, name='query_detail'),
    
    # API Endpoints
    path('api/summary/', views.api_dashboard_summary, name='api_dashboard_summary'),
    path('api/refresh/', views.api_refresh_metrics, name='api_refresh_metrics'),
    path('api/chart-data/', views.api_chart_data, name='api_chart_data'),
]
