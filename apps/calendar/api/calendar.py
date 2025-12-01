from rest_framework import viewsets
from ..models.calendar import Calendar
from ..serializers.calendar import CalendarSerializer

class CalendarViewSet(viewsets.ModelViewSet):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer

    #TODO: Add calendar layout for managing how the calendar view shows the calendar and the events.
