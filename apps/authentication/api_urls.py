"""
Authentication API URLs
"""
from django.urls import path
from apps.authentication.api import auth

app_name = 'authentication_api'

urlpatterns = [
    path('register/', auth.register, name='register'),
    path('login/', auth.login, name='login'),
    path('logout/', auth.logout, name='logout'),
    path('me/', auth.me, name='me'),
]

