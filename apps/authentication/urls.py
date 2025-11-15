"""
Authentication URL patterns - Frontend
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'authentication'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='authentication:login'), name='logout'),
    path('register/', views.register_view, name='register'),
    path('password-reset/', views.password_reset_view, name='password_reset'),
    path('password-change/', views.password_change_view, name='password_change'),
    path('profile/', views.profile_view, name='profile'),
    path('setup-2fa/', views.setup_2fa_view, name='setup_2fa'),
]
