from rest_framework import serializers
from .models import Event, Category, Calendar

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

        def validate_color(self, value): # syntax is validate_<field_name>
            """Validate the color field to ensure it is a valid hex code.
            """
            if not value.startswith('#'):
                raise serializers.ValidationError("Color must be a valid hex code.")
            if len(value) not in (4, 7):
                raise serializers.ValidationError("Color must be a valid hex code of length 4 or 7.")
            return value
        read_only_fields = ('created_at', 'updated_at')

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = '__all__'