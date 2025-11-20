"""
Attendance URL Configuration
"""
from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Attendance Records
    path('records/', views.record_list, name='record_list'),
    path('records/create/', views.record_create, name='record_create'),
    path('records/<uuid:pk>/', views.record_detail, name='record_detail'),
    path('records/<uuid:pk>/update/', views.record_update, name='record_update'),
    path('records/<uuid:pk>/delete/', views.record_delete, name='record_delete'),
    
    # Attendance Sessions
    path('sessions/', views.session_list, name='session_list'),
    path('sessions/create/', views.session_create, name='session_create'),
    path('sessions/<uuid:pk>/', views.session_detail, name='session_detail'),
    path('sessions/<uuid:pk>/update/', views.session_update, name='session_update'),
    path('sessions/<uuid:pk>/mark/', views.bulk_mark_attendance, name='bulk_mark'),
    
    # Reports
    path('reports/student/<uuid:student_id>/', views.student_attendance_report, name='student_report'),
    path('reports/course/<uuid:course_id>/', views.course_attendance_report, name='course_report'),
    
    # API Endpoints
    path('api/mark/', views.api_mark_attendance, name='api_mark'),
    path('api/session/<uuid:session_id>/stats/', views.api_session_stats, name='api_session_stats'),
]
