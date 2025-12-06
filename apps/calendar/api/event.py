from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from ..models.event import Event, EventStatus
from ..serializers.event import (
    EventCreateSerializer,
    EventUpdateSerializer,
    EventResponseSerializer
)
from rest_framework.permissions import IsAuthenticated

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'ukid'
    filterset_fields = ['category', 'type', 'calendar', 'start_date', 'end_date']
    
    def get_serializer_class(self): # type: ignore
        if self.action == 'create':
            return EventCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return EventUpdateSerializer
        return EventResponseSerializer
    
    def get_queryset(self): # type: ignore
        user = self.request.user
        if not user.is_staff or user.is_superuser:
            return Event.objects.all()
        return Event.objects.filter(status=EventStatus.PUBLISHED)

    @action(detail=False, methods=['get'])
    def analytics(self, request):
        total_events = Event.objects.count()
        
        # Upcoming events (next 30 days)
        today = timezone.now().date()
        thirty_days_later = today + timedelta(days=30)
        upcoming_events = Event.objects.filter(
            start_date__gte=today,
            start_date__lte=thirty_days_later
        ).count()

        # Events by category
        events_by_category = Event.objects.values('category__name').annotate(
            count=Count('id')
        ).order_by('-count')

        # Events by status
        events_by_status = Event.objects.values('status').annotate(
            count=Count('id')
        ).order_by('-count')

        return Response({
            'total_events': total_events,
            'upcoming_events': upcoming_events,
            'events_by_category': events_by_category,
            'events_by_status': events_by_status
        })
