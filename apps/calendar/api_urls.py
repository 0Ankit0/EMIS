"""Calendar API URLs"""
from django.urls import path, include

urlpatterns = [
    path('', include('apps.calendar.api.urls')),
]
