"""Integration tests for transcript generation (T184)"""
import pytest
from django.utils import timezone
from apps.courses.models import Course, GradeRecord
from apps.courses.services import CourseService, GradingService
from apps.students.models import Student
from apps.students.services import TranscriptService
from apps.authentication.models import User


@pytest.mark.django_db
class TestTranscript:
    """Test transcript generation"""
    
    def setup_test_data(self):
        """Setup common test data"""
        # Create faculty user
        self.faculty = User.objects.create_user(
            email="faculty@test.com",
            password="testpass123"
        )
        
        # Create student user
        student_user = User.objects.create_user(
            email="student@test.com",
            password="testpass123"
        )
        self.student = Student.objects.create(
            user=student_user,
            student_id="S001",
            program="CS"
        )
        
        # Create courses
        self.course1 = CourseService.create_course({
            'title': 'Programming Fundamentals',
            'code': 'CS101',
            'credits': 3,
            'status': 'active',
        }, str(self.faculty.id))
        
        self.course2 = CourseService.create_course({
            'title': 'Data Structures',
            'code': 'CS201',
            'credits': 4,
            'status': 'active',
        }, str(self.faculty.id))
        
        self.course3 = CourseService.create_course({
            'title': 'Algorithms',
            'code': 'CS301',
            'credits': 3,
            'status': 'active',
        }, str(self.faculty.id))
    
    def test_generate_transcript_basic(self):
        """Test basic transcript generation"""
        self.setup_test_data()
        
        # Create and finalize grades
        grade1 = GradingService.create_grade_record({
            'course': self.course1.id,
            'student': self.student.id,
            'grade_value': 88.0,
            'semester': 'Fall 2024',
            'academic_year': '2024-2025',
        })
        GradingService.finalize_grade_record(str(grade1.id), str(self.faculty.id))
        
        grade2 = GradingService.create_grade_record({
            'course': self.course2.id,
            'student': self.student.id,
            'grade_value': 92.0,
            'semester': 'Fall 2024',
            'academic_year': '2024-2025',
        })
        GradingService.finalize_grade_record(str(grade2.id), str(self.faculty.id))
        
        # Generate transcript
        transcript = TranscriptService.generate_transcript(
            student_id=str(self.student.id),
            transcript_type='unofficial',
            generated_by_id=str(self.faculty.id)
        )
        
        assert transcript.student == self.student
        assert transcript.transcript_type == 'unofficial'
        assert transcript.total_credits_attempted == 7  # 3 + 4
        assert transcript.total_credits_earned == 7  # Both passing grades
        assert transcript.cumulative_gpa > 0
        assert len(transcript.grade_records_snapshot['grades']) == 2
    
    def test_transcript_only_includes_finalized_grades(self):
        """Test that transcript only includes finalized grades"""
        self.setup_test_data()
        
        # Create finalized grade
        grade1 = GradingService.create_grade_record({
            'course': self.course1.id,
            'student': self.student.id,
            'grade_value': 85.0,
            'semester': 'Fall 2024',
            'academic_year': '2024-2025',
        })
        GradingService.finalize_grade_record(str(grade1.id), str(self.faculty.id))
        
        # Create non-finalized grade
        grade2 = GradingService.create_grade_record({
            'course': self.course2.id,
            'student': self.student.id,
            'grade_value': 90.0,
            'semester': 'Fall 2024',
            'academic_year': '2024-2025',
        })
        # Don't finalize this one
        
        # Generate transcript
        transcript = TranscriptService.generate_transcript(
            student_id=str(self.student.id),
            transcript_type='unofficial'
        )
        
        # Should only include finalized grade
        assert len(transcript.grade_records_snapshot['grades']) == 1
        assert transcript.grade_records_snapshot['grades'][0]['course_code'] == 'CS101'
    
    def test_transcript_credits_calculation(self):
        """Test that transcript correctly calculates attempted vs earned credits"""
        self.setup_test_data()
        
        # Passing grade (>= 60)
        grade1 = GradingService.create_grade_record({
            'course': self.course1.id,
            'student': self.student.id,
            'grade_value': 85.0,
            'semester': 'Fall 2024',
            'academic_year': '2024-2025',
        })
        GradingService.finalize_grade_record(str(grade1.id), str(self.faculty.id))
        
        # Failing grade (< 60)
        grade2 = GradingService.create_grade_record({
            'course': self.course2.id,
            'student': self.student.id,
            'grade_value': 55.0,
            'semester': 'Fall 2024',
            'academic_year': '2024-2025',
        })
        GradingService.finalize_grade_record(str(grade2.id), str(self.faculty.id))
        
        # Generate transcript
        transcript = TranscriptService.generate_transcript(
            student_id=str(self.student.id),
            transcript_type='unofficial'
        )
        
        # Attempted: 3 + 4 = 7
        # Earned: 3 (only passing grade)
        assert transcript.total_credits_attempted == 7
        assert transcript.total_credits_earned == 3
    
    def test_transcript_semester_filter(self):
        """Test generating transcript for specific semester"""
        self.setup_test_data()
        
        # Fall 2024 grade
        grade1 = GradingService.create_grade_record({
            'course': self.course1.id,
            'student': self.student.id,
            'grade_value': 85.0,
            'semester': 'Fall 2024',
            'academic_year': '2024-2025',
        })
        GradingService.finalize_grade_record(str(grade1.id), str(self.faculty.id))
        
        # Spring 2025 grade
        grade2 = GradingService.create_grade_record({
            'course': self.course2.id,
            'student': self.student.id,
            'grade_value': 90.0,
            'semester': 'Spring 2025',
            'academic_year': '2024-2025',
        })
        GradingService.finalize_grade_record(str(grade2.id), str(self.faculty.id))
        
        # Generate transcript for Fall 2024 only
        transcript = TranscriptService.generate_transcript(
            student_id=str(self.student.id),
            semester='Fall 2024',
            transcript_type='unofficial'
        )
        
        assert len(transcript.grade_records_snapshot['grades']) == 1
        assert transcript.semester == 'Fall 2024'
    
    def test_certify_transcript(self):
        """Test certifying a transcript"""
        self.setup_test_data()
        
        # Create grade
        grade = GradingService.create_grade_record({
            'course': self.course1.id,
            'student': self.student.id,
            'grade_value': 88.0,
            'semester': 'Fall 2024',
            'academic_year': '2024-2025',
        })
        GradingService.finalize_grade_record(str(grade.id), str(self.faculty.id))
        
        # Generate unofficial transcript
        transcript = TranscriptService.generate_transcript(
            student_id=str(self.student.id),
            transcript_type='unofficial'
        )
        
        assert transcript.is_certified is False
        assert transcript.transcript_type == 'unofficial'
        
        # Certify it
        certified_transcript = TranscriptService.certify_transcript(
            transcript_id=str(transcript.id),
            certified_by_id=str(self.faculty.id)
        )
        
        assert certified_transcript.is_certified is True
        assert certified_transcript.transcript_type == 'official'
        assert certified_transcript.certification_date is not None
    
    def test_transcript_summary(self):
        """Test getting transcript summary"""
        self.setup_test_data()
        
        # Create grades
        grade1 = GradingService.create_grade_record({
            'course': self.course1.id,
            'student': self.student.id,
            'grade_value': 85.0,
            'semester': 'Fall 2024',
            'academic_year': '2024-2025',
        })
        GradingService.finalize_grade_record(str(grade1.id), str(self.faculty.id))
        
        grade2 = GradingService.create_grade_record({
            'course': self.course2.id,
            'student': self.student.id,
            'grade_value': 92.0,
            'semester': 'Fall 2024',
            'academic_year': '2024-2025',
        })
        GradingService.finalize_grade_record(str(grade2.id), str(self.faculty.id))
        
        # Get summary
        summary = TranscriptService.get_transcript_summary(str(self.student.id))
        
        assert summary['total_credits_attempted'] == 7
        assert summary['total_credits_earned'] == 7
        assert summary['cumulative_gpa'] > 0
        assert summary['courses_completed'] == 2
        assert summary['courses_failed'] == 0
        assert summary['total_courses'] == 2
