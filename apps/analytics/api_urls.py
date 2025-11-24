"""API URLs for analytics app"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'metrics', api_views.DashboardMetricViewSet, basename='metric')
router.register(r'reports', api_views.ReportViewSet, basename='report')

urlpatterns = router.urls

