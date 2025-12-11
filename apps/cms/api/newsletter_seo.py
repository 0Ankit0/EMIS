"""Newsletter & SEO API Views"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from ..models import Newsletter, SEO
from ..serializers import NewsletterSerializer, SEOSerializer


class NewsletterViewSet(viewsets.ModelViewSet):
    """ViewSet for Newsletter"""
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['post'])
    def subscribe(self, request):
        """Public endpoint for newsletter subscription"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(is_active=True)
            return Response(
                {'message': 'Successfully subscribed to newsletter'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SEOViewSet(viewsets.ModelViewSet):
    """ViewSet for SEO"""
    queryset = SEO.objects.all()
    serializer_class = SEOSerializer
    permission_classes = [IsAuthenticated]
