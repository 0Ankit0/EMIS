from rest_framework import viewsets
from ..models.enrollment import Enrollment
from ..serializers.enrollment import (
    EnrollmentCreateSerializer,
    EnrollmentUpdateSerializer,
    EnrollmentResponseSerializer
)

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    lookup_field = 'ukid'
    
    def get_serializer_class(self):
        if self.action == 'create':
            return EnrollmentCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return EnrollmentUpdateSerializer
        return EnrollmentResponseSerializer
