"""Event API Views"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db import models
from datetime import timedelta

from ..models import Event, Calendar
from ..serializers import EventSerializer, EventListSerializer, EventReminderSerializer


class EventViewSet(viewsets.ModelViewSet):
    """ViewSet for Event"""
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'priority', 'is_all_day', 'recurrence']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['start_datetime', 'priority', 'title']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return EventListSerializer
        return EventSerializer
    
    def get_queryset(self):
        """Return events from calendars accessible to the user"""
        user = self.request.user
        queryset = Event.objects.filter(
            calendars__in=Calendar.objects.filter(
                models.Q(owner=user) | models.Q(shared_with=user)
            )
        ).distinct()
        
        # Filter by date range if provided
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(start_datetime__gte=start_date)
        if end_date:
            queryset = queryset.filter(end_datetime__lte=end_date)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming events"""
        now = timezone.now()
        events = self.get_queryset().filter(
            start_datetime__gte=now,
            start_datetime__lte=now + timedelta(days=7)
        ).order_by('start_datetime')
        
        serializer = EventListSerializer(events, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's events"""
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)
        
        events = self.get_queryset().filter(
            start_datetime__gte=today_start,
            start_datetime__lt=today_end
        ).order_by('start_datetime')
        
        serializer = EventListSerializer(events, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_reminder(self, request, pk=None):
        """Add a reminder to an event"""
        event = self.get_object()
        serializer = EventReminderSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(event=event, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
