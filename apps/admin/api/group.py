from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from ..serializers import (
    GroupListSerializer,
    GroupDetailSerializer,
    GroupCreateSerializer,
    GroupUpdateSerializer
)

User = get_user_model()


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get_serializer_class(self): # type: ignore
        if self.action == 'list':
            return GroupListSerializer
        elif self.action == 'create':
            return GroupCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return GroupUpdateSerializer
        return GroupDetailSerializer
    
    def get_queryset(self): # type: ignore 
        queryset = Group.objects.all()
        
        # Search by name
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        return queryset.order_by('name')
    
    @action(detail=True, methods=['post'])
    def add_user(self, request, pk=None):
        """Add a user to the group"""
        group = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response(
                {'error': 'user_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(pk=user_id)
            group.user_set.add(user)
            serializer = self.get_serializer(group)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def remove_user(self, request, pk=None):
        """Remove a user from the group"""
        group = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response(
                {'error': 'user_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(pk=user_id)
            group.user_set.remove(user)
            serializer = self.get_serializer(group)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
