from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from ..serializers import PermissionSerializer, ContentTypeSerializer


class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get_queryset(self):
        queryset = Permission.objects.all()
        
        # Filter by content type
        content_type = self.request.query_params.get('content_type')
        if content_type:
            queryset = queryset.filter(content_type__id=content_type)
        
        # Search by name or codename
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                name__icontains=search
            ) | queryset.filter(
                codename__icontains=search
            )
        
        return queryset.select_related('content_type').order_by('content_type', 'codename')


class ContentTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get_queryset(self):
        return ContentType.objects.all().order_by('app_label', 'model')
