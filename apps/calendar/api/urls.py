"""Calendar API URLs"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import (
    EventCategoryViewSet,
    CalendarViewSet,
    EventViewSet,
    EventReminderViewSet
)

router = DefaultRouter()
router.register(r'categories', EventCategoryViewSet, basename='category')
router.register(r'calendars', CalendarViewSet, basename='calendar')
router.register(r'events', EventViewSet, basename='event')
router.register(r'reminders', EventReminderViewSet, basename='reminder')

urlpatterns = [
    path('', include(router.urls)),
]
