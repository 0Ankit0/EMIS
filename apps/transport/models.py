"""
Transport Models
"""
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import TimeStampedModel
from django.core.exceptions import ValidationError

User = get_user_model()


class Driver(TimeStampedModel):
    """Driver model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_profile')
    
    # Personal Information
    license_number = models.CharField(max_length=50, unique=True, db_index=True)
    license_type = models.CharField(
        max_length=20,
        choices=[
            ('light', 'Light Vehicle'),
            ('heavy', 'Heavy Vehicle'),
            ('commercial', 'Commercial'),
            ('other', 'Other'),
        ],
        default='light'
    )
    license_expiry_date = models.DateField()
    
    # Contact
    emergency_contact_name = models.CharField(max_length=200)
    emergency_contact_phone = models.CharField(max_length=20)
    
    # Employment
    date_of_joining = models.DateField()
    employment_status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Active'),
            ('on_leave', 'On Leave'),
            ('suspended', 'Suspended'),
            ('resigned', 'Resigned'),
        ],
        default='active',
        db_index=True
    )
    
    # Additional details
    experience_years = models.IntegerField(default=0, help_text="Years of driving experience")
    address = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'drivers'
        ordering = ['user__first_name', 'user__last_name']
        
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.license_number}"


class Vehicle(TimeStampedModel):
    """Vehicle model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Vehicle Details
    registration_number = models.CharField(max_length=50, unique=True, db_index=True)
    make = models.CharField(max_length=100, help_text="e.g., Toyota, Ford")
    model = models.CharField(max_length=100, help_text="e.g., Hiace, Transit")
    year = models.IntegerField(help_text="Manufacturing year")
    
    vehicle_type = models.CharField(
        max_length=50,
        choices=[
            ('bus', 'Bus'),
            ('van', 'Van'),
            ('car', 'Car'),
            ('minibus', 'Minibus'),
            ('other', 'Other'),
        ],
        default='bus',
        db_index=True
    )
    
    # Capacity
    seating_capacity = models.IntegerField(help_text="Number of seats")
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Active'),
            ('maintenance', 'Under Maintenance'),
            ('inactive', 'Inactive'),
            ('retired', 'Retired'),
        ],
        default='active',
        db_index=True
    )
    
    # Insurance & Registration
    insurance_number = models.CharField(max_length=100, blank=True)
    insurance_expiry_date = models.DateField(null=True, blank=True)
    registration_expiry_date = models.DateField(null=True, blank=True)
    
    # Current Assignment
    assigned_driver = models.ForeignKey(
        Driver,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_vehicles'
    )
    
    # Additional
    color = models.CharField(max_length=50, blank=True)
    fuel_type = models.CharField(
        max_length=20,
        choices=[
            ('petrol', 'Petrol'),
            ('diesel', 'Diesel'),
            ('cng', 'CNG'),
            ('electric', 'Electric'),
            ('hybrid', 'Hybrid'),
        ],
        default='diesel'
    )
    
    purchase_date = models.DateField(null=True, blank=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'vehicles'
        ordering = ['registration_number']
        
    def __str__(self):
        return f"{self.registration_number} - {self.make} {self.model}"


class Route(TimeStampedModel):
    """Transport route model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    route_number = models.CharField(max_length=20, unique=True, db_index=True)
    route_name = models.CharField(max_length=200)
    
    # Route Details
    start_point = models.CharField(max_length=200)
    end_point = models.CharField(max_length=200)
    total_distance_km = models.DecimalField(max_digits=6, decimal_places=2, help_text="Distance in kilometers")
    
    # Timing
    departure_time = models.TimeField()
    estimated_duration_minutes = models.IntegerField(help_text="Estimated duration in minutes")
    
    # Assignment
    assigned_vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='routes'
    )
    assigned_driver = models.ForeignKey(
        Driver,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='routes'
    )
    
    # Status
    is_active = models.BooleanField(default=True, db_index=True)
    route_type = models.CharField(
        max_length=20,
        choices=[
            ('pickup', 'Pickup'),
            ('drop', 'Drop'),
            ('both', 'Pickup & Drop'),
        ],
        default='both'
    )
    
    # Days of operation
    operates_monday = models.BooleanField(default=True)
    operates_tuesday = models.BooleanField(default=True)
    operates_wednesday = models.BooleanField(default=True)
    operates_thursday = models.BooleanField(default=True)
    operates_friday = models.BooleanField(default=True)
    operates_saturday = models.BooleanField(default=False)
    operates_sunday = models.BooleanField(default=False)
    
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'routes'
        ordering = ['route_number']
        
    def __str__(self):
        return f"{self.route_number} - {self.route_name}"
    
    def get_operating_days(self):
        """Get list of operating days"""
        days = []
        if self.operates_monday: days.append('Monday')
        if self.operates_tuesday: days.append('Tuesday')
        if self.operates_wednesday: days.append('Wednesday')
        if self.operates_thursday: days.append('Thursday')
        if self.operates_friday: days.append('Friday')
        if self.operates_saturday: days.append('Saturday')
        if self.operates_sunday: days.append('Sunday')
        return days


class RouteStop(TimeStampedModel):
    """Stop along a route"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='stops')
    stop_name = models.CharField(max_length=200)
    stop_address = models.TextField(blank=True)
    
    # Location
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Sequence
    sequence_number = models.IntegerField(help_text="Order of stop in route")
    arrival_time = models.TimeField(help_text="Estimated arrival time")
    
    # Fare
    fare_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'route_stops'
        ordering = ['route', 'sequence_number']
        unique_together = [['route', 'sequence_number']]
        
    def __str__(self):
        return f"{self.route.route_number} - Stop {self.sequence_number}: {self.stop_name}"


class StudentTransportAssignment(TimeStampedModel):
    """Assign students to routes"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='transport_assignments')
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='student_assignments')
    pickup_stop = models.ForeignKey(
        RouteStop,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pickup_assignments'
    )
    drop_stop = models.ForeignKey(
        RouteStop,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='drop_assignments'
    )
    
    # Dates
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True, db_index=True)
    
    # Payment
    monthly_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('paid', 'Paid'),
            ('pending', 'Pending'),
            ('overdue', 'Overdue'),
        ],
        default='pending'
    )
    
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'student_transport_assignments'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.route.route_number}"


class VehicleMaintenance(TimeStampedModel):
    """Vehicle maintenance records"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='maintenance_records')
    
    maintenance_type = models.CharField(
        max_length=50,
        choices=[
            ('routine', 'Routine Service'),
            ('repair', 'Repair'),
            ('inspection', 'Inspection'),
            ('tire_change', 'Tire Change'),
            ('oil_change', 'Oil Change'),
            ('other', 'Other'),
        ],
        db_index=True
    )
    
    description = models.TextField()
    maintenance_date = models.DateField()
    
    # Cost
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    vendor = models.CharField(max_length=200, blank=True)
    
    # Odometer
    odometer_reading = models.IntegerField(help_text="Odometer reading in km")
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('scheduled', 'Scheduled'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        default='scheduled',
        db_index=True
    )
    
    next_service_date = models.DateField(null=True, blank=True)
    next_service_odometer = models.IntegerField(null=True, blank=True)
    
    notes = models.TextField(blank=True)
    performed_by = models.CharField(max_length=200, blank=True)
    
    class Meta:
        db_table = 'vehicle_maintenance'
        ordering = ['-maintenance_date']
        
    def __str__(self):
        return f"{self.vehicle.registration_number} - {self.get_maintenance_type_display()} - {self.maintenance_date}"


class FuelLog(TimeStampedModel):
    """Fuel consumption log"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='fuel_logs')
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name='fuel_logs')
    
    # Fuel Details
    fuel_date = models.DateField()
    fuel_type = models.CharField(
        max_length=20,
        choices=[
            ('petrol', 'Petrol'),
            ('diesel', 'Diesel'),
            ('cng', 'CNG'),
        ],
        default='diesel'
    )
    quantity_liters = models.DecimalField(max_digits=6, decimal_places=2, help_text="Quantity in liters")
    price_per_liter = models.DecimalField(max_digits=6, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Odometer
    odometer_reading = models.IntegerField(help_text="Odometer reading in km")
    
    # Station
    fuel_station = models.CharField(max_length=200, blank=True)
    
    # Receipt
    receipt_number = models.CharField(max_length=100, blank=True)
    
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'fuel_logs'
        ordering = ['-fuel_date']
        
    def __str__(self):
        return f"{self.vehicle.registration_number} - {self.fuel_date} - {self.quantity_liters}L"
    
    def save(self, *args, **kwargs):
        """Calculate total cost"""
        if self.quantity_liters and self.price_per_liter:
            self.total_cost = self.quantity_liters * self.price_per_liter
        super().save(*args, **kwargs)


class RouteTracking(TimeStampedModel):
    """Track route execution/trips"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='tracking_logs')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='tracking_logs')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='tracking_logs')
    
    # Trip Details
    trip_date = models.DateField(db_index=True)
    actual_departure_time = models.TimeField()
    actual_arrival_time = models.TimeField(null=True, blank=True)
    
    # Odometer
    start_odometer = models.IntegerField()
    end_odometer = models.IntegerField(null=True, blank=True)
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('scheduled', 'Scheduled'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        default='scheduled',
        db_index=True
    )
    
    # Students
    students_count = models.IntegerField(default=0)
    
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'route_tracking'
        ordering = ['-trip_date', '-actual_departure_time']
        
    def __str__(self):
        return f"{self.route.route_number} - {self.trip_date} - {self.status}"
