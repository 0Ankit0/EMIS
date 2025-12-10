"""HR Models - Comprehensive Human Resource Management"""
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator, EmailValidator
from django.utils import timezone
from apps.core.models import TimeStampedModel
from decimal import Decimal
from datetime import date

User = get_user_model()


class Department(TimeStampedModel):
    """HR Department/Division"""
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=50, unique=True, db_index=True)
    description = models.TextField(blank=True)
    
    head = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='headed_departments'
    )
    
    parent_department = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sub_departments'
    )
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'hr_departments'
        ordering = ['name']
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class Designation(TimeStampedModel):
    """Job Designation/Position"""
    
    class Level(models.TextChoices):
        ENTRY = 'entry', 'Entry Level'
        JUNIOR = 'junior', 'Junior'
        MID = 'mid', 'Mid Level'
        SENIOR = 'senior', 'Senior'
        LEAD = 'lead', 'Lead'
        MANAGER = 'manager', 'Manager'
        DIRECTOR = 'director', 'Director'
        EXECUTIVE = 'executive', 'Executive'
    
    title = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=50, unique=True, db_index=True)
    description = models.TextField(blank=True)
    
    level = models.CharField(max_length=20, choices=Level.choices)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='designations')
    
    min_salary = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    max_salary = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    
    required_qualifications = models.TextField(blank=True)
    responsibilities = models.TextField(blank=True)
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'hr_designations'
        ordering = ['title']
        verbose_name = 'Designation'
        verbose_name_plural = 'Designations'
    
    def __str__(self):
        return self.title


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


class Attendance(TimeStampedModel):
    """Employee Attendance"""
    
    class Status(models.TextChoices):
        PRESENT = 'present', 'Present'
        ABSENT = 'absent', 'Absent'
        HALF_DAY = 'half_day', 'Half Day'
        LATE = 'late', 'Late'
        ON_LEAVE = 'on_leave', 'On Leave'
        WORK_FROM_HOME = 'work_from_home', 'Work From Home'
        HOLIDAY = 'holiday', 'Holiday'
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField(db_index=True)
    status = models.CharField(max_length=20, choices=Status.choices)
    
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    working_hours = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    
    marked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='marked_hr_attendance')
    remarks = models.TextField(blank=True)
    
    class Meta:
        db_table = 'hr_attendance'
        unique_together = ['employee', 'date']
        ordering = ['-date']
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance Records'
        indexes = [
            models.Index(fields=['employee', 'date']),
            models.Index(fields=['date', 'status']),
        ]
    
    def __str__(self):
        return f"{self.employee.employee_id} - {self.date} - {self.status}"


class Leave(TimeStampedModel):
    """Employee Leave Management"""
    
    class LeaveType(models.TextChoices):
        CASUAL = 'casual', 'Casual Leave'
        SICK = 'sick', 'Sick Leave'
        EARNED = 'earned', 'Earned Leave'
        MATERNITY = 'maternity', 'Maternity Leave'
        PATERNITY = 'paternity', 'Paternity Leave'
        UNPAID = 'unpaid', 'Unpaid Leave'
        COMPENSATORY = 'compensatory', 'Compensatory Off'
    
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
        CANCELLED = 'cancelled', 'Cancelled'
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_applications')
    
    leave_type = models.CharField(max_length=20, choices=LeaveType.choices)
    start_date = models.DateField()
    end_date = models.DateField()
    number_of_days = models.IntegerField(validators=[MinValueValidator(1)])
    
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True)
    
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_hr_leaves')
    approval_date = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    
    supporting_document = models.FileField(upload_to='hr/leaves/%Y/%m/', blank=True, null=True)
    
    class Meta:
        db_table = 'hr_leaves'
        ordering = ['-start_date']
        verbose_name = 'Leave'
        verbose_name_plural = 'Leaves'
        indexes = [
            models.Index(fields=['employee', 'status']),
            models.Index(fields=['start_date', 'end_date']),
        ]
    
    def __str__(self):
        return f"{self.employee.employee_id} - {self.leave_type} ({self.start_date})"
    
    def save(self, *args, **kwargs):
        """Calculate number of days"""
        if self.start_date and self.end_date:
            delta = self.end_date - self.start_date
            self.number_of_days = delta.days + 1
        super().save(*args, **kwargs)



