"""API URLs for admissions app"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.applications import ApplicationViewSet
from .api.merit_lists import MeritListViewSet

router = DefaultRouter()
router.register(r'applications', ApplicationViewSet, basename='application')
router.register(r'merit-lists', MeritListViewSet, basename='merit-list')

urlpatterns = router.urls

