"""Transport Serializers"""
from rest_framework import serializers
from .models import Driver, Vehicle, Route, RouteStop, StudentTransportAssignment, VehicleMaintenance, FuelLog


class DriverSerializer(serializers.ModelSerializer):
    """Serializer for Driver"""
    class Meta:
        model = Driver
        fields = '__all__'


class VehicleSerializer(serializers.ModelSerializer):
    """Serializer for Vehicle"""
    class Meta:
        model = Vehicle
        fields = '__all__'


class RouteSerializer(serializers.ModelSerializer):
    """Serializer for Route"""
    class Meta:
        model = Route
        fields = '__all__'


class RouteStopSerializer(serializers.ModelSerializer):
    """Serializer for RouteStop"""
    class Meta:
        model = RouteStop
        fields = '__all__'


class StudentTransportAssignmentSerializer(serializers.ModelSerializer):
    """Serializer for StudentTransportAssignment"""
    class Meta:
        model = StudentTransportAssignment
        fields = '__all__'


class VehicleMaintenanceSerializer(serializers.ModelSerializer):
    """Serializer for VehicleMaintenance"""
    class Meta:
        model = VehicleMaintenance
        fields = '__all__'


class FuelLogSerializer(serializers.ModelSerializer):
    """Serializer for FuelLog"""
    class Meta:
        model = FuelLog
        fields = '__all__'