class Payroll(TimeStampedModel):
    """Monthly Payroll"""
    
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PROCESSED = 'processed', 'Processed'
        PAID = 'paid', 'Paid'
        ON_HOLD = 'on_hold', 'On Hold'
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='payrolls')
    
    month = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    year = models.IntegerField(validators=[MinValueValidator(2000)])
    
    # Earnings
    basic_salary = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    hra = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    da = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    other_allowances = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    overtime_pay = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    bonus = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    gross_salary = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    
    # Deductions
    pf = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    esi = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    professional_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tds = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    loan_deduction = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    other_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    total_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    net_salary = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    
    # Attendance details
    working_days = models.IntegerField(validators=[MinValueValidator(0)])
    present_days = models.IntegerField(validators=[MinValueValidator(0)])
    leave_days = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True)
    
    payment_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    transaction_reference = models.CharField(max_length=100, blank=True)
    
    remarks = models.TextField(blank=True)
    
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='processed_payrolls')
    
    class Meta:
        db_table = 'hr_payrolls'
        unique_together = ['employee', 'month', 'year']
        ordering = ['-year', '-month']
        verbose_name = 'Payroll'
        verbose_name_plural = 'Payrolls'
        indexes = [
            models.Index(fields=['employee', 'year', 'month']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.employee.employee_id} - {self.month}/{self.year}"
    
    def save(self, *args, **kwargs):
        """Calculate gross, deductions and net salary"""
        self.gross_salary = (
            self.basic_salary + self.hra + self.da + 
            self.other_allowances + self.overtime_pay + self.bonus
        )
        
        self.total_deductions = (
            self.pf + self.esi + self.professional_tax + 
            self.tds + self.loan_deduction + self.other_deductions
        )
        
        self.net_salary = self.gross_salary - self.total_deductions
        
        super().save(*args, **kwargs)


class JobPosting(TimeStampedModel):
    """Job Opening/Vacancy Posting"""
    
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        OPEN = 'open', 'Open'
        CLOSED = 'closed', 'Closed'
        ON_HOLD = 'on_hold', 'On Hold'
    
    title = models.CharField(max_length=200)
    job_code = models.CharField(max_length=50, unique=True, db_index=True)
    
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='job_postings')
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE, related_name='job_postings')
    
    employment_type = models.CharField(max_length=20, choices=Employee.EmploymentType.choices)
    
    vacancies = models.IntegerField(validators=[MinValueValidator(1)])
    
    description = models.TextField()
    requirements = models.TextField()
    responsibilities = models.TextField()
    
    min_experience_years = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    max_experience_years = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    
    min_salary = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    max_salary = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    
    location = models.CharField(max_length=200)
    
    posted_date = models.DateField(default=timezone.now)
    closing_date = models.DateField(null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True)
    
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='posted_jobs')
    
    class Meta:
        db_table = 'hr_job_postings'
        ordering = ['-posted_date']
        verbose_name = 'Job Posting'
        verbose_name_plural = 'Job Postings'
        indexes = [
            models.Index(fields=['job_code']),
            models.Index(fields=['status', 'posted_date']),
        ]
    
    def __str__(self):
        return f"{self.job_code} - {self.title}"


class JobApplication(TimeStampedModel):
    """Job Application from Candidates"""
    
    class Status(models.TextChoices):
        SUBMITTED = 'submitted', 'Submitted'
        SCREENING = 'screening', 'Under Screening'
        SHORTLISTED = 'shortlisted', 'Shortlisted'
        INTERVIEW_SCHEDULED = 'interview_scheduled', 'Interview Scheduled'
        SELECTED = 'selected', 'Selected'
        REJECTED = 'rejected', 'Rejected'
        OFFER_SENT = 'offer_sent', 'Offer Sent'
        OFFER_ACCEPTED = 'offer_accepted', 'Offer Accepted'
        OFFER_DECLINED = 'offer_declined', 'Offer Declined'
        JOINED = 'joined', 'Joined'
    
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    
    # Candidate Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    current_location = models.CharField(max_length=200)
    
    total_experience_years = models.DecimalField(max_digits=4, decimal_places=1, validators=[MinValueValidator(0)])
    current_company = models.CharField(max_length=200, blank=True)
    current_designation = models.CharField(max_length=200, blank=True)
    current_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    expected_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    notice_period_days = models.IntegerField(null=True, blank=True)
    
    resume = models.FileField(upload_to='hr/applications/resumes/%Y/%m/')
    cover_letter = models.TextField(blank=True)
    
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.SUBMITTED, db_index=True)
    
    application_date = models.DateTimeField(default=timezone.now)
    
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='hr_reviewed_applications')
    review_notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'hr_job_applications'
        ordering = ['-application_date']
        verbose_name = 'Job Application'
        verbose_name_plural = 'Job Applications'
        indexes = [
            models.Index(fields=['job_posting', 'status']),
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.job_posting.title}"


