from rest_framework import viewsets
from .models import Event, Category, Calendar
from .serializers import EventSerializer, CategorySerializer, CalendarSerializer

# syntax is <ModelName>ViewSet(viewsets.ModelViewSet)
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CalendarViewSet(viewsets.ModelViewSet):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer

    #TODO: Add calendar layout for managing how the calendar view shows the calendar and the events.
    