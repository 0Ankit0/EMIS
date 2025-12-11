"""API URLs for reports app"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'templates', views.ReportTemplateViewSet, basename='reporttemplate')
router.register(r'generated', views.GeneratedReportViewSet, basename='generatedreport')
router.register(r'scheduled', views.ScheduledReportViewSet, basename='scheduledreport')
router.register(r'widgets', views.ReportWidgetViewSet, basename='reportwidget')
router.register(r'favorites', views.ReportFavoriteViewSet, basename='reportfavorite')
router.register(r'access-logs', views.ReportAccessLogViewSet, basename='reportaccesslog')

urlpatterns = [
    path('', include(router.urls)),
]

