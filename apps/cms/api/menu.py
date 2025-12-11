"""Menu API Views"""
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from ..models import Menu, MenuItem
from ..serializers import MenuSerializer, MenuItemSerializer


class MenuViewSet(viewsets.ModelViewSet):
    """ViewSet for Menu"""
    queryset = Menu.objects.filter(is_active=True)
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['location']


class MenuItemViewSet(viewsets.ModelViewSet):
    """ViewSet for MenuItem"""
    queryset = MenuItem.objects.filter(is_active=True)
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['menu', 'parent']
