from rest_framework import viewsets
from ..models.category import Category
from ..serializers.category import (
    CategoryCreateSerializer,
    CategoryUpdateSerializer,
    CategoryResponseSerializer
)
from rest_framework.permissions import IsAuthenticated

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'ukid'
    
    def get_serializer_class(self): # type: ignore
        if self.action == 'create':
            return CategoryCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return CategoryUpdateSerializer
        return CategoryResponseSerializer
