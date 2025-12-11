"""Calendar API Views"""
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models

from ..models import Calendar
from ..serializers import CalendarSerializer


class CalendarViewSet(viewsets.ModelViewSet):
    """ViewSet for Calendar"""
    serializer_class = CalendarSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['calendar_type', 'visibility', 'is_active']
    search_fields = ['name', 'description']
    
    def get_queryset(self):
        """Return calendars owned by or shared with the user"""
        user = self.request.user
        return Calendar.objects.filter(
            models.Q(owner=user) | models.Q(shared_with=user)
        ).distinct()
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
