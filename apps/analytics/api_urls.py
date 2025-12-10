"""API URLs for analytics app"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.dashboard import DashboardViewSet

router = DefaultRouter()
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

urlpatterns = router.urls


