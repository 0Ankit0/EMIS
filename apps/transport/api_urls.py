"""API URLs for transport app"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'vehicles', api_views.VehicleViewSet, basename='vehicle')
router.register(r'routes', api_views.RouteViewSet, basename='route')
router.register(r'stops', api_views.RouteStopViewSet, basename='stop')
router.register(r'drivers', api_views.DriverViewSet, basename='driver')
router.register(r'assignments', api_views.StudentTransportAssignmentViewSet, basename='assignment')
router.register(r'maintenance', api_views.VehicleMaintenanceViewSet, basename='maintenance')
router.register(r'fuel-logs', api_views.FuelLogViewSet, basename='fuel-log')

urlpatterns = router.urls
