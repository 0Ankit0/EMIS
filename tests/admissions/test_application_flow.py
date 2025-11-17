"""Tests for application submission and workflow"""
import pytest
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import date
from apps.admissions.models import Application
from apps.admissions.services.application_service import ApplicationService
from apps.authentication.models import User


@pytest.mark.django_db
class TestApplicationFlow:
    """Test application submission and status transitions"""
    
    def test_submit_application(self):
        """Test application submission with validation"""
        application_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '+1234567890',
            'date_of_birth': date(2005, 1, 1),
            'gender': 'male',
            'address_line1': '123 Main St',
            'city': 'Test City',
            'state': 'TS',
            'postal_code': '12345',
            'country': 'Test Country',
            'previous_school': 'Test High School',
            'previous_grade': 'A',
            'gpa': 3.8,
            'program': 'Computer Science',
            'admission_year': 2024,
            'admission_semester': 'Fall'
        }
        
        application = ApplicationService.submit_application(application_data)
        
        assert application.id is not None
        assert application.application_number is not None
        assert application.status == 'submitted'
        assert application.submitted_at is not None
        assert application.first_name == 'John'
        assert application.email == 'john.doe@example.com'
        
        # Test validation
        errors = ApplicationService.validate_application(application)
        assert len(errors) == 0
    
    def test_application_status_transitions(self):
        """Test application status transitions through workflow"""
        # Create application
        application = Application.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='jane.smith@example.com',
            phone='+1234567891',
            date_of_birth=date(2005, 2, 1),
            gender='female',
            address_line1='456 Oak Ave',
            city='Test City',
            state='TS',
            postal_code='12345',
            country='Test Country',
            previous_school='Test High School',
            previous_grade='A+',
            gpa=3.9,
            program='Computer Science',
            admission_year=2024,
            admission_semester='Fall',
            status='draft'
        )
        
        # Create reviewer
        reviewer = User.objects.create(
            username='reviewer1',
            email='reviewer@example.com',
            first_name='Review',
            last_name='User'
        )
        
        # Test valid transitions
        # draft -> submitted
        application = ApplicationService.update_status(application, 'submitted')
        assert application.status == 'submitted'
        
        # submitted -> under_review
        application = ApplicationService.update_status(
            application, 'under_review', reviewer=reviewer, review_notes='Reviewing application'
        )
        assert application.status == 'under_review'
        assert application.reviewed_by == reviewer
        assert application.reviewed_at is not None
        
        # under_review -> accepted
        application = ApplicationService.update_status(
            application, 'accepted', reviewer=reviewer, merit_score=85.5
        )
        assert application.status == 'accepted'
        assert application.merit_score == 85.5
        
        # Test invalid transition
        with pytest.raises(ValidationError) as exc_info:
            ApplicationService.update_status(application, 'draft')
        
        assert 'Cannot transition' in str(exc_info.value)

