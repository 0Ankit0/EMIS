"""Hostel API URLs"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'hostels', api_views.HostelViewSet, basename='hostel')
router.register(r'floors', api_views.FloorViewSet, basename='floor')
router.register(r'rooms', api_views.RoomViewSet, basename='room')
router.register(r'allocations', api_views.RoomAllocationViewSet, basename='allocation')
router.register(r'fees', api_views.HostelFeeViewSet, basename='fee')
router.register(r'mess-menus', api_views.MessMenuViewSet, basename='mess-menu')
router.register(r'visitors', api_views.VisitorLogViewSet, basename='visitor')
router.register(r'complaints', api_views.ComplaintViewSet, basename='complaint')
router.register(r'outings', api_views.OutingRequestViewSet, basename='outing')
router.register(r'attendance', api_views.AttendanceViewSet, basename='attendance')

urlpatterns = [
    path('', include(router.urls)),
]
