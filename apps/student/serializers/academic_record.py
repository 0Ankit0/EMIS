from rest_framework import serializers
from ..models import AcademicRecord

class AcademicRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicRecord
        fields = '__all__'
        exclude = ['id']
        lookup_field = 'ukid'