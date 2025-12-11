"""API URLs for lms app"""
from django.urls import path, include

urlpatterns = [
    path('', include('apps.lms.api.urls')),
]

