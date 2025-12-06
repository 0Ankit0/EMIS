from rest_framework import viewsets
from ..models.guardian import Guardian
from ..serializers.guardian import (
    GuardianCreateSerializer,
    GuardianUpdateSerializer,
    GuardianResponseSerializer
)

class GuardianViewSet(viewsets.ModelViewSet):
    queryset = Guardian.objects.all()
    lookup_field = 'ukid'
    
    def get_serializer_class(self):
        if self.action == 'create':
            return GuardianCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return GuardianUpdateSerializer
        return GuardianResponseSerializer
