"""Transport API Views"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Vehicle, Route, RouteStop, Driver, StudentTransportAssignment, VehicleMaintenance, FuelLog
from .serializers import (
    VehicleSerializer, RouteSerializer, RouteStopSerializer,
    DriverSerializer, StudentTransportAssignmentSerializer,
    VehicleMaintenanceSerializer, FuelLogSerializer
)


class VehicleViewSet(viewsets.ModelViewSet):
    """ViewSet for Vehicles"""
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['vehicle_type', 'status']
    search_fields = ['vehicle_number', 'make', 'model']
    ordering = ['vehicle_number']


class RouteViewSet(viewsets.ModelViewSet):
    """ViewSet for Routes"""
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['route_name', 'route_number']
    
    @action(detail=True, methods=['get'])
    def stops(self, request, pk=None):
        """Get stops for this route"""
        route = self.get_object()
        stops = RouteStop.objects.filter(route=route).order_by('stop_order')
        serializer = RouteStopSerializer(stops, many=True)
        return Response(serializer.data)


class RouteStopViewSet(viewsets.ModelViewSet):
    """ViewSet for Route Stops"""
    queryset = RouteStop.objects.all()
    serializer_class = RouteStopSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['route']
    ordering = ['route', 'stop_order']


class DriverViewSet(viewsets.ModelViewSet):
    """ViewSet for Drivers"""
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['first_name', 'last_name', 'license_number', 'phone']


class StudentTransportAssignmentViewSet(viewsets.ModelViewSet):
    """ViewSet for Student Transport Assignments"""
    queryset = StudentTransportAssignment.objects.all()
    serializer_class = StudentTransportAssignmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['student', 'route', 'is_active']
    search_fields = ['student__user__first_name', 'student__user__last_name']


class VehicleMaintenanceViewSet(viewsets.ModelViewSet):
    """ViewSet for Vehicle Maintenance"""
    queryset = VehicleMaintenance.objects.all()
    serializer_class = VehicleMaintenanceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['vehicle', 'maintenance_type', 'status']
    ordering = ['-maintenance_date']


class FuelLogViewSet(viewsets.ModelViewSet):
    """ViewSet for Fuel Logs"""
    queryset = FuelLog.objects.all()
    serializer_class = FuelLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['vehicle']
    ordering = ['-date']
