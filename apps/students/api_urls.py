"""API URLs for students app"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'students', api_views.StudentViewSet, basename='student')

urlpatterns = router.urls
