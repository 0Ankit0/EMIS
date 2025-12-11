"""HR Employee Model"""
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, EmailValidator
from apps.core.models import TimeStampedModel
from datetime import date
from .department import Department
from .designation import Designation

User = get_user_model()


class Employee(TimeStampedModel):
    """Employee/Staff Member"""
    
    class EmploymentType(models.TextChoices):
        FULL_TIME = 'full_time', 'Full Time'
        PART_TIME = 'part_time', 'Part Time'
        CONTRACT = 'contract', 'Contract'
        INTERN = 'intern', 'Intern'
        CONSULTANT = 'consultant', 'Consultant'
    
    class Gender(models.TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'
        OTHER = 'other', 'Other'
    
    class MaritalStatus(models.TextChoices):
        SINGLE = 'single', 'Single'
        MARRIED = 'married', 'Married'
        DIVORCED = 'divorced', 'Divorced'
        WIDOWED = 'widowed', 'Widowed'
    
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        ON_LEAVE = 'on_leave', 'On Leave'
        SUSPENDED = 'suspended', 'Suspended'
        TERMINATED = 'terminated', 'Terminated'
        RESIGNED = 'resigned', 'Resigned'
        RETIRED = 'retired', 'Retired'
    
    # Link to User
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    
    # Employee Information
    employee_id = models.CharField(max_length=50, unique=True, db_index=True)
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=Gender.choices)
    marital_status = models.CharField(max_length=20, choices=MaritalStatus.choices)
    blood_group = models.CharField(max_length=10, blank=True)
    
    # Contact Information
    phone = models.CharField(max_length=20)
    alternate_phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(validators=[EmailValidator()])
    personal_email = models.EmailField(blank=True)
    
    # Address
    current_address = models.TextField()
    permanent_address = models.TextField(blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    country = models.CharField(max_length=100, default='India')
    
    # Government IDs
    aadhar_number = models.CharField(max_length=12, blank=True)
    pan_number = models.CharField(max_length=10, blank=True)
    passport_number = models.CharField(max_length=20, blank=True)
    
    # Employment Details
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='employees')
    designation = models.ForeignKey(Designation, on_delete=models.PROTECT, related_name='employees')
    employment_type = models.CharField(max_length=20, choices=EmploymentType.choices)
    
    date_of_joining = models.DateField()
    date_of_leaving = models.DateField(null=True, blank=True)
    
    probation_period_months = models.IntegerField(default=6, validators=[MinValueValidator(0)])
    is_probation_completed = models.BooleanField(default=False)
    confirmation_date = models.DateField(null=True, blank=True)
    
    reporting_manager = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reportees'
    )
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE, db_index=True)
    
    # Salary Information
    basic_salary = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    hra = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    da = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    other_allowances = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    # Bank Details
    bank_name = models.CharField(max_length=200, blank=True)
    bank_account_number = models.CharField(max_length=50, blank=True)
    ifsc_code = models.CharField(max_length=20, blank=True)
    
    # Documents
    photo = models.ImageField(upload_to='hr/employees/photos/%Y/', blank=True, null=True)
    resume = models.FileField(upload_to='hr/employees/resumes/%Y/', blank=True, null=True)
    id_proof = models.FileField(upload_to='hr/employees/id_proofs/%Y/', blank=True, null=True)
    
    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=200, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    emergency_contact_relation = models.CharField(max_length=100, blank=True)
    
    # Additional
    notes = models.TextField(blank=True)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_employees')
    
    class Meta:
        db_table = 'hr_employees'
        ordering = ['employee_id']
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        indexes = [
            models.Index(fields=['employee_id']),
            models.Index(fields=['department', 'status']),
            models.Index(fields=['designation']),
        ]
    
    def __str__(self):
        return f"{self.employee_id} - {self.get_full_name()}"
    
    def get_full_name(self):
        """Get employee full name"""
        parts = [self.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        parts.append(self.last_name)
        return ' '.join(parts)
    
    def get_age(self):
        """Calculate employee age"""
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
    
    @property
    def gross_salary(self):
        """Calculate gross salary"""
        return self.basic_salary + self.hra + self.da + self.other_allowances
    
    @property
    def experience_years(self):
        """Calculate years of experience"""
        end_date = self.date_of_leaving if self.date_of_leaving else date.today()
        delta = end_date - self.date_of_joining
        return round(delta.days / 365.25, 2)
