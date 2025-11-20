"""
Authentication URL Configuration
"""
from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    
    # 2FA
    path('verify-2fa/', views.verify_2fa, name='verify_2fa'),
    path('setup-2fa/', views.setup_2fa, name='setup_2fa'),
    path('disable-2fa/', views.disable_2fa, name='disable_2fa'),
    
    # Password Reset
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('password-reset/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),
    
    # Security Settings
    path('security/', views.security_settings, name='security_settings'),
    path('session/<uuid:session_id>/terminate/', views.terminate_session, name='terminate_session'),
    path('sessions/terminate-all/', views.terminate_all_sessions, name='terminate_all_sessions'),
]