class PerformanceReview(TimeStampedModel):
    """Employee Performance Review/Appraisal"""
    
    class ReviewType(models.TextChoices):
        PROBATION = 'probation', 'Probation Review'
        QUARTERLY = 'quarterly', 'Quarterly Review'
        HALF_YEARLY = 'half_yearly', 'Half-Yearly Review'
        ANNUAL = 'annual', 'Annual Review'
        SPECIAL = 'special', 'Special Review'
    
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'
    
    class Rating(models.IntegerChoices):
        POOR = 1, 'Poor'
        BELOW_AVERAGE = 2, 'Below Average'
        AVERAGE = 3, 'Average'
        GOOD = 4, 'Good'
        EXCELLENT = 5, 'Excellent'
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='performance_reviews')
    
    review_type = models.CharField(max_length=20, choices=ReviewType.choices)
    review_period_start = models.DateField()
    review_period_end = models.DateField()
    
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='conducted_reviews')
    
    # Ratings
    technical_skills = models.IntegerField(choices=Rating.choices, null=True, blank=True)
    communication = models.IntegerField(choices=Rating.choices, null=True, blank=True)
    teamwork = models.IntegerField(choices=Rating.choices, null=True, blank=True)
    leadership = models.IntegerField(choices=Rating.choices, null=True, blank=True)
    punctuality = models.IntegerField(choices=Rating.choices, null=True, blank=True)
    quality_of_work = models.IntegerField(choices=Rating.choices, null=True, blank=True)
    
    overall_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    
    strengths = models.TextField(blank=True)
    areas_of_improvement = models.TextField(blank=True)
    achievements = models.TextField(blank=True)
    goals_for_next_period = models.TextField(blank=True)
    
    comments = models.TextField(blank=True)
    employee_comments = models.TextField(blank=True)
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    
    review_date = models.DateField(null=True, blank=True)
    
    class Meta:
        db_table = 'hr_performance_reviews'
        ordering = ['-review_period_end']
        verbose_name = 'Performance Review'
        verbose_name_plural = 'Performance Reviews'
    
    def __str__(self):
        return f"{self.employee.employee_id} - {self.review_type} ({self.review_period_end})"
    
    def calculate_overall_rating(self):
        """Calculate overall rating from individual ratings"""
        ratings = [
            self.technical_skills, self.communication, self.teamwork,
            self.leadership, self.punctuality, self.quality_of_work
        ]
        valid_ratings = [r for r in ratings if r is not None]
        
        if valid_ratings:
            return round(sum(valid_ratings) / len(valid_ratings), 2)
        return None


class Training(TimeStampedModel):
    """Training Programs"""
    
    class Status(models.TextChoices):
        PLANNED = 'planned', 'Planned'
        ONGOING = 'ongoing', 'Ongoing'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'
    
    title = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True, db_index=True)
    description = models.TextField()
    
    trainer_name = models.CharField(max_length=200)
    trainer_organization = models.CharField(max_length=200, blank=True)
    
    start_date = models.DateField()
    end_date = models.DateField()
    duration_hours = models.IntegerField(validators=[MinValueValidator(1)])
    
    location = models.CharField(max_length=200)
    capacity = models.IntegerField(validators=[MinValueValidator(1)])
    
    cost_per_participant = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLANNED)
    
    organized_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='organized_trainings')
    
    class Meta:
        db_table = 'hr_trainings'
        ordering = ['-start_date']
        verbose_name = 'Training'
        verbose_name_plural = 'Trainings'
    
    def __str__(self):
        return f"{self.code} - {self.title}"


class TrainingParticipant(TimeStampedModel):
    """Training Participants"""
    
    class Status(models.TextChoices):
        ENROLLED = 'enrolled', 'Enrolled'
        ATTENDED = 'attended', 'Attended'
        COMPLETED = 'completed', 'Completed'
        DROPPED = 'dropped', 'Dropped'
    
    training = models.ForeignKey(Training, on_delete=models.CASCADE, related_name='participants')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='training_participations')
    
    enrollment_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ENROLLED)
    
    attendance_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    assessment_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    certificate_issued = models.BooleanField(default=False)
    certificate = models.FileField(upload_to='hr/training_certificates/%Y/', blank=True, null=True)
    
    feedback = models.TextField(blank=True)
    
    class Meta:
        db_table = 'hr_training_participants'
        unique_together = ['training', 'employee']
        ordering = ['-enrollment_date']
    
    def __str__(self):
        return f"{self.employee.employee_id} - {self.training.title}"


# Import and add managers
from .managers import (
    EmployeeManager, LeaveManager, PayrollManager,
    JobPostingManager, JobApplicationManager
)

Employee.add_to_class('objects', EmployeeManager())
Leave.add_to_class('objects', LeaveManager())
Payroll.add_to_class('objects', PayrollManager())
JobPosting.add_to_class('objects', JobPostingManager())
JobApplication.add_to_class('objects', JobApplicationManager())
