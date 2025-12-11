"""Slider & Widget API Views"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..models import Slider, Widget
from ..serializers import SliderSerializer, WidgetSerializer


class SliderViewSet(viewsets.ModelViewSet):
    """ViewSet for Slider"""
    queryset = Slider.objects.filter(is_active=True).order_by('order')
    serializer_class = SliderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class WidgetViewSet(viewsets.ModelViewSet):
    """ViewSet for Widget"""
    serializer_class = WidgetSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = Widget.objects.filter(is_active=True).order_by('order')
        location = self.request.query_params.get('location')
        if location:
            queryset = queryset.filter(location=location)
        return queryset
