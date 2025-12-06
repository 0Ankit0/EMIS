from rest_framework import serializers
from ..models.calendar import Calendar

class CalendarCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = ['title', 'start_date', 'end_date']
    
    def validate(self, attrs):
        if attrs.get('end_date') and attrs.get('start_date'):
            if attrs['end_date'] < attrs['start_date']:
                raise serializers.ValidationError({
                    'end_date': 'End date must be after start date.'
                })
        return attrs
    
class CalendarUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = ['title', 'start_date', 'end_date', 'updated_by']
        extra_kwargs = {
            'title': {'required': False},
            'start_date': {'required': False},
            'end_date': {'required': False},
        }
    
    def validate(self, attrs):
        instance = self.instance
        start_date = attrs.get('start_date', instance.start_date if instance else None)
        end_date = attrs.get('end_date', instance.end_date if instance else None)
        
        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError({
                'end_date': 'End date must be after start date.'
            })
        return attrs

class CalendarResponseSerializer(serializers.ModelSerializer):
    event_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Calendar
        fields = ['ukid', 'title', 'start_date', 'end_date', 'event_count', 'created_at', 'updated_at']
        read_only_fields = ['ukid', 'created_at', 'updated_at']
    
    def get_event_count(self, obj):
        return obj.events.count()
