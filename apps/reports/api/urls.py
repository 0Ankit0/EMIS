"""API URLs for reports app"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'templates', api_views.ReportTemplateViewSet, basename='reporttemplate')
router.register(r'generated', api_views.GeneratedReportViewSet, basename='generatedreport')
router.register(r'scheduled', api_views.ScheduledReportViewSet, basename='scheduledreport')
router.register(r'widgets', api_views.ReportWidgetViewSet, basename='reportwidget')
router.register(r'favorites', api_views.ReportFavoriteViewSet, basename='reportfavorite')
router.register(r'access-logs', api_views.ReportAccessLogViewSet, basename='reportaccesslog')

urlpatterns = [
    path('', include(router.urls)),
]

