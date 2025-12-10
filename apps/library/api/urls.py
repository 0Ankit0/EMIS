"""API URLs for library app"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'books', api_views.BookViewSet, basename='book')
router.register(r'issues', api_views.BookIssueViewSet, basename='issue')
router.register(r'members', api_views.LibraryMemberViewSet, basename='member')

urlpatterns = [
    path('', include(router.urls)),
]

