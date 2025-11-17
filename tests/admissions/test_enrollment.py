"""Tests for enrollment creation from applications"""
import pytest
from django.core.exceptions import ValidationError
from datetime import date
from apps.admissions.models import Application
from apps.students.models import Student, Enrollment
from apps.students.services.enrollment_service import EnrollmentService


@pytest.mark.django_db
class TestEnrollment:
    """Test enrollment creation from accepted applications"""
    
    def test_create_enrollment_from_accepted_application(self):
        """Test creating enrollment from accepted application"""
        # Create an accepted application
        application = Application.objects.create(
            first_name='Alice',
            last_name='Johnson',
            email='alice.johnson@example.com',
            phone='+1234567892',
            date_of_birth=date(2005, 3, 15),
            gender='female',
            address_line1='789 Pine St',
            city='Test City',
            state='TS',
            postal_code='12345',
            country='Test Country',
            previous_school='Test High School',
            previous_grade='A',
            gpa=3.7,
            program='Computer Science',
            admission_year=2024,
            admission_semester='Fall',
            status='accepted',
            merit_score=88.5,
            rank=1
        )
        
        # Create enrollment
        enrollment = EnrollmentService.create_enrollment_from_application(application)
        
        # Verify enrollment
        assert enrollment.id is not None
        assert enrollment.student is not None
        assert enrollment.program == 'Computer Science'
        assert enrollment.status == 'confirmed'
        assert enrollment.application == application
        
        # Verify student record
        student = enrollment.student
        assert student.email == 'alice.johnson@example.com'
        assert student.first_name == 'Alice'
        assert student.student_id is not None
        assert student.student_status == 'active'
        assert student.program == 'Computer Science'
        assert student.admission_year == 2024
        
        # Verify application status updated
        application.refresh_from_db()
        assert application.status == 'enrolled'
    
    def test_cannot_enroll_non_accepted_application(self):
        """Test that only accepted applications can be enrolled"""
        # Create a submitted (not accepted) application
        application = Application.objects.create(
            first_name='Bob',
            last_name='Williams',
            email='bob.williams@example.com',
            phone='+1234567893',
            date_of_birth=date(2005, 4, 20),
            gender='male',
            address_line1='321 Maple Dr',
            city='Test City',
            state='TS',
            postal_code='12345',
            country='Test Country',
            previous_school='Test High School',
            previous_grade='B+',
            gpa=3.5,
            program='Computer Science',
            admission_year=2024,
            admission_semester='Fall',
            status='submitted'  # Not accepted
        )
        
        # Attempt to create enrollment
        with pytest.raises(ValidationError) as exc_info:
            EnrollmentService.create_enrollment_from_application(application)
        
        assert 'only enroll from accepted applications' in str(exc_info.value).lower()
    
    def test_bulk_enrollment(self):
        """Test bulk enrollment of multiple applications"""
        # Create multiple accepted applications
        applications = []
        for i in range(3):
            app = Application.objects.create(
                first_name=f'Student{i}',
                last_name=f'Test{i}',
                email=f'student{i}@example.com',
                phone=f'+123456789{i}',
                date_of_birth=date(2005, 5, i+1),
                gender='male' if i % 2 == 0 else 'female',
                address_line1=f'{i+1} Test St',
                city='Test City',
                state='TS',
                postal_code='12345',
                country='Test Country',
                previous_school='Test High School',
                previous_grade='A',
                gpa=3.6 + (i * 0.1),
                program='Computer Science',
                admission_year=2024,
                admission_semester='Fall',
                status='accepted',
                merit_score=80 + i,
                rank=i + 1
            )
            applications.append(app)
        
        # Bulk enroll
        results = EnrollmentService.bulk_enroll([app.id for app in applications])
        
        # Verify results
        assert len(results['success']) == 3
        assert len(results['failed']) == 0
        
        # Verify enrollments created
        enrollments = Enrollment.objects.filter(application__in=applications)
        assert enrollments.count() == 3
        
        # Verify all applications marked as enrolled
        for app in applications:
            app.refresh_from_db()
            assert app.status == 'enrolled'
