"""Management command to load sample data"""
from django.core.management.base import BaseCommand
from apps.students.models import Student
from apps.students.models.enrollment import Enrollment
from apps.courses.models.course import Course
from apps.admissions.models import Application
from apps.exams.models import Exam
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Load sample data for EMIS'

    def handle(self, *args, **kwargs):
        self.stdout.write('Loading sample data...')
        
        # Create sample students
        self.create_students()
        
        # Create sample courses
        self.create_courses()
        
        # Create sample enrollments
        self.create_enrollments()
        
        # Create sample exams
        self.create_exams()
        
        # Create sample applications
        self.create_applications()
        
        self.stdout.write(self.style.SUCCESS('Sample data loaded successfully!'))
    
    def create_students(self):
        """Create sample students"""
        self.stdout.write('Creating students...')
        
        programs = ['Computer Science', 'Business Administration', 'Engineering', 'Medicine', 'Law']
        genders = ['M', 'F']
        
        sample_students = [
            ('John', 'Doe', 'john.doe@example.com'),
            ('Jane', 'Smith', 'jane.smith@example.com'),
            ('Michael', 'Johnson', 'michael.j@example.com'),
            ('Emily', 'Williams', 'emily.w@example.com'),
            ('David', 'Brown', 'david.b@example.com'),
            ('Sarah', 'Davis', 'sarah.d@example.com'),
            ('Robert', 'Miller', 'robert.m@example.com'),
            ('Lisa', 'Wilson', 'lisa.w@example.com'),
            ('James', 'Moore', 'james.m@example.com'),
            ('Maria', 'Taylor', 'maria.t@example.com'),
        ]
        
        for first_name, last_name, email in sample_students:
            if not Student.objects.filter(email=email).exists():
                student = Student.objects.create_user(
                    username=email.split('@')[0],
                    email=email,
                    password='student123',
                    first_name=first_name,
                    last_name=last_name
                )
                student.student_id = f"ST{random.randint(100000, 999999)}"
                student.phone = f"+1{random.randint(2000000000, 9999999999)}"
                student.date_of_birth = datetime.now().date() - timedelta(days=random.randint(6570, 9125))  # 18-25 years
                student.gender = random.choice(genders)
                student.program = random.choice(programs)
                student.year = random.randint(1, 4)
                student.save()
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(sample_students)} students'))
    
    def create_courses(self):
        """Create sample courses"""
        self.stdout.write('Creating courses...')
        
        sample_courses = [
            ('CS101', 'Introduction to Programming', 3, 'Computer Science'),
            ('CS201', 'Data Structures and Algorithms', 4, 'Computer Science'),
            ('CS301', 'Database Systems', 3, 'Computer Science'),
            ('BUS101', 'Principles of Management', 3, 'Business'),
            ('BUS201', 'Financial Accounting', 4, 'Business'),
            ('ENG101', 'Engineering Mathematics', 4, 'Engineering'),
            ('ENG201', 'Thermodynamics', 3, 'Engineering'),
            ('MED101', 'Human Anatomy', 5, 'Medicine'),
            ('LAW101', 'Constitutional Law', 3, 'Law'),
            ('LAW201', 'Criminal Law', 4, 'Law'),
        ]
        
        for code, name, credits, dept in sample_courses:
            if not Course.objects.filter(code=code).exists():
                Course.objects.create(
                    code=code,
                    title=name,
                    credits=credits,
                    department=dept,
                    description=f"This is a comprehensive course on {name}.",
                    status='active'
                )
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(sample_courses)} courses'))
    
    def create_enrollments(self):
        """Create sample enrollments"""
        self.stdout.write('Skipping enrollments - model structure needs update')
        # TODO: Update once Enrollment model structure is finalized
    
    def create_exams(self):
        """Create sample exams"""
        self.stdout.write('Skipping exams - model structure needs update')
        # TODO: Update once Exam model structure is finalized
    
    def create_applications(self):
        """Create sample applications"""
        self.stdout.write('Creating applications...')
        
        programs = ['Computer Science', 'Business Administration', 'Engineering', 'Medicine', 'Law']
        statuses = ['pending', 'approved', 'rejected']
        
        sample_apps = [
            ('Alice', 'Anderson', 'alice.a@example.com', '+15551234567'),
            ('Bob', 'Baker', 'bob.b@example.com', '+15551234568'),
            ('Charlie', 'Clark', 'charlie.c@example.com', '+15551234569'),
            ('Diana', 'Davis', 'diana.d@example.com', '+15551234570'),
            ('Edward', 'Evans', 'edward.e@example.com', '+15551234571'),
        ]
        
        for first_name, last_name, email, phone in sample_apps:
            if not Application.objects.filter(email=email).exists():
                try:
                    Application.objects.create(
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        phone=phone,
                        date_of_birth=datetime.now().date() - timedelta(days=random.randint(6570, 7300)),
                        program=random.choice(programs),
                        status=random.choice(statuses),
                    )
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'Could not create application for {email}: {e}'))
        
        self.stdout.write(self.style.SUCCESS('Applications created (some may have been skipped)'))
