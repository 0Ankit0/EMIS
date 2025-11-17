"""Integration tests for course creation and prerequisite validation (T181)"""
import pytest
from django.utils import timezone
from datetime import timedelta
from apps.courses.models import Course
from apps.courses.services import CourseService
from apps.authentication.models import User
from apps.students.models import Student
from apps.courses.models import GradeRecord


@pytest.mark.django_db
class TestCourseFlow:
    """Test course creation with prerequisites"""
    
    def test_create_course_basic(self):
        """Test basic course creation"""
        # Create a faculty user
        user = User.objects.create_user(
            email="faculty@test.com",
            password="testpass123"
        )
        
        # Create course
        course_data = {
            'title': 'Introduction to Programming',
            'code': 'CS101',
            'description': 'Learn programming basics',
            'syllabus': 'Week 1: Variables, Week 2: Functions',
            'credits': 3,
            'status': 'active',
            'department': 'Computer Science',
            'semester': 'Fall 2024',
            'academic_year': '2024-2025',
        }
        
        course = CourseService.create_course(course_data, str(user.id))
        
        assert course.title == 'Introduction to Programming'
        assert course.code == 'CS101'
        assert course.credits == 3
        assert course.created_by == user
        assert course.status == 'active'
    
    def test_create_course_with_prerequisites(self):
        """Test course creation with prerequisites"""
        user = User.objects.create_user(
            email="faculty2@test.com",
            password="testpass123"
        )
        
        # Create prerequisite course
        prereq_course = CourseService.create_course({
            'title': 'CS Fundamentals',
            'code': 'CS100',
            'credits': 3,
            'status': 'active',
        }, str(user.id))
        
        # Create advanced course with prerequisite
        advanced_course = CourseService.create_course({
            'title': 'Data Structures',
            'code': 'CS201',
            'credits': 4,
            'prerequisites': [str(prereq_course.id)],
            'status': 'active',
        }, str(user.id))
        
        assert advanced_course.prerequisites == [str(prereq_course.id)]
    
    def test_prerequisite_validation_pass(self):
        """Test prerequisite validation when student has completed prerequisite"""
        user = User.objects.create_user(
            email="student@test.com",
            password="testpass123"
        )
        student = Student.objects.create(
            user=user,
            student_id="S001",
            program="CS"
        )
        
        faculty = User.objects.create_user(
            email="faculty3@test.com",
            password="testpass123"
        )
        
        # Create prerequisite course
        prereq_course = CourseService.create_course({
            'title': 'Intro CS',
            'code': 'CS100',
            'credits': 3,
            'status': 'active',
        }, str(faculty.id))
        
        # Create advanced course with prerequisite
        advanced_course = CourseService.create_course({
            'title': 'Advanced CS',
            'code': 'CS200',
            'credits': 3,
            'prerequisites': [str(prereq_course.id)],
            'status': 'active',
        }, str(faculty.id))
        
        # Student completes prerequisite with passing grade
        grade = GradeRecord.objects.create(
            course=prereq_course,
            student=student,
            grade_value=85.0,
            grade_letter='B',
            grade_points=3.0,
            finalized=True,
            finalized_at=timezone.now(),
            semester='Fall 2024',
            academic_year='2024-2025'
        )
        
        # Validate prerequisites
        is_valid, missing = CourseService.validate_prerequisites(
            student_id=str(student.id),
            course_id=str(advanced_course.id)
        )
        
        assert is_valid is True
        assert missing is None
    
    def test_prerequisite_validation_fail(self):
        """Test prerequisite validation when student hasn't completed prerequisite"""
        user = User.objects.create_user(
            email="student2@test.com",
            password="testpass123"
        )
        student = Student.objects.create(
            user=user,
            student_id="S002",
            program="CS"
        )
        
        faculty = User.objects.create_user(
            email="faculty4@test.com",
            password="testpass123"
        )
        
        # Create prerequisite course
        prereq_course = CourseService.create_course({
            'title': 'Intro CS',
            'code': 'CS101',
            'credits': 3,
            'status': 'active',
        }, str(faculty.id))
        
        # Create advanced course with prerequisite
        advanced_course = CourseService.create_course({
            'title': 'Advanced CS',
            'code': 'CS201',
            'credits': 3,
            'prerequisites': [str(prereq_course.id)],
            'status': 'active',
        }, str(faculty.id))
        
        # Student hasn't taken prerequisite
        # Validate prerequisites
        is_valid, missing = CourseService.validate_prerequisites(
            student_id=str(student.id),
            course_id=str(advanced_course.id)
        )
        
        assert is_valid is False
        assert missing is not None
        assert str(prereq_course.id) in missing
    
    def test_prerequisite_validation_no_prerequisites(self):
        """Test prerequisite validation when course has no prerequisites"""
        user = User.objects.create_user(
            email="student3@test.com",
            password="testpass123"
        )
        student = Student.objects.create(
            user=user,
            student_id="S003",
            program="CS"
        )
        
        faculty = User.objects.create_user(
            email="faculty5@test.com",
            password="testpass123"
        )
        
        # Create course without prerequisites
        course = CourseService.create_course({
            'title': 'Intro CS',
            'code': 'CS102',
            'credits': 3,
            'status': 'active',
        }, str(faculty.id))
        
        # Validate prerequisites
        is_valid, missing = CourseService.validate_prerequisites(
            student_id=str(student.id),
            course_id=str(course.id)
        )
        
        assert is_valid is True
        assert missing is None
