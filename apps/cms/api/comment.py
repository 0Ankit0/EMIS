"""Comment API Views"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from ..models import Comment
from ..serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for Comment"""
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['post', 'is_approved']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = Comment.objects.select_related('author', 'post')
        
        # Public users see only approved comments
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_approved=True)
        
        return queryset
    
    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(author=self.request.user)
        else:
            serializer.save()
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve a comment"""
        comment = self.get_object()
        comment.is_approved = True
        comment.save()
        serializer = self.get_serializer(comment)
        return Response(serializer.data)
