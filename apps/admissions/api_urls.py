"""API URLs for admissions app"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'applications', api_views.ApplicationViewSet, basename='application')
router.register(r'merit-lists', api_views.MeritListViewSet, basename='merit-list')

urlpatterns = router.urls

