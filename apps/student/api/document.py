from rest_framework import viewsets
from django.utils import timezone
from ..models.document import Document
from ..serializers.document import (
    DocumentCreateSerializer,
    DocumentUpdateSerializer,
    DocumentResponseSerializer
)

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    lookup_field = 'ukid'
    
    def get_serializer_class(self):
        if self.action == 'create':
            return DocumentCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return DocumentUpdateSerializer
        return DocumentResponseSerializer
    
    def perform_update(self, serializer):
        """Auto-set verification fields when marking as verified"""
        if serializer.validated_data.get('is_verified') and not self.get_object().is_verified:
            serializer.save(
                verified_at=timezone.now(),
                verified_by=self.request.user.username if hasattr(self.request, 'user') and self.request.user.is_authenticated else None
            )
        else:
            serializer.save()
