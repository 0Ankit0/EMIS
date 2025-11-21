"""Hostel Models - Comprehensive Hostel Management System"""
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from apps.core.models import TimeStampedModel
from .managers import HostelManager, RoomManager, RoomAllocationManager, ComplaintManager, OutingRequestManager
from decimal import Decimal

User = get_user_model()


class Hostel(TimeStampedModel):
    """Hostel/Dormitory Building"""
    
    HOSTEL_TYPE_CHOICES = [
        ('boys', "Boys' Hostel"),
        ('girls', "Girls' Hostel"),
        ('mixed', 'Co-ed Hostel'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('maintenance', 'Under Maintenance'),
        ('closed', 'Closed'),
    ]
    
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True, db_index=True)
    hostel_type = models.CharField(max_length=20, choices=HOSTEL_TYPE_CHOICES)
    
    address = models.TextField()
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    
    total_floors = models.IntegerField(validators=[MinValueValidator(1)])
    total_rooms = models.IntegerField(validators=[MinValueValidator(1)])
    total_capacity = models.IntegerField(validators=[MinValueValidator(1)])
    occupied_capacity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    warden = models.ForeignKey(
        'faculty.Faculty',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_hostels'
    )
    
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    
    amenities = models.JSONField(
        default=list,
        help_text="List of amenities: ['WiFi', 'Laundry', 'Gym', etc.]"
    )
    
    facilities = models.TextField(blank=True, help_text="Description of facilities")
    rules_and_regulations = models.TextField(blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', db_index=True)
    is_active = models.BooleanField(default=True)
    
    established_date = models.DateField(null=True, blank=True)
    
    class Meta:
        db_table = 'hostels'
        ordering = ['name']
        verbose_name = 'Hostel'
        verbose_name_plural = 'Hostels'
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['hostel_type', 'status']),
        ]
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    @property
    def available_capacity(self):
        return self.total_capacity - self.occupied_capacity
    
    @property
    def occupancy_percentage(self):
        if self.total_capacity > 0:
            return (self.occupied_capacity / self.total_capacity) * 100
        return 0


class Floor(TimeStampedModel):
    """Floor in a Hostel"""
    
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='floors')
    floor_number = models.IntegerField(validators=[MinValueValidator(0)])
    
    total_rooms = models.IntegerField(validators=[MinValueValidator(1)])
    description = models.TextField(blank=True)
    
    class Meta:
        db_table = 'hostel_floors'
        unique_together = ['hostel', 'floor_number']
        ordering = ['hostel', 'floor_number']
        verbose_name = 'Floor'
        verbose_name_plural = 'Floors'
    
    def __str__(self):
        return f"{self.hostel.name} - Floor {self.floor_number}"


class Room(TimeStampedModel):
    """Room in a Hostel"""
    
    ROOM_TYPE_CHOICES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('triple', 'Triple'),
        ('quad', 'Quad'),
        ('dormitory', 'Dormitory'),
    ]
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('full', 'Full'),
        ('maintenance', 'Under Maintenance'),
        ('reserved', 'Reserved'),
    ]
    
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='rooms')
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name='rooms')
    
    room_number = models.CharField(max_length=20, db_index=True)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
    
    capacity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    occupied_beds = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    area_sqft = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    
    has_attached_bathroom = models.BooleanField(default=True)
    has_balcony = models.BooleanField(default=False)
    has_ac = models.BooleanField(default=False)
    
    furniture = models.JSONField(
        default=list,
        help_text="List of furniture: ['Bed', 'Study Table', 'Chair', 'Wardrobe']"
    )
    
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', db_index=True)
    
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'hostel_rooms'
        unique_together = ['hostel', 'room_number']
        ordering = ['hostel', 'floor', 'room_number']
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'
        indexes = [
            models.Index(fields=['hostel', 'status']),
            models.Index(fields=['room_number']),
        ]
    
    def __str__(self):
        return f"{self.hostel.code} - Room {self.room_number}"
    
    @property
    def available_beds(self):
        return self.capacity - self.occupied_beds
    
    @property
    def is_available(self):
        return self.status == 'available' and self.available_beds > 0


