"""
Exams API URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import ExamViewSet, ExamResultViewSet, ExamScheduleViewSet

router = DefaultRouter()
router.register(r'exams', ExamViewSet, basename='exam')
router.register(r'results', ExamResultViewSet, basename='examresult')
router.register(r'schedules', ExamScheduleViewSet, basename='examschedule')

urlpatterns = [
    path('', include(router.urls)),
]
