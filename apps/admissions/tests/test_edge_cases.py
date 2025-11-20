"""Edge case tests for admissions module"""
import pytest
from decimal import Decimal
from datetime import date
from django.utils import timezone
from django.core.exceptions import ValidationError
from apps.admissions.models import Application
from apps.admissions.services.application_service import ApplicationService
from apps.admissions.services.merit_list_service import MeritListService
from apps.authentication.models import User


@pytest.mark.django_db
class TestAdmissionsEdgeCases:
    """Test edge cases for admissions"""
    
    def test_application_missing_required_document(self):
        """Test application with missing required fields"""
        # Create incomplete application
        application_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            # Missing phone, date_of_birth, etc.
            'program': 'Computer Science',
            'admission_year': 2024,
            'admission_semester': 'Fall'
        }
        
        # This should create the application but validation should fail
        application = Application.objects.create(**application_data)
        
        errors = ApplicationService.validate_application(application)
        
        # Should have errors for missing required fields
        assert len(errors) > 0
        assert 'phone' in errors or 'date_of_birth' in errors
    
    def test_duplicate_admission_applications(self):
        """Test handling of duplicate applications for same program/year"""
        # Create first application
        app1 = Application.objects.create(
            first_name='Duplicate',
            last_name='Student',
            email='duplicate@example.com',
            phone='+1234567890',
            date_of_birth=date(2005, 1, 1),
            gender='male',
            address_line1='123 St',
            city='City',
            state='ST',
            postal_code='12345',
            country='Country',
            previous_school='High School',
            gpa=3.5,
            program='Computer Science',
            admission_year=2024,
            admission_semester='Fall',
            status='submitted'
        )
        
        # Create second application with same email/program/year
        app2 = Application.objects.create(
            first_name='Duplicate',
            last_name='Student',
            email='duplicate@example.com',  # Same email
            phone='+1234567891',
            date_of_birth=date(2005, 1, 1),
            gender='male',
            address_line1='456 St',
            city='City',
            state='ST',
            postal_code='12345',
            country='Country',
            previous_school='High School',
            gpa=3.5,
            program='Computer Science',  # Same program
            admission_year=2024,  # Same year
            admission_semester='Fall',
            status='draft'
        )
        
        # Validate second application
        errors = ApplicationService.validate_application(app2)
        
        # Should have error about duplicate email
        assert 'email' in errors
        assert 'already exists' in errors['email'].lower()
    
    def test_multiple_merit_list_generations(self):
        """Test multiple merit list generations maintain version numbers"""
        reviewer = User.objects.create(
            username='reviewer',
            email='reviewer@example.com',
            first_name='Reviewer',
            last_name='User'
        )
        
        # Create applications
        for i in range(3):
            Application.objects.create(
                first_name=f'Version{i}',
                last_name='Test',
                email=f'version{i}@example.com',
                phone=f'+123456789{i}',
                date_of_birth=date(2005, 1, 1),
                gender='male',
                address_line1='123 St',
                city='City',
                state='ST',
                postal_code='12345',
                country='Country',
                previous_school='High School',
                gpa=3.6,
                program='Mathematics',
                admission_year=2024,
                admission_semester='Fall',
                status='accepted',
                merit_score=Decimal(80 + i)
            )
        
        # Generate first merit list
        ml1 = MeritListService.generate_merit_list(
            name='Math Fall 2024 v1',
            program='Mathematics',
            admission_year=2024,
            admission_semester='Fall',
            criteria='Merit-based',
            generated_by=reviewer
        )
        
        # Generate second merit list
        ml2 = MeritListService.generate_merit_list(
            name='Math Fall 2024 v2',
            program='Mathematics',
            admission_year=2024,
            admission_semester='Fall',
            criteria='Merit-based',
            generated_by=reviewer
        )
        
        # Generate third merit list
        ml3 = MeritListService.generate_merit_list(
            name='Math Fall 2024 v3',
            program='Mathematics',
            admission_year=2024,
            admission_semester='Fall',
            criteria='Merit-based',
            generated_by=reviewer
        )
        
        # Verify version numbers are sequential
        assert ml1.version == 1
        assert ml2.version == 2
        assert ml3.version == 3
        
        # Verify all merit lists exist
        from apps.admissions.models import MeritList
        lists = MeritList.objects.filter(
            program='Mathematics',
            admission_year=2024,
            admission_semester='Fall'
        ).order_by('version')
        
        assert lists.count() == 3
        assert list(lists.values_list('version', flat=True)) == [1, 2, 3]
