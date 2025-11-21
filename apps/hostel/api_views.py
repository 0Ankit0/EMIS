"""Hostel API Views"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count, Q, Avg
from django.utils import timezone

from .models import (
    Hostel, Floor, Room, RoomAllocation, HostelFee, MessMenu,
    VisitorLog, Complaint, OutingRequest, Attendance
)
from .serializers import (
    HostelSerializer, FloorSerializer, RoomSerializer, RoomAllocationSerializer,
    HostelFeeSerializer, MessMenuSerializer, VisitorLogSerializer,
    ComplaintSerializer, OutingRequestSerializer, AttendanceSerializer
)


class HostelViewSet(viewsets.ModelViewSet):
    """ViewSet for Hostel"""
    queryset = Hostel.objects.all()
    serializer_class = HostelSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['hostel_type', 'status', 'is_active']
    search_fields = ['name', 'code', 'city']
    ordering_fields = ['name', 'total_capacity', 'occupied_capacity']
    ordering = ['name']
    
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Get hostel statistics"""
        hostel = self.get_object()
        stats = {
            'total_capacity': hostel.total_capacity,
            'occupied': hostel.occupied_capacity,
            'available': hostel.available_capacity,
            'occupancy_rate': hostel.occupancy_percentage,
            'total_rooms': hostel.rooms.count(),
            'available_rooms': hostel.rooms.filter(status='available').count(),
            'floors': hostel.floors.count(),
            'active_allocations': hostel.rooms.filter(
                allocations__status='active'
            ).distinct().count(),
        }
        return Response(stats)
    
    @action(detail=True, methods=['get'])
    def available_rooms(self, request, pk=None):
        """Get available rooms in hostel"""
        hostel = self.get_object()
        rooms = hostel.rooms.with_vacancy()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)


class FloorViewSet(viewsets.ModelViewSet):
    """ViewSet for Floor"""
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['hostel']
    ordering = ['hostel', 'floor_number']


