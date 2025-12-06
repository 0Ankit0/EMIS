from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import (
    StudentViewSet,
    EnrollmentViewSet,
    GuardianViewSet,
    AcademicRecordViewSet,
    DocumentViewSet,
    EnrollmentHistoryViewSet
)

router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')
router.register(r'guardians', GuardianViewSet, basename='guardian')
router.register(r'academic-records', AcademicRecordViewSet, basename='academic-record')
router.register(r'documents', DocumentViewSet, basename='document')
router.register(r'enrollment-history', EnrollmentHistoryViewSet, basename='enrollment-history')

urlpatterns = [
    path('', include(router.urls)),
]
