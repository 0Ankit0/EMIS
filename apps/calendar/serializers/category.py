"""Event Category Serializer"""
from rest_framework import serializers
from ..models import EventCategory


class EventCategorySerializer(serializers.ModelSerializer):
    event_count = serializers.SerializerMethodField()
    
    class Meta:
        model = EventCategory
        fields = '__all__'
    
    def get_event_count(self, obj):
        return obj.events.count()
