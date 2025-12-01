from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import CalendarViewSet, EventViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'calendars', CalendarViewSet)
router.register(r'events', EventViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
