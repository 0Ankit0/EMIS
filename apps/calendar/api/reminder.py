"""Event Reminder API Views"""
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from ..models import EventReminder
from ..serializers import EventReminderSerializer


class EventReminderViewSet(viewsets.ModelViewSet):
    """ViewSet for EventReminder"""
    serializer_class = EventReminderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['event', 'is_sent', 'reminder_type']
    
    def get_queryset(self):
        return EventReminder.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
