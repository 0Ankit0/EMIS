from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone
from apps.core.models import TimeStampedModel
from decimal import Decimal
from .department import Department
from .managers import FacultyManager

User = get_user_model()

class Faculty(TimeStampedModel):
    """Faculty/Staff Member Profile"""
    class EmploymentType(models.TextChoices):
        FULL_TIME = 'full_time', 'Full Time'
        PART_TIME = 'part_time', 'Part Time'
        CONTRACT = 'contract', 'Contract'
        VISITING = 'visiting', 'Visiting'
        ADJUNCT = 'adjunct', 'Adjunct'
    
    class Designation(models.TextChoices):
        PROFESSOR = 'professor', 'Professor'
        ASSOCIATE_PROFESSOR = 'associate_professor', 'Associate Professor'
        ASSISTANT_PROFESSOR = 'assistant_professor', 'Assistant Professor'
        LECTURER = 'lecturer', 'Lecturer'
        SENIOR_LECTURER = 'senior_lecturer', 'Senior Lecturer'
        INSTRUCTOR = 'instructor', 'Instructor'
        TEACHING_ASSISTANT = 'teaching_assistant', 'Teaching Assistant'
        RESEARCH_ASSOCIATE = 'research_associate', 'Research Associate'
    
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        ON_LEAVE = 'on_leave', 'On Leave'
        SABBATICAL = 'sabbatical', 'Sabbatical'
        SUSPENDED = 'suspended', 'Suspended'
        RETIRED = 'retired', 'Retired'
        RESIGNED = 'resigned', 'Resigned'
    
    class Gender(models.TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'
        OTHER = 'other', 'Other'
    
    class BloodGroup(models.TextChoices):
        A_POSITIVE = 'A+', 'A+'
        A_NEGATIVE = 'A-', 'A-'
        B_POSITIVE = 'B+', 'B+'
        B_NEGATIVE = 'B-', 'B-'
        AB_POSITIVE = 'AB+', 'AB+'
        AB_NEGATIVE = 'AB-', 'AB-'
        O_POSITIVE = 'O+', 'O+'
        O_NEGATIVE = 'O-', 'O-'
    
    class CasteCategory(models.TextChoices):
        GENERAL = 'general', 'General'
        OBC = 'obc', 'OBC'
        SC = 'sc', 'SC'
        ST = 'st', 'ST'
        OTHER = 'other', 'Other'
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='faculty_profile')
    employee_id = models.CharField(max_length=50, unique=True, db_index=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be in format: '+999999999'. Up to 15 digits.")
    phone = models.CharField(validators=[phone_regex], max_length=17)
    alternate_phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    personal_email = models.EmailField(blank=True)
    official_email = models.EmailField(unique=True, db_index=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=Gender.choices)
    blood_group = models.CharField(max_length=5, choices=BloodGroup.choices, blank=True)
    nationality = models.CharField(max_length=100, default='Indian')
    religion = models.CharField(max_length=50, blank=True)
    caste_category = models.CharField(max_length=20, choices=CasteCategory.choices, blank=True)
    aadhar_number = models.CharField(max_length=12, blank=True, unique=True, null=True)
    pan_number = models.CharField(max_length=10, blank=True, unique=True, null=True)
    passport_number = models.CharField(max_length=20, blank=True)
    current_address = models.TextField()
    permanent_address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    country = models.CharField(max_length=100, default='India')
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='faculty_members')
    designation = models.CharField(max_length=50, choices=Designation.choices)
    specialization = models.CharField(max_length=200)
    employment_type = models.CharField(max_length=20, choices=EmploymentType.choices, default=EmploymentType.FULL_TIME)
    date_of_joining = models.DateField()
    date_of_leaving = models.DateField(null=True, blank=True)
    probation_period_months = models.IntegerField(default=6)
    is_probation_completed = models.BooleanField(default=False)
    confirmation_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE, db_index=True)
    is_teaching = models.BooleanField(default=True)
    is_research_active = models.BooleanField(default=False)
    is_hod = models.BooleanField(default=False, verbose_name='Is Head of Department')
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    grade_pay = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pay_scale = models.CharField(max_length=100, blank=True)
    bank_name = models.CharField(max_length=100, blank=True)
    bank_account_number = models.CharField(max_length=30, blank=True)
    ifsc_code = models.CharField(max_length=11, blank=True)
    max_weekly_hours = models.IntegerField(default=16, validators=[MinValueValidator(1), MaxValueValidator(40)])
    current_weekly_hours = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    research_interests = models.TextField(blank=True)
    publications_count = models.IntegerField(default=0)
    projects_count = models.IntegerField(default=0)
    photo = models.ImageField(upload_to='faculty/photos/%Y/%m/', blank=True, null=True)
    resume = models.FileField(upload_to='faculty/resumes/%Y/%m/', blank=True, null=True)
    id_proof = models.FileField(upload_to='faculty/documents/%Y/%m/', blank=True, null=True)
    linkedin_url = models.URLField(blank=True)
    google_scholar_url = models.URLField(blank=True)
    research_gate_url = models.URLField(blank=True)
    orcid_id = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_faculty')
    objects = FacultyManager()
    class Meta:
        db_table = 'faculty'
        ordering = ['employee_id']
        verbose_name = 'Faculty Member'
        verbose_name_plural = 'Faculty Members'
        indexes = [
            models.Index(fields=['employee_id']),
            models.Index(fields=['official_email']),
            models.Index(fields=['status']),
            models.Index(fields=['department', 'status']),
        ]
    def __str__(self):
        return f"{self.employee_id} - {self.get_full_name()}"
    def get_full_name(self):
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"
    def get_experience_years(self):
        if self.date_of_leaving:
            end_date = self.date_of_leaving
        else:
            end_date = timezone.now().date()
        delta = end_date - self.date_of_joining
        return delta.days / 365.25
    def get_age(self):
        today = timezone.now().date()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
    def is_available_for_teaching(self):
        return self.status == 'active' and self.is_teaching and self.current_weekly_hours < self.max_weekly_hours
