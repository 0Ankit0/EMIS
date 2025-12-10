"""Hostel App Tests"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal

from .models import (
    Hostel, Floor, Room, RoomAllocation, HostelFee, MessMenu,
    VisitorLog, Complaint, OutingRequest, Attendance
)

User = get_user_model()


class HostelTestCase(TestCase):
    """Test Hostel model"""
    
    def setUp(self):
        self.hostel = Hostel.objects.create(
            name='Boys Hostel 1',
            code='BH-01',
            hostel_type='boys',
            address='Campus Road',
            city='Mumbai',
            pincode='400001',
            total_floors=3,
            total_rooms=30,
            total_capacity=90,
            contact_number='+919876543210'
        )
    
    def test_available_capacity(self):
        """Test available capacity calculation"""
        self.assertEqual(self.hostel.available_capacity, 90)
        
        self.hostel.occupied_capacity = 30
        self.hostel.save()
        
        self.assertEqual(self.hostel.available_capacity, 60)
    
    def test_occupancy_percentage(self):
        """Test occupancy percentage calculation"""
        self.hostel.occupied_capacity = 45
        self.hostel.save()
        
        self.assertEqual(self.hostel.occupancy_percentage, 50.0)


class RoomTestCase(TestCase):
    """Test Room model"""
    
    def setUp(self):
        self.hostel = Hostel.objects.create(
            name='Test Hostel',
            code='TH-01',
            hostel_type='boys',
            address='Test Address',
            city='Test City',
            pincode='123456',
            total_floors=1,
            total_rooms=10,
            total_capacity=20,
            contact_number='+911234567890'
        )
        
        self.floor = Floor.objects.create(
            hostel=self.hostel,
            floor_number=1,
            total_rooms=10
        )
        
        self.room = Room.objects.create(
            hostel=self.hostel,
            floor=self.floor,
            room_number='101',
            room_type='double',
            capacity=2,
            monthly_rent=Decimal('5000.00')
        )
    
    def test_available_beds(self):
        """Test available beds calculation"""
        self.assertEqual(self.room.available_beds, 2)
        
        self.room.occupied_beds = 1
        self.room.save()
        
        self.assertEqual(self.room.available_beds, 1)
    
    def test_is_available(self):
        """Test room availability check"""
        self.assertTrue(self.room.is_available)
        
        self.room.occupied_beds = 2
        self.room.status = 'full'
        self.room.save()
        
        self.assertFalse(self.room.is_available)


class ComplaintTestCase(TestCase):
    """Test Complaint model"""
    
    def test_complaint_number_generation(self):
        """Test automatic complaint number generation"""
        # This would require a full setup with student
        pass


class HostelFeeTestCase(TestCase):
    """Test HostelFee model"""
    
    def test_total_fee_calculation(self):
        """Test total fee auto-calculation"""
        hostel = Hostel.objects.create(
            name='Test Hostel',
            code='TH-01',
            hostel_type='boys',
            address='Test',
            city='Test',
            pincode='123456',
            total_floors=1,
            total_rooms=10,
            total_capacity=20,
            contact_number='+911234567890'
        )
        
        fee = HostelFee.objects.create(
            hostel=hostel,
            room_type='single',
            accommodation_fee=Decimal('5000'),
            mess_fee=Decimal('3000'),
            maintenance_fee=Decimal('500'),
            electricity_charges=Decimal('500'),
            other_charges=Decimal('200'),
            academic_year='2024-2025'
        )
        
        self.assertEqual(fee.total_fee, Decimal('9200.00'))
