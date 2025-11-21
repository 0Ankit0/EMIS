from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'dashboards', api_views.DashboardViewSet, basename='dashboard')
router.register(r'widgets', api_views.WidgetViewSet, basename='widget')
router.register(r'quick-links', api_views.QuickLinkViewSet, basename='quicklink')
router.register(r'announcements', api_views.AnnouncementViewSet, basename='announcement')
router.register(r'student-profiles', api_views.StudentPortalProfileViewSet, basename='student-profile')
router.register(r'faculty-profiles', api_views.FacultyPortalProfileViewSet, basename='faculty-profile')
router.register(r'activities', api_views.PortalActivityViewSet, basename='activity')
router.register(r'settings', api_views.PortalSettingsViewSet, basename='settings')

urlpatterns = [
    path('', include(router.urls)),
]
