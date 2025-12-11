"""API URLs for notifications app"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'notifications', views.NotificationViewSet, basename='notification')
router.register(r'templates', views.NotificationTemplateViewSet, basename='template')
router.register(r'preferences', views.NotificationPreferenceViewSet, basename='preference')
router.register(r'scheduled', views.ScheduledNotificationViewSet, basename='scheduled')
router.register(r'logs', views.NotificationLogViewSet, basename='log')

urlpatterns = [
    path('', include(router.urls)),
]
