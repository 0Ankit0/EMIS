from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from ..models.event import Event
from ..serializers.event import EventSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

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
