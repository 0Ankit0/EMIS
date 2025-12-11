"""API URLs for reports app"""
from django.urls import path, include

urlpatterns = [
    path('', include('apps.reports.api.urls')),
]

