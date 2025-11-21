"""Tests for prerequisite validation before enrollment (T185)"""
import pytest
from django.utils import timezone
from apps.courses.models import Course, GradeRecord
from apps.courses.services import CourseService, GradingService
from apps.students.models import Student
from apps.authentication.models import User
from apps.core.exceptions import EMISException


@pytest.mark.django_db
class TestPrerequisites:
    """Test prerequisite validation"""
    
    def setup_test_data(self):
        """Setup common test data"""
        self.faculty = User.objects.create_user(
            email="faculty@test.com",
            password="testpass123"
        )
        
        student_user = User.objects.create_user(
            email="student@test.com",
            password="testpass123"
        )
        self.student = Student.objects.create(
            user=student_user,
            student_id="S001",
            program="CS"
        )
    
    def test_single_prerequisite_met(self):
        """Test validation when single prerequisite is met"""
        self.setup_test_data()
        
        # Create courses
        prereq = CourseService.create_course({
            'title': 'Intro to CS',
            'code': 'CS100',
            'credits': 3,
        }, str(self.faculty.id))
        
        advanced = CourseService.create_course({
            'title': 'Advanced CS',
            'code': 'CS200',
            'credits': 3,
            'prerequisites': [str(prereq.id)],
        }, str(self.faculty.id))
        
        # Student completes prerequisite
        grade = GradingService.create_grade_record({
            'course': prereq.id,
            'student': self.student.id,
            'grade_value': 75.0,
            'semester': 'Fall 2024',
            'academic_year': '2024-2025',
        })
        GradingService.finalize_grade_record(str(grade.id), str(self.faculty.id))
        
        # Validate prerequisites
        is_valid, missing = CourseService.validate_prerequisites(
            student_id=str(self.student.id),
            course_id=str(advanced.id)
        )
        
        assert is_valid is True
        assert missing is None
    
    def test_multiple_prerequisites_all_met(self):
        """Test validation when all multiple prerequisites are met"""
        self.setup_test_data()
        
        # Create prerequisite courses
        prereq1 = CourseService.create_course({
            'title': 'Math 101',
            'code': 'MATH101',
            'credits': 3,
        }, str(self.faculty.id))
        
        prereq2 = CourseService.create_course({
            'title': 'Programming 101',
            'code': 'CS101',
            'credits': 3,
        }, str(self.faculty.id))
        
        # Create advanced course requiring both prerequisites
        advanced = CourseService.create_course({
            'title': 'Advanced Programming',
            'code': 'CS301',
            'credits': 4,
            'prerequisites': [str(prereq1.id), str(prereq2.id)],
        }, str(self.faculty.id))
        
        # Student completes both prerequisites
        grade1 = GradingService.create_grade_record({
            'course': prereq1.id,
            'student': self.student.id,
            'grade_value': 80.0,
            'semester': 'Fall 2024',
            'academic_year': '2024-2025',
        })
        GradingService.finalize_grade_record(str(grade1.id), str(self.faculty.id))
        
        grade2 = GradingService.create_grade_record({
            'course': prereq2.id,
            'student': self.student.id,
            'grade_value': 85.0,
            'semester': 'Fall 2024',
            'academic_year': '2024-2025',
        })
        GradingService.finalize_grade_record(str(grade2.id), str(self.faculty.id))
        
        # Validate prerequisites
        is_valid, missing = CourseService.validate_prerequisites(
            student_id=str(self.student.id),
            course_id=str(advanced.id)
        )
        
        assert is_valid is True
        assert missing is None
    
    def test_multiple_prerequisites_one_missing(self):
        """Test validation when one of multiple prerequisites is missing"""
        self.setup_test_data()
        
        # Create prerequisite courses
        prereq1 = CourseService.create_course({
            'title': 'Math 101',
            'code': 'MATH101',
            'credits': 3,
        }, str(self.faculty.id))
        
        prereq2 = CourseService.create_course({
            'title': 'Programming 101',
            'code': 'CS101',
            'credits': 3,
        }, str(self.faculty.id))
        
        # Create advanced course requiring both
        advanced = CourseService.create_course({
            'title': 'Advanced Programming',
            'code': 'CS301',
            'credits': 4,
            'prerequisites': [str(prereq1.id), str(prereq2.id)],
        }, str(self.faculty.id))
        
        # Student only completes one prerequisite
        grade = GradingService.create_grade_record({
            'course': prereq1.id,
            'student': self.student.id,
            'grade_value': 80.0,
            'semester': 'Fall 2024',
            'academic_year': '2024-2025',
        })
        GradingService.finalize_grade_record(str(grade.id), str(self.faculty.id))
        
        # Validate prerequisites
        is_valid, missing = CourseService.validate_prerequisites(
            student_id=str(self.student.id),
            course_id=str(advanced.id)
        )
        
        assert is_valid is False
        assert missing is not None
        assert str(prereq2.id) in missing
        assert str(prereq1.id) not in missing
    
    def test_failing_grade_not_sufficient(self):
        """Test that failing grade doesn't meet prerequisite"""
        self.setup_test_data()
        
        # Create courses
        prereq = CourseService.create_course({
            'title': 'Intro CS',
            'code': 'CS100',
            'credits': 3,
        }, str(self.faculty.id))
        
        advanced = CourseService.create_course({
            'title': 'Advanced CS',
            'code': 'CS200',
            'credits': 3,
            'prerequisites': [str(prereq.id)],
        }, str(self.faculty.id))
        
        # Student fails prerequisite (< 60)
        grade = GradingService.create_grade_record({
            'course': prereq.id,
            'student': self.student.id,
            'grade_value': 55.0,
            'semester': 'Fall 2024',
            'academic_year': '2024-2025',
        })
        GradingService.finalize_grade_record(str(grade.id), str(self.faculty.id))
        
        # Validate prerequisites
        is_valid, missing = CourseService.validate_prerequisites(
            student_id=str(self.student.id),
            course_id=str(advanced.id)
        )
        
        assert is_valid is False
        assert missing is not None
        assert str(prereq.id) in missing
    
    def test_non_finalized_grade_not_counted(self):
        """Test that non-finalized grades don't count as completed prerequisites"""
        self.setup_test_data()
        
        # Create courses
        prereq = CourseService.create_course({
            'title': 'Intro CS',
            'code': 'CS100',
            'credits': 3,
        }, str(self.faculty.id))
        
        advanced = CourseService.create_course({
            'title': 'Advanced CS',
            'code': 'CS200',
            'credits': 3,
            'prerequisites': [str(prereq.id)],
        }, str(self.faculty.id))
        
        # Create passing grade but don't finalize it
        grade = GradingService.create_grade_record({
            'course': prereq.id,
            'student': self.student.id,
            'grade_value': 85.0,
            'semester': 'Fall 2024',
            'academic_year': '2024-2025',
        })
        # Don't finalize
        
        # Validate prerequisites
        is_valid, missing = CourseService.validate_prerequisites(
            student_id=str(self.student.id),
            course_id=str(advanced.id)
        )
        
        assert is_valid is False
        assert missing is not None
        assert str(prereq.id) in missing
