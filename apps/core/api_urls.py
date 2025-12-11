"""Core API URL configuration"""
from django.urls import path, include
from apps.core.api.health import health_check, readiness_check, liveness_check
from apps.core.api.metrics import metrics

urlpatterns = [
    # Health and monitoring endpoints
    path('health/', health_check, name='health'),
    path('readiness/', readiness_check, name='readiness'),
    path('liveness/', liveness_check, name='liveness'),
    path('metrics/', metrics, name='metrics'),
    
    # Authentication URLs
    path('auth/', include('apps.authentication.api_urls')),
    
    # Admissions URLs
    path('admissions/', include('apps.admissions.api_urls')),
    
    # Students URLs
    path('students/', include('apps.students.api_urls')),
    
    # Courses URLs
    path('courses/', include('apps.courses.api_urls')),
    
    # Inventory URLs
    path('inventory/', include('apps.inventory.api_urls')),
    
    # LMS URLs
    path('lms/', include('apps.lms.api_urls')),
    
    # Library URLs
    path('library/', include('apps.library.api_urls')),
    
    # Transport URLs
    path('transport/', include('apps.transport.api_urls')),
    
    # Notifications URLs
    path('notifications/', include('apps.notifications.api_urls')),
    
    # Portal URLs
    path('portal/', include('apps.portal.api_urls')),
    
    # Reports URLs
    path('reports/', include('apps.reports.api_urls')),
]
