"""
Core API URL patterns
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('apps.authentication.api_urls')),
    path('students/', include('apps.students.api_urls')),
    path('faculty/', include('apps.faculty.api_urls')),
    path('hr/', include('apps.hr.api_urls')),
    path('finance/', include('apps.finance.api_urls')),
    path('library/', include('apps.library.api_urls')),
    path('admissions/', include('apps.admissions.api_urls')),
    path('exams/', include('apps.exams.api_urls')),
    path('attendance/', include('apps.attendance.api_urls')),
    path('lms/', include('apps.lms.api_urls')),
    path('analytics/', include('apps.analytics.api_urls')),
    path('notifications/', include('apps.notifications.api_urls')),
    path('reports/', include('apps.reports.api_urls')),
]