class RoomViewSet(viewsets.ModelViewSet):
    """ViewSet for Room"""
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['hostel', 'floor', 'room_type', 'status', 'has_ac']
    search_fields = ['room_number']
    ordering_fields = ['room_number', 'monthly_rent']
    ordering = ['hostel', 'room_number']
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get all available rooms"""
        rooms = Room.objects.available()
        serializer = self.get_serializer(rooms, many=True)
        return Response(serializer.data)


class RoomAllocationViewSet(viewsets.ModelViewSet):
    """ViewSet for RoomAllocation"""
    queryset = RoomAllocation.objects.all()
    serializer_class = RoomAllocationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['student', 'room', 'status', 'academic_year']
    ordering = ['-allocation_date']
    
    def perform_create(self, serializer):
        """Update room occupancy when allocating"""
        allocation = serializer.save(allocated_by=self.request.user)
        room = allocation.room
        room.occupied_beds += 1
        if room.occupied_beds >= room.capacity:
            room.status = 'full'
        else:
            room.status = 'occupied'
        room.save()
        
        # Update hostel occupancy
        hostel = room.hostel
        hostel.occupied_capacity += 1
        hostel.save()
    
    @action(detail=True, methods=['post'])
    def vacate(self, request, pk=None):
        """Vacate a room allocation"""
        allocation = self.get_object()
        
        if allocation.status != 'active':
            return Response(
                {'error': 'Only active allocations can be vacated'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        allocation.status = 'vacated'
        allocation.vacate_date = timezone.now().date()
        allocation.save()
        
        # Update room occupancy
        room = allocation.room
        room.occupied_beds = max(0, room.occupied_beds - 1)
        if room.occupied_beds < room.capacity:
            room.status = 'available'
        room.save()
        
        # Update hostel occupancy
        hostel = room.hostel
        hostel.occupied_capacity = max(0, hostel.occupied_capacity - 1)
        hostel.save()
        
        return Response({'message': 'Room vacated successfully'})


class HostelFeeViewSet(viewsets.ModelViewSet):
    """ViewSet for HostelFee"""
    queryset = HostelFee.objects.all()
    serializer_class = HostelFeeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['hostel', 'room_type', 'academic_year', 'is_active']
    ordering = ['-created_at']


class MessMenuViewSet(viewsets.ModelViewSet):
    """ViewSet for MessMenu"""
    queryset = MessMenu.objects.all()
    serializer_class = MessMenuSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['hostel', 'day_of_week', 'meal_type', 'is_active']
    ordering = ['hostel', 'day_of_week', 'meal_type']
    
    @action(detail=False, methods=['get'])
    def weekly_menu(self, request):
        """Get weekly menu for a hostel"""
        hostel_id = request.query_params.get('hostel')
        if not hostel_id:
            return Response(
                {'error': 'hostel parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        menus = MessMenu.objects.filter(hostel_id=hostel_id, is_active=True)
        serializer = self.get_serializer(menus, many=True)
        return Response(serializer.data)


class VisitorLogViewSet(viewsets.ModelViewSet):
    """ViewSet for VisitorLog"""
    queryset = VisitorLog.objects.all()
    serializer_class = VisitorLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['hostel', 'student', 'purpose']
    search_fields = ['visitor_name', 'visitor_phone']
    ordering = ['-entry_time']
    
    @action(detail=True, methods=['post'])
    def mark_exit(self, request, pk=None):
        """Mark visitor exit time"""
        visitor = self.get_object()
        
        if visitor.exit_time:
            return Response(
                {'error': 'Exit already marked'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        visitor.exit_time = timezone.now()
        visitor.save()
        
        return Response({'message': 'Exit time marked successfully'})


class ComplaintViewSet(viewsets.ModelViewSet):
    """ViewSet for Complaint"""
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['hostel', 'student', 'category', 'priority', 'status']
    search_fields = ['complaint_number', 'title', 'description']
    ordering = ['-submitted_date']
    
    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        """Acknowledge a complaint"""
        complaint = self.get_object()
        
        if complaint.status != 'submitted':
            return Response(
                {'error': 'Only submitted complaints can be acknowledged'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        complaint.status = 'acknowledged'
        complaint.acknowledged_date = timezone.now()
        complaint.save()
        
        return Response({'message': 'Complaint acknowledged'})
    
    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """Resolve a complaint"""
        complaint = self.get_object()
        resolution = request.data.get('resolution')
        
        if not resolution:
            return Response(
                {'error': 'Resolution is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        complaint.status = 'resolved'
        complaint.resolved_date = timezone.now()
        complaint.resolution = resolution
        complaint.save()
        
        return Response({'message': 'Complaint resolved successfully'})


class OutingRequestViewSet(viewsets.ModelViewSet):
    """ViewSet for OutingRequest"""
    queryset = OutingRequest.objects.all()
    serializer_class = OutingRequestSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['student', 'hostel', 'status']
    ordering = ['-created_at']
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve outing request"""
        outing = self.get_object()
        
        if outing.status != 'pending':
            return Response(
                {'error': 'Only pending requests can be approved'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        outing.status = 'approved'
        outing.approved_by = request.user
        outing.approval_date = timezone.now()
        outing.save()
        
        return Response({'message': 'Outing request approved'})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject outing request"""
        outing = self.get_object()
        reason = request.data.get('reason', '')
        
        if outing.status != 'pending':
            return Response(
                {'error': 'Only pending requests can be rejected'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        outing.status = 'rejected'
        outing.rejection_reason = reason
        outing.save()
        
        return Response({'message': 'Outing request rejected'})
    
    @action(detail=True, methods=['post'])
    def mark_returned(self, request, pk=None):
        """Mark student as returned"""
        outing = self.get_object()
        
        if outing.status != 'approved':
            return Response(
                {'error': 'Only approved outings can be marked as returned'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        outing.status = 'returned'
        outing.actual_return_date = timezone.now().date()
        outing.actual_return_time = timezone.now().time()
        outing.save()
        
        return Response({'message': 'Student marked as returned'})


class AttendanceViewSet(viewsets.ModelViewSet):
    """ViewSet for Attendance"""
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['hostel', 'student', 'date', 'status']
    ordering = ['-date']
    
    def perform_create(self, serializer):
        """Set marked_by when creating attendance"""
        serializer.save(marked_by=self.request.user)
    
    @action(detail=False, methods=['post'])
    def bulk_mark(self, request):
        """Mark attendance for multiple students"""
        student_ids = request.data.get('student_ids', [])
        date = request.data.get('date')
        status_value = request.data.get('status')
        hostel_id = request.data.get('hostel')
        
        if not all([student_ids, date, status_value, hostel_id]):
            return Response(
                {'error': 'student_ids, date, status, and hostel are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from apps.students.models import Student
        
        count = 0
        for student_id in student_ids:
            try:
                student = Student.objects.get(id=student_id)
                Attendance.objects.update_or_create(
                    student=student,
                    date=date,
                    defaults={
                        'hostel_id': hostel_id,
                        'status': status_value,
                        'marked_by': request.user
                    }
                )
                count += 1
            except Student.DoesNotExist:
                continue
        
        return Response({
            'message': f'Attendance marked for {count} students',
            'count': count
        })
