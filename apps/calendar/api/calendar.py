from django.utils import timezone
from rest_framework import viewsets
from ..models.calendar import Calendar
from ..serializers.calendar import (
    CalendarCreateSerializer,
    CalendarUpdateSerializer,
    CalendarResponseSerializer
)
from rest_framework.permissions import IsAuthenticated

class CalendarViewSet(viewsets.ModelViewSet):
    queryset = Calendar.objects.all()
    permission_classes = [IsAuthenticated] 
    lookup_field = 'ukid'

    def get_queryset(self): # type: ignore
        user = self.request.user
        if  user.is_staff or user.is_superuser:
            return Calendar.objects.all()
        return Calendar.objects.filter(end_date__gte=timezone.now().date())
    
    def get_serializer_class(self): # type: ignore
        if self.action == 'create':
            return CalendarCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return CalendarUpdateSerializer
        return CalendarResponseSerializer

    #TODO: Add calendar layout for managing how the calendar view shows the calendar and the events.
