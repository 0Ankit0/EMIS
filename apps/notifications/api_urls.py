"""API URLs for notifications app"""
from django.urls import path, include

urlpatterns = [
    path('', include('apps.notifications.api.urls')),
]
