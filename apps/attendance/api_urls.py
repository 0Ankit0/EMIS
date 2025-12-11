"""API URLs for attendance app"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import (
    AttendanceRecordViewSet,
    AttendanceSessionViewSet,
    AttendancePolicyViewSet,
    AttendanceReportViewSet
)

router = DefaultRouter()
router.register(r'records', AttendanceRecordViewSet, basename='attendance-record')
router.register(r'sessions', AttendanceSessionViewSet, basename='attendance-session')
router.register(r'policies', AttendancePolicyViewSet, basename='attendance-policy')
router.register(r'reports', AttendanceReportViewSet, basename='attendance-report')

urlpatterns = [
    path('', include(router.urls)),
]

