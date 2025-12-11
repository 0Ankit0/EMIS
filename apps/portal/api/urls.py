from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'dashboards', views.DashboardViewSet, basename='dashboard')
router.register(r'widgets', views.WidgetViewSet, basename='widget')
router.register(r'quick-links', views.QuickLinkViewSet, basename='quicklink')
router.register(r'announcements', views.AnnouncementViewSet, basename='announcement')
router.register(r'student-profiles', views.StudentPortalProfileViewSet, basename='student-profile')
router.register(r'faculty-profiles', views.FacultyPortalProfileViewSet, basename='faculty-profile')
router.register(r'activities', views.PortalActivityViewSet, basename='activity')
router.register(r'settings', views.PortalSettingsViewSet, basename='settings')

urlpatterns = [
    path('', include(router.urls)),
]
