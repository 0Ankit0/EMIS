from rest_framework import viewsets, permissions
from apps.calendar.models import CalendarLayout
from apps.calendar.serializers.layout import CalendarLayoutSerializer

class CalendarLayoutViewSet(viewsets.ModelViewSet):
    serializer_class = CalendarLayoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CalendarLayout.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
