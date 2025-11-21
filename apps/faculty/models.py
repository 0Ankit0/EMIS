"""
Faculty Models - Comprehensive Faculty Management System
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone
from apps.core.models import TimeStampedModel
from decimal import Decimal
from .managers import FacultyManager, FacultyQualificationManager, FacultyExperienceManager

User = get_user_model()


class Department(TimeStampedModel):
    """Academic Department"""
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    head = models.ForeignKey('Faculty', on_delete=models.SET_NULL, null=True, blank=True, related_name='headed_department')
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'faculty_departments'
        ordering = ['name']
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class Faculty(TimeStampedModel):
    """Faculty/Staff Member Profile"""
    
    EMPLOYMENT_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('visiting', 'Visiting'),
        ('adjunct', 'Adjunct'),
    ]
    
    DESIGNATION_CHOICES = [
        ('professor', 'Professor'),
        ('associate_professor', 'Associate Professor'),
        ('assistant_professor', 'Assistant Professor'),
        ('lecturer', 'Lecturer'),
        ('senior_lecturer', 'Senior Lecturer'),
        ('instructor', 'Instructor'),
        ('teaching_assistant', 'Teaching Assistant'),
        ('research_associate', 'Research Associate'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('on_leave', 'On Leave'),
        ('sabbatical', 'Sabbatical'),
        ('suspended', 'Suspended'),
        ('retired', 'Retired'),
        ('resigned', 'Resigned'),
    ]
    
    # Link to User
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='faculty_profile')
    
    # Personal Information
    employee_id = models.CharField(max_length=50, unique=True, db_index=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be in format: '+999999999'. Up to 15 digits."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17)
    alternate_phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    personal_email = models.EmailField(blank=True)
    official_email = models.EmailField(unique=True, db_index=True)
    
    date_of_birth = models.DateField()
    gender = models.CharField(
        max_length=10,
        choices=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
        ]
    )
    
    blood_group = models.CharField(
        max_length=5,
        choices=[
            ('A+', 'A+'), ('A-', 'A-'),
            ('B+', 'B+'), ('B-', 'B-'),
            ('AB+', 'AB+'), ('AB-', 'AB-'),
            ('O+', 'O+'), ('O-', 'O-'),
        ],
        blank=True
    )
    
    nationality = models.CharField(max_length=100, default='Indian')
    religion = models.CharField(max_length=50, blank=True)
    caste_category = models.CharField(
        max_length=20,
        choices=[
            ('general', 'General'),
            ('obc', 'OBC'),
            ('sc', 'SC'),
            ('st', 'ST'),
            ('other', 'Other'),
        ],
        blank=True
    )
    
    # Government IDs
    aadhar_number = models.CharField(max_length=12, blank=True, unique=True, null=True)
    pan_number = models.CharField(max_length=10, blank=True, unique=True, null=True)
    passport_number = models.CharField(max_length=20, blank=True)
    
    # Address
    current_address = models.TextField()
    permanent_address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    country = models.CharField(max_length=100, default='India')
    
    # Professional Information
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='faculty_members')
    designation = models.CharField(max_length=50, choices=DESIGNATION_CHOICES)
    specialization = models.CharField(max_length=200)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES, default='full_time')
    
    # Employment Details
    date_of_joining = models.DateField()
    date_of_leaving = models.DateField(null=True, blank=True)
    probation_period_months = models.IntegerField(default=6)
    is_probation_completed = models.BooleanField(default=False)
    confirmation_date = models.DateField(null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', db_index=True)
    is_teaching = models.BooleanField(default=True)
    is_research_active = models.BooleanField(default=False)
    is_hod = models.BooleanField(default=False, verbose_name='Is Head of Department')
    
    # Salary Information
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    grade_pay = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pay_scale = models.CharField(max_length=100, blank=True)
    bank_name = models.CharField(max_length=100, blank=True)
    bank_account_number = models.CharField(max_length=30, blank=True)
    ifsc_code = models.CharField(max_length=11, blank=True)
    
    # Teaching Load
    max_weekly_hours = models.IntegerField(default=16, validators=[MinValueValidator(1), MaxValueValidator(40)])
    current_weekly_hours = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    # Research
    research_interests = models.TextField(blank=True)
    publications_count = models.IntegerField(default=0)
    projects_count = models.IntegerField(default=0)
    
    # Documents
    photo = models.ImageField(upload_to='faculty/photos/%Y/%m/', blank=True, null=True)
    resume = models.FileField(upload_to='faculty/resumes/%Y/%m/', blank=True, null=True)
    id_proof = models.FileField(upload_to='faculty/documents/%Y/%m/', blank=True, null=True)
    
    # Social Links
    linkedin_url = models.URLField(blank=True)
    google_scholar_url = models.URLField(blank=True)
    research_gate_url = models.URLField(blank=True)
    orcid_id = models.CharField(max_length=50, blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    # Metadata
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
        """Return full name"""
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"
    
    def get_experience_years(self):
        """Calculate total years of experience"""
        if self.date_of_leaving:
            end_date = self.date_of_leaving
        else:
            end_date = timezone.now().date()
        
        delta = end_date - self.date_of_joining
        return delta.days / 365.25
    
    def get_age(self):
        """Calculate current age"""
        today = timezone.now().date()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
    
    def is_available_for_teaching(self):
        """Check if faculty is available for teaching"""
        return self.status == 'active' and self.is_teaching and self.current_weekly_hours < self.max_weekly_hours


class FacultyQualification(TimeStampedModel):
    """Educational Qualifications of Faculty"""
    
    DEGREE_CHOICES = [
        ('phd', 'Ph.D.'),
        ('masters', 'Masters'),
        ('bachelors', 'Bachelors'),
        ('diploma', 'Diploma'),
        ('certification', 'Certification'),
        ('other', 'Other'),
    ]
    
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='qualifications')
    degree = models.CharField(max_length=50, choices=DEGREE_CHOICES)
    degree_name = models.CharField(max_length=200)
    specialization = models.CharField(max_length=200)
    institution = models.CharField(max_length=300)
    university = models.CharField(max_length=300)
    year_of_passing = models.IntegerField()
    percentage_or_cgpa = models.CharField(max_length=20)
    grade_system = models.CharField(
        max_length=20,
        choices=[
            ('percentage', 'Percentage'),
            ('cgpa_10', 'CGPA (10 Point)'),
            ('cgpa_4', 'CGPA (4 Point)'),
            ('grade', 'Grade'),
        ],
        default='percentage'
    )
    certificate = models.FileField(upload_to='faculty/qualifications/%Y/%m/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    
    objects = FacultyQualificationManager()
    
    class Meta:
        db_table = 'faculty_qualifications'
        ordering = ['-year_of_passing']
        verbose_name = 'Faculty Qualification'
        verbose_name_plural = 'Faculty Qualifications'
    
    def __str__(self):
        return f"{self.faculty.get_full_name()} - {self.degree_name}"


class FacultyExperience(TimeStampedModel):
    """Work Experience of Faculty"""
    
    EXPERIENCE_TYPE_CHOICES = [
        ('teaching', 'Teaching'),
        ('research', 'Research'),
        ('industry', 'Industry'),
        ('administrative', 'Administrative'),
        ('other', 'Other'),
    ]
    
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='experiences')
    organization = models.CharField(max_length=300)
    designation = models.CharField(max_length=200)
    experience_type = models.CharField(max_length=20, choices=EXPERIENCE_TYPE_CHOICES, default='teaching')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    responsibilities = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    certificate = models.FileField(upload_to='faculty/experience/%Y/%m/', blank=True, null=True)
    
    objects = FacultyExperienceManager()
    
    class Meta:
        db_table = 'faculty_experience'
        ordering = ['-start_date']
        verbose_name = 'Faculty Experience'
        verbose_name_plural = 'Faculty Experiences'
    
    def __str__(self):
        return f"{self.faculty.get_full_name()} - {self.designation} at {self.organization}"
    
    def get_duration_years(self):
        """Calculate duration in years"""
        end = self.end_date if self.end_date else timezone.now().date()
        delta = end - self.start_date
        return delta.days / 365.25


class FacultyAttendance(TimeStampedModel):
    """Daily Attendance for Faculty"""
    
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('on_leave', 'On Leave'),
        ('half_day', 'Half Day'),
        ('late', 'Late'),
        ('work_from_home', 'Work From Home'),
    ]
    
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField(db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    working_hours = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    remarks = models.TextField(blank=True)
    marked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='marked_faculty_attendance')
    
    class Meta:
        db_table = 'faculty_attendance'
        ordering = ['-date']
        unique_together = ['faculty', 'date']
        verbose_name = 'Faculty Attendance'
        verbose_name_plural = 'Faculty Attendance Records'
        indexes = [
            models.Index(fields=['faculty', 'date']),
            models.Index(fields=['date', 'status']),
        ]
    
    def __str__(self):
        return f"{self.faculty.get_full_name()} - {self.date} - {self.status}"


class FacultyLeave(TimeStampedModel):
    """Leave Applications for Faculty"""
    
    LEAVE_TYPE_CHOICES = [
        ('casual', 'Casual Leave'),
        ('sick', 'Sick Leave'),
        ('earned', 'Earned Leave'),
        ('maternity', 'Maternity Leave'),
        ('paternity', 'Paternity Leave'),
        ('compensatory', 'Compensatory Off'),
        ('unpaid', 'Unpaid Leave'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]
    
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='leave_applications')
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    number_of_days = models.IntegerField(validators=[MinValueValidator(1)])
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_faculty_leaves')
    approval_date = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    supporting_document = models.FileField(upload_to='faculty/leave_documents/%Y/%m/', blank=True, null=True)
    
    class Meta:
        db_table = 'faculty_leaves'
        ordering = ['-start_date']
        verbose_name = 'Faculty Leave'
        verbose_name_plural = 'Faculty Leaves'
        indexes = [
            models.Index(fields=['faculty', 'status']),
            models.Index(fields=['start_date', 'end_date']),
        ]
    
    def __str__(self):
        return f"{self.faculty.get_full_name()} - {self.leave_type} ({self.start_date} to {self.end_date})"
    
    def save(self, *args, **kwargs):
        # Calculate number of days
        if self.start_date and self.end_date:
            delta = self.end_date - self.start_date
            self.number_of_days = delta.days + 1
        super().save(*args, **kwargs)


class FacultyPublication(TimeStampedModel):
    """Research Publications by Faculty"""
    
    PUBLICATION_TYPE_CHOICES = [
        ('journal', 'Journal Article'),
        ('conference', 'Conference Paper'),
        ('book', 'Book'),
        ('chapter', 'Book Chapter'),
        ('patent', 'Patent'),
        ('other', 'Other'),
    ]
    
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='publications')
    title = models.CharField(max_length=500)
    publication_type = models.CharField(max_length=20, choices=PUBLICATION_TYPE_CHOICES)
    authors = models.TextField(help_text="Comma separated list of authors")
    journal_or_conference = models.CharField(max_length=300)
    volume = models.CharField(max_length=50, blank=True)
    issue = models.CharField(max_length=50, blank=True)
    pages = models.CharField(max_length=50, blank=True)
    year = models.IntegerField()
    doi = models.CharField(max_length=200, blank=True, verbose_name='DOI')
    isbn_issn = models.CharField(max_length=50, blank=True, verbose_name='ISBN/ISSN')
    url = models.URLField(blank=True)
    abstract = models.TextField(blank=True)
    keywords = models.CharField(max_length=500, blank=True)
    citation_count = models.IntegerField(default=0)
    impact_factor = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True)
    is_indexed = models.BooleanField(default=False, help_text="Indexed in Scopus/Web of Science")
    document = models.FileField(upload_to='faculty/publications/%Y/%m/', blank=True, null=True)
    
    class Meta:
        db_table = 'faculty_publications'
        ordering = ['-year', '-created_at']
        verbose_name = 'Faculty Publication'
        verbose_name_plural = 'Faculty Publications'
    
    def __str__(self):
        return f"{self.title[:50]} - {self.year}"


class FacultyAward(TimeStampedModel):
    """Awards and Achievements of Faculty"""
    
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='awards')
    title = models.CharField(max_length=300)
    awarding_body = models.CharField(max_length=300)
    date_received = models.DateField()
    description = models.TextField(blank=True)
    category = models.CharField(
        max_length=50,
        choices=[
            ('teaching', 'Teaching Excellence'),
            ('research', 'Research Excellence'),
            ('service', 'Service'),
            ('national', 'National Level'),
            ('international', 'International Level'),
            ('other', 'Other'),
        ],
        default='other'
    )
    certificate = models.FileField(upload_to='faculty/awards/%Y/%m/', blank=True, null=True)
    
    class Meta:
        db_table = 'faculty_awards'
        ordering = ['-date_received']
        verbose_name = 'Faculty Award'
        verbose_name_plural = 'Faculty Awards'
    
    def __str__(self):
        return f"{self.faculty.get_full_name()} - {self.title}"
