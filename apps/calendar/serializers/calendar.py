from rest_framework import serializers
from ..models.calendar import Calendar

class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = '__all__'
        exclude = ['id']
        lookup_field = 'ukid'