class RoomAllocation(TimeStampedModel):
    """Student Room Allocation"""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('vacated', 'Vacated'),
        ('transferred', 'Transferred'),
        ('terminated', 'Terminated'),
    ]
    
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='room_allocations')
    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name='allocations')
    bed_number = models.CharField(max_length=10, blank=True)
    
    allocation_date = models.DateField(default=timezone.now)
    vacate_date = models.DateField(null=True, blank=True)
    
    academic_year = models.CharField(max_length=20)
    semester = models.CharField(max_length=50, blank=True)
    
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', db_index=True)
    
    allocated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='allocated_rooms')
    
    remarks = models.TextField(blank=True)
    
    class Meta:
        db_table = 'hostel_room_allocations'
        ordering = ['-allocation_date']
        verbose_name = 'Room Allocation'
        verbose_name_plural = 'Room Allocations'
        indexes = [
            models.Index(fields=['student', 'status']),
            models.Index(fields=['room', 'status']),
            models.Index(fields=['allocation_date']),
        ]
    
    def __str__(self):
        return f"{self.student.user.email} - {self.room.room_number}"


class HostelFee(TimeStampedModel):
    """Hostel Fee Structure"""
    
    FEE_TYPE_CHOICES = [
        ('monthly', 'Monthly'),
        ('semester', 'Semester'),
        ('annual', 'Annual'),
    ]
    
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='fee_structures')
    room_type = models.CharField(max_length=20, choices=Room.ROOM_TYPE_CHOICES)
    
    fee_type = models.CharField(max_length=20, choices=FEE_TYPE_CHOICES, default='monthly')
    
    accommodation_fee = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    mess_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    maintenance_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    electricity_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    other_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    total_fee = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    academic_year = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    
    description = models.TextField(blank=True)
    
    class Meta:
        db_table = 'hostel_fees'
        ordering = ['-created_at']
        verbose_name = 'Hostel Fee'
        verbose_name_plural = 'Hostel Fees'
    
    def __str__(self):
        return f"{self.hostel.name} - {self.room_type} ({self.academic_year})"
    
    def save(self, *args, **kwargs):
        self.total_fee = (
            self.accommodation_fee + self.mess_fee + self.maintenance_fee +
            self.electricity_charges + self.other_charges
        )
        super().save(*args, **kwargs)


class MessMenu(TimeStampedModel):
    """Mess Menu"""
    
    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('snacks', 'Snacks'),
        ('dinner', 'Dinner'),
    ]
    
    DAY_CHOICES = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]
    
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='mess_menus')
    
    day_of_week = models.CharField(max_length=20, choices=DAY_CHOICES)
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPE_CHOICES)
    
    menu_items = models.JSONField(
        default=list,
        help_text="List of menu items"
    )
    
    timing = models.CharField(max_length=50, help_text="e.g., '7:00 AM - 9:00 AM'")
    
    is_active = models.BooleanField(default=True)
    effective_from = models.DateField(default=timezone.now)
    
    class Meta:
        db_table = 'hostel_mess_menus'
        unique_together = ['hostel', 'day_of_week', 'meal_type']
        ordering = ['hostel', 'day_of_week', 'meal_type']
        verbose_name = 'Mess Menu'
        verbose_name_plural = 'Mess Menus'
    
    def __str__(self):
        return f"{self.hostel.name} - {self.day_of_week} {self.meal_type}"


class VisitorLog(TimeStampedModel):
    """Visitor Entry/Exit Log"""
    
    PURPOSE_CHOICES = [
        ('parent', 'Parent Visit'),
        ('friend', 'Friend Visit'),
        ('relative', 'Relative'),
        ('official', 'Official'),
        ('delivery', 'Delivery'),
        ('other', 'Other'),
    ]
    
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='visitor_logs')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='hostel_visitors')
    
    visitor_name = models.CharField(max_length=200)
    visitor_phone = models.CharField(max_length=20)
    visitor_id_type = models.CharField(max_length=50, help_text="e.g., Aadhar, Driving License")
    visitor_id_number = models.CharField(max_length=50)
    
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES)
    purpose_details = models.TextField(blank=True)
    
    entry_time = models.DateTimeField(default=timezone.now)
    exit_time = models.DateTimeField(null=True, blank=True)
    
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='approved_visitors')
    
    remarks = models.TextField(blank=True)
    
    class Meta:
        db_table = 'hostel_visitor_logs'
        ordering = ['-entry_time']
        verbose_name = 'Visitor Log'
        verbose_name_plural = 'Visitor Logs'
        indexes = [
            models.Index(fields=['hostel', 'entry_time']),
            models.Index(fields=['student']),
        ]
    
    def __str__(self):
        return f"{self.visitor_name} visiting {self.student.user.email}"


