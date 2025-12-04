from rest_framework import serializers
from ..models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ('id','registration_number','updated_at','created_at','is_active')

    def delete(self,instance):
        instance.is_active = False
        instance.save()