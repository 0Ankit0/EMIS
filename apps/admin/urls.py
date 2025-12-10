from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import UserViewSet, GroupViewSet, PermissionViewSet, ContentTypeViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'permissions', PermissionViewSet, basename='permission')
router.register(r'content-types', ContentTypeViewSet, basename='content-type')

urlpatterns = [
    path('', include(router.urls)),
]
