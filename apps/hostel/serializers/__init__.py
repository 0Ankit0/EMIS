"""Hostel Serializers"""
from rest_framework import serializers
from .models import (
    Hostel, Floor, Room, RoomAllocation, HostelFee, MessMenu,
    VisitorLog, Complaint, OutingRequest, Attendance
)


class HostelSerializer(serializers.ModelSerializer):
    """Serializer for Hostel"""
    warden_name = serializers.CharField(source='warden.get_full_name', read_only=True)
    available_capacity = serializers.IntegerField(read_only=True)
    occupancy_percentage = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    
    class Meta:
        model = Hostel
        fields = '__all__'
        read_only_fields = ['id', 'occupied_capacity', 'created_at', 'updated_at']


class FloorSerializer(serializers.ModelSerializer):
    """Serializer for Floor"""
    hostel_name = serializers.CharField(source='hostel.name', read_only=True)
    
    class Meta:
        model = Floor
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class RoomSerializer(serializers.ModelSerializer):
    """Serializer for Room"""
    hostel_name = serializers.CharField(source='hostel.name', read_only=True)
    floor_number = serializers.IntegerField(source='floor.floor_number', read_only=True)
    available_beds = serializers.IntegerField(read_only=True)
    is_available = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Room
        fields = '__all__'
        read_only_fields = ['id', 'occupied_beds', 'created_at', 'updated_at']


class RoomAllocationSerializer(serializers.ModelSerializer):
    """Serializer for RoomAllocation"""
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    student_email = serializers.CharField(source='student.user.email', read_only=True)
    room_number = serializers.CharField(source='room.room_number', read_only=True)
    hostel_name = serializers.CharField(source='room.hostel.name', read_only=True)
    allocated_by_name = serializers.CharField(source='allocated_by.get_full_name', read_only=True)
    
    class Meta:
        model = RoomAllocation
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class HostelFeeSerializer(serializers.ModelSerializer):
    """Serializer for HostelFee"""
    hostel_name = serializers.CharField(source='hostel.name', read_only=True)
    
    class Meta:
        model = HostelFee
        fields = '__all__'
        read_only_fields = ['id', 'total_fee', 'created_at', 'updated_at']


class MessMenuSerializer(serializers.ModelSerializer):
    """Serializer for MessMenu"""
    hostel_name = serializers.CharField(source='hostel.name', read_only=True)
    
    class Meta:
        model = MessMenu
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class VisitorLogSerializer(serializers.ModelSerializer):
    """Serializer for VisitorLog"""
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    hostel_name = serializers.CharField(source='hostel.name', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True)
    
    class Meta:
        model = VisitorLog
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class ComplaintSerializer(serializers.ModelSerializer):
    """Serializer for Complaint"""
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    hostel_name = serializers.CharField(source='hostel.name', read_only=True)
    room_number = serializers.CharField(source='room.room_number', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    
    class Meta:
        model = Complaint
        fields = '__all__'
        read_only_fields = ['id', 'complaint_number', 'created_at', 'updated_at']


class OutingRequestSerializer(serializers.ModelSerializer):
    """Serializer for OutingRequest"""
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    hostel_name = serializers.CharField(source='hostel.name', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True)
    
    class Meta:
        model = OutingRequest
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, data):
        """Validate outing request dates"""
        if data.get('out_date') and data.get('expected_return_date'):
            if data['out_date'] > data['expected_return_date']:
                raise serializers.ValidationError("Return date must be after out date")
        return data


class AttendanceSerializer(serializers.ModelSerializer):
    """Serializer for Attendance"""
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    hostel_name = serializers.CharField(source='hostel.name', read_only=True)
    marked_by_name = serializers.CharField(source='marked_by.get_full_name', read_only=True)
    
    class Meta:
        model = Attendance
        fields = '__all__'
        read_only_fields = ['id', 'marked_at', 'created_at', 'updated_at']
