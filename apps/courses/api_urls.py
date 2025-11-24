"""Courses API URL Configuration"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'courses', api_views.CourseViewSet, basename='course')
router.register(r'modules', api_views.ModuleViewSet, basename='module')
router.register(r'assignments', api_views.AssignmentViewSet, basename='assignment')
router.register(r'submissions', api_views.SubmissionViewSet, basename='submission')
router.register(r'grades', api_views.GradeRecordViewSet, basename='grade')

urlpatterns = router.urls
