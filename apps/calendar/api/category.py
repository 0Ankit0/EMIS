"""Event Category API Views"""
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated

from ..models import EventCategory
from ..serializers import EventCategorySerializer


class EventCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for EventCategory"""
    queryset = EventCategory.objects.filter(is_active=True)
    serializer_class = EventCategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
