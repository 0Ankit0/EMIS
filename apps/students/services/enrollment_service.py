"""Enrollment service for student enrollment management"""
from typing import Dict, Optional
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import date
from ..models import Enrollment, Student
from apps.admissions.models import Application


class EnrollmentService:
    """Service for managing student enrollments"""
    
    @classmethod
    def create_enrollment_from_application(cls, application: Application) -> Enrollment:
        """Create student enrollment from an accepted application"""
        
        if application.status != 'accepted':
            raise ValidationError("Can only enroll from accepted applications")
        
        # Check if student already exists for this application
        if hasattr(application, 'student_record') and application.student_record:
            student = application.student_record
        else:
            # Create student record
            student = cls._create_student_from_application(application)
        
        # Create enrollment
        with transaction.atomic():
            enrollment = Enrollment.objects.create(
                student=student,
                program=application.program,
                batch=f"{application.admission_year}-{application.admission_semester}",
                section='',  # To be assigned later
                start_date=date.today(),
                status='confirmed',
                application=application,
                enrollment_data={
                    'application_number': application.application_number,
                    'merit_score': float(application.merit_score) if application.merit_score else None,
                    'rank': application.rank
                }
            )
            
            # Update application status
            application.status = 'enrolled'
            application.save()
            
            # Update student program info
            student.program = application.program
            student.batch = enrollment.batch
            student.admission_year = application.admission_year
            student.student_status = 'active'
            student.save()
            
            return enrollment
    
    @classmethod
    def _create_student_from_application(cls, application: Application) -> Student:
        """Create a student record from application data"""
        
        # Generate student ID
        student_id = cls._generate_student_id(application.admission_year, application.program)
        
        # Create student
        student = Student.objects.create(
            student_id=student_id,
            username=student_id,  # Use student_id as username
            email=application.email,
            first_name=application.first_name,
            last_name=application.last_name,
            phone=application.phone,
            date_of_birth=application.date_of_birth,
            gender=application.gender,
            admission_year=application.admission_year,
            program=application.program,
            batch='',  # Will be set in enrollment
            section='',
            student_status='active',
            guardian_name='',  # To be filled later
            guardian_phone='',
            emergency_contact_name='',
            emergency_contact_phone='',
            application=application
        )
        
        return student
    
    @classmethod
    def _generate_student_id(cls, admission_year: int, program: str) -> str:
        """Generate unique student ID"""
        # Format: YEAR-PROGRAM-SEQUENCE (e.g., 2024-CS-001)
        program_code = ''.join([c for c in program.upper() if c.isalpha()])[:3]
        
        # Get last student ID for this year/program
        last_student = Student.objects.filter(
            admission_year=admission_year,
            program__icontains=program_code
        ).order_by('-student_id').first()
        
        if last_student and '-' in last_student.student_id:
            try:
                last_sequence = int(last_student.student_id.split('-')[-1])
                next_sequence = last_sequence + 1
            except (ValueError, IndexError):
                next_sequence = 1
        else:
            next_sequence = 1
        
        return f"{admission_year}-{program_code}-{next_sequence:03d}"
    
    @classmethod
    def update_enrollment_status(cls, enrollment: Enrollment, new_status: str) -> Enrollment:
        """Update enrollment status"""
        valid_statuses = [choice[0] for choice in Enrollment.STATUS_CHOICES]
        
        if new_status not in valid_statuses:
            raise ValidationError(f"Invalid status: {new_status}")
        
        enrollment.status = new_status
        
        # Update actual_end_date if completed or withdrawn
        if new_status in ['completed', 'withdrawn']:
            enrollment.actual_end_date = date.today()
        
        enrollment.save()
        return enrollment
    
    @classmethod
    def assign_section(cls, enrollment: Enrollment, section: str) -> Enrollment:
        """Assign section to enrollment"""
        enrollment.section = section
        enrollment.save()
        
        # Also update student record
        enrollment.student.section = section
        enrollment.student.save()
        
        return enrollment
    
    @classmethod
    def get_active_enrollments(cls, student: Student) -> list:
        """Get active enrollments for a student"""
        return Enrollment.objects.filter(
            student=student,
            status='active'
        ).order_by('-start_date')
    
    @classmethod
    def bulk_enroll(cls, application_ids: list) -> Dict:
        """Bulk enroll students from applications"""
        results = {
            'success': [],
            'failed': []
        }
        
        applications = Application.objects.filter(id__in=application_ids, status='accepted')
        
        for application in applications:
            try:
                enrollment = cls.create_enrollment_from_application(application)
                results['success'].append({
                    'application_number': application.application_number,
                    'student_id': enrollment.student.student_id,
                    'enrollment_id': str(enrollment.id)
                })
            except Exception as e:
                results['failed'].append({
                    'application_number': application.application_number,
                    'error': str(e)
                })
        
        return results
