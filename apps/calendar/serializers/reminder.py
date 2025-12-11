"""Event Reminder Serializer"""
from rest_framework import serializers
from ..models import EventReminder


class EventReminderSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    reminder_datetime = serializers.SerializerMethodField()
    
    class Meta:
        model = EventReminder
        fields = '__all__'
    
    def get_reminder_datetime(self, obj):
        return obj.get_reminder_datetime()
