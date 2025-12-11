"""API URLs for library app"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'books', views.BookViewSet, basename='book')
router.register(r'issues', views.BookIssueViewSet, basename='issue')
router.register(r'members', views.LibraryMemberViewSet, basename='member')

urlpatterns = [
    path('', include(router.urls)),
]

