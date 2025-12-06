from rest_framework import viewsets
from ..models.academic_record import AcademicRecord
from ..serializers.academic_record import (
    AcademicRecordCreateSerializer,
    AcademicRecordUpdateSerializer,
    AcademicRecordResponseSerializer
)

class AcademicRecordViewSet(viewsets.ModelViewSet):
    queryset = AcademicRecord.objects.all()
    lookup_field = 'ukid'
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AcademicRecordCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return AcademicRecordUpdateSerializer
        return AcademicRecordResponseSerializer
