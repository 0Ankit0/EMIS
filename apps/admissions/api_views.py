"""Admissions API Views"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q

from .models import Application, MeritList
from .serializers import (
    ApplicationCreateSerializer, ApplicationUpdateSerializer, ApplicationResponseSerializer,
    MeritListCreateSerializer, MeritListResponseSerializer, MeritListDetailSerializer
)


class ApplicationViewSet(viewsets.ModelViewSet):
    """ViewSet for Application management"""
    queryset = Application.objects.all()
    serializer_class = ApplicationResponseSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'program', 'admission_year', 'admission_semester']
    search_fields = ['application_number', 'first_name', 'last_name', 'email']
    ordering_fields = ['created_at', 'merit_score', 'rank']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ApplicationCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ApplicationUpdateSerializer
        return ApplicationResponseSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def approve(self, request, pk=None):
        """Approve an application"""
        application = self.get_object()
        if application.status != 'submitted':
            return Response(
                {'error': 'Only submitted applications can be approved'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        application.status = 'approved'
        application.save()
        return Response({'message': 'Application approved successfully'})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def reject(self, request, pk=None):
        """Reject an application"""
        application = self.get_object()
        application.status = 'rejected'
        application.save()
        return Response({'message': 'Application rejected'})
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get application statistics"""
        queryset = self.get_queryset()
        stats = {
            'total': queryset.count(),
            'by_status': dict(queryset.values('status').annotate(count=Count('id')).values_list('status', 'count')),
            'by_program': dict(queryset.values('program').annotate(count=Count('id')).values_list('program', 'count')),
        }
        return Response(stats)


class MeritListViewSet(viewsets.ModelViewSet):
    """ViewSet for Merit List management"""
    queryset = MeritList.objects.all()
    serializer_class = MeritListResponseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['program', 'admission_year', 'admission_semester', 'is_published']
    ordering_fields = ['created_at', 'cutoff_rank']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return MeritListCreateSerializer
        elif self.action == 'retrieve':
            return MeritListDetailSerializer
        return MeritListResponseSerializer
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """Publish a merit list"""
        merit_list = self.get_object()
        merit_list.is_published = True
        merit_list.save()
        return Response({'message': 'Merit list published successfully'})
