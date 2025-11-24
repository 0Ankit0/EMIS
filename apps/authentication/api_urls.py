"""
Authentication API URLs
"""
from django.urls import path
from apps.authentication import api_views

app_name = 'authentication_api'

urlpatterns = [
    path('register/', api_views.register, name='register'),
    path('login/', api_views.login, name='login'),
    path('logout/', api_views.logout, name='logout'),
    path('me/', api_views.me, name='me'),
    path('refresh/', api_views.refresh_token, name='refresh'),
]
