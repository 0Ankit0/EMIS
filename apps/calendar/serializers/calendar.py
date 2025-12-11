"""Calendar Serializer"""
from rest_framework import serializers
from ..models import Calendar


class CalendarSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.get_full_name', read_only=True)
    event_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Calendar
        fields = '__all__'
        read_only_fields = ['owner']
    
    def get_event_count(self, obj):
        return obj.events.count()
