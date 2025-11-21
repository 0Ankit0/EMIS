"""API URLs for notifications app"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'notifications', api_views.NotificationViewSet, basename='notification')
router.register(r'templates', api_views.NotificationTemplateViewSet, basename='template')
router.register(r'preferences', api_views.NotificationPreferenceViewSet, basename='preference')
router.register(r'scheduled', api_views.ScheduledNotificationViewSet, basename='scheduled')
router.register(r'logs', api_views.NotificationLogViewSet, basename='log')

urlpatterns = [
    path('', include(router.urls)),
]
