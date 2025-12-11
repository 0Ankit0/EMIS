"""
Transport Serializers
"""
from rest_framework import serializers
from ..models import Driver, Vehicle, Route, RouteStop, StudentTransportAssignment, VehicleMaintenance, FuelLog, RouteTracking


class DriverSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = Driver
        fields = '__all__'


class VehicleSerializer(serializers.ModelSerializer):
    driver_name = serializers.CharField(source='assigned_driver.user.get_full_name', read_only=True)
    
    class Meta:
        model = Vehicle
        fields = '__all__'


class RouteSerializer(serializers.ModelSerializer):
    vehicle_number = serializers.CharField(source='assigned_vehicle.registration_number', read_only=True)
    driver_name = serializers.CharField(source='assigned_driver.user.get_full_name', read_only=True)
    
    class Meta:
        model = Route
        fields = '__all__'


class RouteStopSerializer(serializers.ModelSerializer):
    route_name = serializers.CharField(source='route.route_name', read_only=True)
    
    class Meta:
        model = RouteStop
        fields = '__all__'


class StudentTransportAssignmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    route_name = serializers.CharField(source='route.route_name', read_only=True)
    
    class Meta:
        model = StudentTransportAssignment
        fields = '__all__'


class VehicleMaintenanceSerializer(serializers.ModelSerializer):
    vehicle_number = serializers.CharField(source='vehicle.registration_number', read_only=True)
    
    class Meta:
        model = VehicleMaintenance
        fields = '__all__'


class FuelLogSerializer(serializers.ModelSerializer):
    vehicle_number = serializers.CharField(source='vehicle.registration_number', read_only=True)
    driver_name = serializers.CharField(source='driver.user.get_full_name', read_only=True)
    
    class Meta:
        model = FuelLog
        fields = '__all__'


class RouteTrackingSerializer(serializers.ModelSerializer):
    route_name = serializers.CharField(source='route.route_name', read_only=True)
    vehicle_number = serializers.CharField(source='vehicle.registration_number', read_only=True)
    driver_name = serializers.CharField(source='driver.user.get_full_name', read_only=True)
    
    class Meta:
        model = RouteTracking
        fields = '__all__'
        fields = [
            'id', 'name', 'description', 'status',
            'created_by', 'created_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_name(self, value):
        """Validate name field"""
        if len(value) < 3:
            raise serializers.ValidationError("Name must be at least 3 characters long")
        return value


class TransportItemListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing transport items
    """
    class Meta:
        model = TransportItem
        fields = ['id', 'name', 'status', 'created_at']
