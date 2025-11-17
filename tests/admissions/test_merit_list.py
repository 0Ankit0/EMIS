"""Tests for merit list generation"""
import pytest
from decimal import Decimal
from datetime import date
from django.utils import timezone
from apps.admissions.models import Application, MeritList
from apps.admissions.services.merit_list_service import MeritListService
from apps.authentication.models import User


@pytest.mark.django_db
class TestMeritList:
    """Test merit list generation and ranking"""
    
    def test_generate_merit_list(self):
        """Test merit list generation with ranking"""
        reviewer = User.objects.create(
            username='admin',
            email='admin@example.com',
            first_name='Admin',
            last_name='User'
        )
        
        # Create applications with different merit scores
        for i in range(5):
            Application.objects.create(
                first_name=f'Student{i}',
                last_name='Test',
                email=f'student{i}@example.com',
                phone='+1234567890',
                date_of_birth=date(2005, 1, 1),
                gender='male',
                program='Computer Science',
                admission_year=2024,
                admission_semester='Fall',
                status='accepted',
                merit_score=Decimal(90 - i * 5),
                submitted_at=timezone.now(),
                previous_school='Test School',
                address_line1='123 St',
                city='City',
                state='ST',
                postal_code='12345',
                country='Country',
                gpa=3.8
            )
        
        merit_list = MeritListService.generate_merit_list(
            name='Fall 2024 CS Merit List',
            program='Computer Science',
            admission_year=2024,
            admission_semester='Fall',
            criteria='GPA-based ranking',
            generated_by=reviewer,
            total_seats=3
        )
        
        assert merit_list.id is not None
        assert merit_list.total_seats == 3
        assert merit_list.version == 1
        assert merit_list.program == 'Computer Science'
        
        # Verify applications are ranked
        applications = Application.objects.filter(
            program='Computer Science',
            admission_year=2024,
            admission_semester='Fall',
            rank__isnull=False
        ).order_by('rank')
        
        assert applications.count() >= 3
        assert applications.first().rank == 1
        assert applications.first().merit_score >= applications.last().merit_score
    
    def test_merit_list_idempotency(self):
        """Test that regenerating merit list produces consistent results"""
        reviewer = User.objects.create(
            username='admin2',
            email='admin2@example.com',
            first_name='Admin',
            last_name='User'
        )
        
        # Create applications
        for i in range(3):
            Application.objects.create(
                first_name=f'StudentX{i}',
                last_name='Test',
                email=f'studentx{i}@example.com',
                phone='+1234567890',
                date_of_birth=date(2005, 2, 1),
                gender='male',
                program='Engineering',
                admission_year=2024,
                admission_semester='Spring',
                status='accepted',
                merit_score=Decimal(85 - i * 3),
                submitted_at=timezone.now(),
                previous_school='Test School',
                address_line1='123 St',
                city='City',
                state='ST',
                postal_code='12345',
                country='Country',
                gpa=3.7
            )
        
        # Generate first merit list
        merit_list_1 = MeritListService.generate_merit_list(
            name='Spring 2024 Engineering Merit List',
            program='Engineering',
            admission_year=2024,
            admission_semester='Spring',
            criteria='Merit-based',
            generated_by=reviewer
        )
        
        # Generate second merit list (should have version 2)
        merit_list_2 = MeritListService.generate_merit_list(
            name='Spring 2024 Engineering Merit List v2',
            program='Engineering',
            admission_year=2024,
            admission_semester='Spring',
            criteria='Merit-based',
            generated_by=reviewer
        )
        
        assert merit_list_1.version == 1
        assert merit_list_2.version == 2
        
        # Verify rankings are consistent
        apps_after_1 = list(Application.objects.filter(
            program='Engineering',
            admission_year=2024
        ).order_by('rank').values_list('id', 'rank'))
        
        # Recalculate first merit list
        MeritListService.recalculate_ranks(merit_list_1)
        
        apps_after_recalc = list(Application.objects.filter(
            program='Engineering',
            admission_year=2024
        ).order_by('rank').values_list('id', 'rank'))
        
        assert apps_after_1 == apps_after_recalc  # Rankings should be idempotent

