"""API URLs for faculty app"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'departments', api_views.DepartmentViewSet, basename='department')
router.register(r'faculty', api_views.FacultyViewSet, basename='faculty')
router.register(r'qualifications', api_views.FacultyQualificationViewSet, basename='qualification')
router.register(r'experiences', api_views.FacultyExperienceViewSet, basename='experience')
router.register(r'attendance', api_views.FacultyAttendanceViewSet, basename='attendance')
router.register(r'leaves', api_views.FacultyLeaveViewSet, basename='leave')
router.register(r'publications', api_views.FacultyPublicationViewSet, basename='publication')
router.register(r'awards', api_views.FacultyAwardViewSet, basename='award')

urlpatterns = [
    path('', include(router.urls)),
]

