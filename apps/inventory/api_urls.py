"""Inventory API URLs"""
from django.urls import path, include

urlpatterns = [
    path('', include('apps.inventory.api.urls')),
]
