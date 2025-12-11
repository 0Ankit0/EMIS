"""Event Serializers"""
from rest_framework import serializers
from ..models import Event
from .reminder import EventReminderSerializer


class EventSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    color_code = serializers.SerializerMethodField()
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    reminders = EventReminderSerializer(many=True, read_only=True)
    calendar_names = serializers.SerializerMethodField()
    
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['created_by']
    
    def get_color_code(self, obj):
        return obj.get_color()
    
    def get_calendar_names(self, obj):
        return [cal.name for cal in obj.calendars.all()]


class EventListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for event listings"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    color_code = serializers.SerializerMethodField()
    
    class Meta:
        model = Event
        fields = ['id', 'title', 'start_datetime', 'end_datetime', 'is_all_day', 
                  'category', 'category_name', 'color_code', 'location', 'priority']
    
    def get_color_code(self, obj):
        return obj.get_color()
