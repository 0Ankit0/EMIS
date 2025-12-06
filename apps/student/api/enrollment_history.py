from rest_framework import viewsets
from ..models.enrollment_history import EnrollmentHistory
from ..serializers.enrollment_history import (
    EnrollmentHistoryCreateSerializer,
    EnrollmentHistoryUpdateSerializer,
    EnrollmentHistoryResponseSerializer
)

class EnrollmentHistoryViewSet(viewsets.ModelViewSet):
    queryset = EnrollmentHistory.objects.all()
    lookup_field = 'ukid'
    
    def get_serializer_class(self):
        if self.action == 'create':
            return EnrollmentHistoryCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return EnrollmentHistoryUpdateSerializer
        return EnrollmentHistoryResponseSerializer
