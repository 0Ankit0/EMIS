"""API URLs for library app"""
from django.urls import path, include

urlpatterns = [
    path('', include('apps.library.api.urls')),
]

