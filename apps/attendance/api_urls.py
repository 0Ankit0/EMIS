from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'sessions', api_views.AttendanceSessionViewSet, basename='session')
router.register(r'records', api_views.AttendanceRecordViewSet, basename='record')

urlpatterns = router.urls