class Complaint(TimeStampedModel):
    """Hostel Complaints"""
    
    CATEGORY_CHOICES = [
        ('maintenance', 'Maintenance'),
        ('electricity', 'Electricity'),
        ('water', 'Water Supply'),
        ('cleanliness', 'Cleanliness'),
        ('food', 'Food/Mess'),
        ('security', 'Security'),
        ('internet', 'Internet/WiFi'),
        ('other', 'Other'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('acknowledged', 'Acknowledged'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
        ('rejected', 'Rejected'),
    ]
    
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='complaints')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='hostel_complaints')
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='complaints')
    
    complaint_number = models.CharField(max_length=50, unique=True, db_index=True)
    
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted', db_index=True)
    
    submitted_date = models.DateTimeField(default=timezone.now)
    acknowledged_date = models.DateTimeField(null=True, blank=True)
    resolved_date = models.DateTimeField(null=True, blank=True)
    
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_complaints')
    
    resolution = models.TextField(blank=True)
    
    attachment = models.FileField(upload_to='hostel/complaints/%Y/%m/', blank=True, null=True)
    
    class Meta:
        db_table = 'hostel_complaints'
        ordering = ['-submitted_date']
        verbose_name = 'Complaint'
        verbose_name_plural = 'Complaints'
        indexes = [
            models.Index(fields=['complaint_number']),
            models.Index(fields=['hostel', 'status']),
            models.Index(fields=['student']),
        ]
    
    def __str__(self):
        return f"{self.complaint_number} - {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.complaint_number:
            year = timezone.now().year
            from django.db.models import Count
            count = Complaint.objects.filter(created_at__year=year).count() + 1
            self.complaint_number = f"COMP-{year}-{count:06d}"
        super().save(*args, **kwargs)


class OutingRequest(TimeStampedModel):
    """Student Outing/Leave Request"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('returned', 'Returned'),
    ]
    
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='outing_requests')
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='outing_requests')
    
    out_date = models.DateField()
    out_time = models.TimeField()
    expected_return_date = models.DateField()
    expected_return_time = models.TimeField()
    
    actual_return_date = models.DateField(null=True, blank=True)
    actual_return_time = models.TimeField(null=True, blank=True)
    
    destination = models.CharField(max_length=200)
    purpose = models.TextField()
    
    parent_contact = models.CharField(max_length=20)
    emergency_contact = models.CharField(max_length=20)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)
    
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_outings')
    approval_date = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    
    remarks = models.TextField(blank=True)
    
    class Meta:
        db_table = 'hostel_outing_requests'
        ordering = ['-created_at']
        verbose_name = 'Outing Request'
        verbose_name_plural = 'Outing Requests'
        indexes = [
            models.Index(fields=['student', 'status']),
            models.Index(fields=['hostel', 'out_date']),
        ]
    
    def __str__(self):
        return f"{self.student.user.email} - {self.out_date}"


class Attendance(TimeStampedModel):
    """Hostel Attendance"""
    
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('on_leave', 'On Leave'),
    ]
    
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='hostel_attendance')
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='attendance_records')
    
    date = models.DateField(db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    
    marked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='marked_hostel_attendance')
    marked_at = models.DateTimeField(auto_now_add=True)
    
    remarks = models.TextField(blank=True)
    
    class Meta:
        db_table = 'hostel_attendance'
        unique_together = ['student', 'date']
        ordering = ['-date']
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance Records'
        indexes = [
            models.Index(fields=['hostel', 'date']),
            models.Index(fields=['student', 'date']),
        ]
    
    def __str__(self):
        return f"{self.student.user.email} - {self.date} - {self.status}"

# Add managers to models
Hostel.add_to_class('objects', HostelManager())
Room.add_to_class('objects', RoomManager())
RoomAllocation.add_to_class('objects', RoomAllocationManager())
Complaint.add_to_class('objects', ComplaintManager())
OutingRequest.add_to_class('objects', OutingRequestManager())
