from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import CalendarViewSet, EventViewSet, CategoryViewSet, CalendarLayoutViewSet

router = DefaultRouter()
router.register(r'calendars', CalendarViewSet)
router.register(r'events', EventViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'layouts', CalendarLayoutViewSet, basename='layout')

urlpatterns = [
    path('', include(router.urls)),
]
