from rest_framework import serializers
from django.utils import timezone
from ..models.event import Event, EventType, EventStatus
from ..models.category import Category
from ..models.calendar import Calendar
from .calendar import CalendarResponseSerializer
from .category import CategoryResponseSerializer

class EventCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='ukid', queryset=Category.objects.all())
    calendar = serializers.SlugRelatedField(slug_field='ukid', queryset=Calendar.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Event
        fields = [
            'category', 'calendar', 'title', 'description', 'organizer', 
            'location', 'type', 'start_date', 'end_date', 'start_time', 
            'end_time', 'event_duration', 'entry_form_required', 
            'registration_url', 'registration_limit', 'reminder_enabled', 
            'remainder_time_before_event'
        ]
    
    def validate(self, attrs):
        errors = {}
        
        # Validate time
        if attrs.get('start_time') and attrs.get('end_time'):
            if attrs['end_time'] <= attrs['start_time']:
                errors['end_time'] = 'End time must be after start time.'
        
        # Validate dates based on event type
        event_type = attrs.get('type', EventType.SINGLE_DAY)
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')
        
        if event_type == EventType.MULTI_DAY:
            if not start_date or not end_date:
                if not start_date:
                    errors['start_date'] = 'Start date is required for multi-day events.'
                if not end_date:
                    errors['end_date'] = 'End date is required for multi-day events.'
            elif start_date >= end_date:
                errors['end_date'] = 'End date must be after start date for multi-day events.'
        elif event_type == EventType.SINGLE_DAY:
            if not start_date or not end_date:
                if not start_date:
                    errors['start_date'] = 'Start date is required for single day events.'
                if not end_date:
                    errors['end_date'] = 'End date is required for single day events.'
            elif start_date != end_date:
                errors['end_date'] = 'Start date and end date must be the same for single day events.'
        
        # Validate registration
        if attrs.get('entry_form_required') and not attrs.get('registration_url'):
            errors['registration_url'] = 'Registration URL is required when entry form is required.'
        
        if errors:
            raise serializers.ValidationError(errors)
        
        return attrs

class EventUpdateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='ukid', queryset=Category.objects.all(), required=False)
    calendar = serializers.SlugRelatedField(slug_field='ukid', queryset=Calendar.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Event
        fields = [
            'category', 'calendar', 'title', 'description', 'organizer', 
            'location', 'type', 'start_date', 'end_date', 'start_time', 
            'end_time', 'event_duration', 'entry_form_required', 
            'registration_url', 'registration_limit', 'reminder_enabled', 
            'remainder_time_before_event', 'status', 'postponed_to', 'updated_by'
        ]
        extra_kwargs = {field: {'required': False} for field in fields}
    
    def validate(self, attrs):
        instance = self.instance
        errors = {}
        
        # Get values from attrs or instance
        start_time = attrs.get('start_time', instance.start_time if instance else None)
        end_time = attrs.get('end_time', instance.end_time if instance else None)
        
        if start_time and end_time and end_time <= start_time:
            errors['end_time'] = 'End time must be after start time.'
        
        # Validate dates based on event type
        event_type = attrs.get('type', instance.type if instance else EventType.SINGLE_DAY)
        start_date = attrs.get('start_date', instance.start_date if instance else None)
        end_date = attrs.get('end_date', instance.end_date if instance else None)
        
        if event_type == EventType.MULTI_DAY:
            if start_date and end_date and start_date >= end_date:
                errors['end_date'] = 'End date must be after start date for multi-day events.'
        elif event_type == EventType.SINGLE_DAY:
            if start_date and end_date and start_date != end_date:
                errors['end_date'] = 'Start date and end date must be the same for single day events.'
        
        if errors:
            raise serializers.ValidationError(errors)
        
        return attrs
    
    def update(self, instance, validated_data):
        old_status = instance.status
        new_status = validated_data.get('status', old_status)
        
        # Handle status transitions
        if old_status != new_status:
            if new_status == EventStatus.PUBLISHED:
                validated_data['published_at'] = timezone.now()
                request = self.context.get('request')
                if request and hasattr(request, 'user') and request.user.is_authenticated:
                    validated_data['published_by'] = request.user.id
            elif new_status == EventStatus.CANCELLED:
                validated_data['cancelled_at'] = timezone.now()
                request = self.context.get('request')
                if request and hasattr(request, 'user') and request.user.is_authenticated:
                    validated_data['cancelled_by'] = request.user.id
        
        return super().update(instance, validated_data)

class EventResponseSerializer(serializers.ModelSerializer):
    category = CategoryResponseSerializer(read_only=True)
    calendar = CalendarResponseSerializer(read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Event
        fields = [
            'ukid', 'category', 'calendar', 'title', 'description', 'organizer', 
            'location', 'slug', 'type', 'type_display', 'start_date', 'end_date', 
            'start_time', 'end_time', 'event_duration', 'entry_form_required', 
            'registration_url', 'registration_limit', 'reminder_enabled', 
            'remainder_time_before_event', 'status', 'status_display', 'published_at', 
            'published_by', 'postponed_to', 'cancelled_at', 'cancelled_by', 
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'ukid', 'slug', 'published_at', 'published_by', 'cancelled_at', 
            'cancelled_by', 'created_at', 'updated_at'
        ]