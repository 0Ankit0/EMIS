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
    
    # Module APIs
    path('admissions/', include('apps.admissions.api_urls')),
    path('students/', include('apps.students.api_urls')),
    path('courses/', include('apps.courses.api_urls')),
    path('faculty/', include('apps.faculty.api_urls')),
    path('finance/', include('apps.finance.api_urls')),
    path('exams/', include('apps.exams.api_urls')),
    path('library/', include('apps.library.api_urls')),
    path('hr/', include('apps.hr.api_urls')),
    path('hostel/', include('apps.hostel.api_urls')),
    path('transport/', include('apps.transport.api_urls')),
    path('inventory/', include('apps.inventory.api_urls')),
    path('timetable/', include('apps.timetable.api_urls')),
    path('attendance/', include('apps.attendance.api_urls')),
    path('lms/', include('apps.lms.api_urls')),
    path('analytics/', include('apps.analytics.api_urls')),
    path('reports/', include('apps.reports.api_urls')),
    path('notifications/', include('apps.notifications.api_urls')),
    # path('portal/', include('apps.portal.api_urls')),  # TODO: Fix Enrollment import
    path('cms/', include('apps.cms.api_urls')),
]
