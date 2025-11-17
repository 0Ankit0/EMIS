"""Merit list API views"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from ..models import MeritList
from ..serializers import (
    MeritListCreateSerializer,
    MeritListResponseSerializer,
    MeritListDetailSerializer
)
from ..services import MeritListService
from apps.core.permissions import IsAdminOrReadOnly


class MeritListViewSet(viewsets.ModelViewSet):
    """ViewSet for MeritList CRUD operations"""
    
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['program', 'admission_year', 'admission_semester', 'is_published']
    ordering_fields = ['generation_timestamp', 'version', 'created_at']
    ordering = ['-generation_timestamp']
    
    def get_queryset(self):
        # Regular users can only see published merit lists
        if self.request.user.is_staff or hasattr(self.request.user, 'has_permission'):
            return MeritList.objects.all()
        return MeritList.objects.filter(is_published=True)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return MeritListCreateSerializer
        elif self.action == 'retrieve':
            return MeritListDetailSerializer
        return MeritListResponseSerializer
    
    def create(self, request, *args, **kwargs):
        """Generate a new merit list"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        merit_list = MeritListService.generate_merit_list(
            name=serializer.validated_data['name'],
            program=serializer.validated_data['program'],
            admission_year=serializer.validated_data['admission_year'],
            admission_semester=serializer.validated_data['admission_semester'],
            criteria=serializer.validated_data['criteria'],
            generated_by=request.user,
            cutoff_score=serializer.validated_data.get('cutoff_score'),
            total_seats=serializer.validated_data.get('total_seats')
        )
        
        response_serializer = MeritListResponseSerializer(merit_list)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'], url_path='publish')
    def publish(self, request, pk=None):
        """Publish a merit list"""
        merit_list = self.get_object()
        published_list = MeritListService.publish_merit_list(merit_list)
        
        serializer = MeritListResponseSerializer(published_list)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], url_path='recalculate')
    def recalculate(self, request, pk=None):
        """Recalculate ranks for merit list"""
        merit_list = self.get_object()
        recalculated_list = MeritListService.recalculate_ranks(merit_list)
        
        serializer = MeritListDetailSerializer(recalculated_list)
        return Response(serializer.data)
