"""Integration tests for grading workflow (T183)"""
import pytest
from django.utils import timezone
from datetime import timedelta
from apps.courses.models import Course, Assignment, Submission, GradeRecord
from apps.courses.services import (
    CourseService,
    AssignmentService,
    SubmissionService,
    GradingService
)
from apps.authentication.models import User
from apps.students.models import Student


@pytest.mark.django_db
class TestGradingFlow:
    """Test grading workflow"""
    
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
        
        # Create course
        self.course = CourseService.create_course({
            'title': 'Programming 101',
            'code': 'CS101',
            'credits': 3,
            'status': 'active',
        }, str(self.faculty.id))
    
    def test_submission_grading(self):
        """Test grading a submission"""
        self.setup_test_data()
        
        # Create assignment
        assignment = AssignmentService.create_assignment({
            'course': self.course.id,
            'title': 'Homework 1',
            'description': 'Complete exercises',
            'max_score': 100.0,
            'due_date': timezone.now() + timedelta(days=7),
            'is_published': True,
        })
        
        # Create submission
        submission = SubmissionService.create_submission({
            'assignment': assignment.id,
            'student': self.student.id,
            'content': 'My solution',
        })
        
        # Grade the submission
        graded_submission = SubmissionService.grade_submission(
            submission_id=str(submission.id),
            score=85.0,
            feedback='Good work! Minor improvements needed.',
            graded_by_id=str(self.faculty.id)
        )
        
        assert graded_submission.score == 85.0
        assert graded_submission.feedback == 'Good work! Minor improvements needed.'
        assert graded_submission.grade_status == 'graded'
        assert graded_submission.graded_by == self.faculty
        assert graded_submission.graded_at is not None
    
    def test_create_grade_record(self):
        """Test creating a grade record for a course"""
        self.setup_test_data()
        
        # Create grade record
        grade_record = GradingService.create_grade_record({
            'course': self.course.id,
            'student': self.student.id,
            'grade_value': 88.5,
            'semester': 'Fall 2024',
            'academic_year': '2024-2025',
        })
        
        assert grade_record.grade_value == 88.5
        assert grade_record.grade_letter == 'B+'
        assert grade_record.grade_points == 3.30
        assert grade_record.finalized is False
    
    def test_grade_letter_calculation(self):
        """Test automatic grade letter calculation"""
        self.setup_test_data()
        
        test_cases = [
            (97, 'A+'),
            (95, 'A'),
            (90, 'A-'),
            (87, 'B+'),
            (85, 'B'),
            (80, 'B-'),
            (77, 'C+'),
            (75, 'C'),
            (70, 'C-'),
            (65, 'D'),
            (55, 'F'),
        ]
        
        for grade_value, expected_letter in test_cases:
            grade_record = GradingService.create_grade_record({
                'course': self.course.id,
                'student': self.student.id,
                'grade_value': grade_value,
                'semester': f'Test {grade_value}',
                'academic_year': '2024-2025',
            })
            
            assert grade_record.grade_letter == expected_letter, \
                f"Grade {grade_value} should be {expected_letter}, got {grade_record.grade_letter}"
    
    def test_finalize_grade_record(self):
        """Test finalizing a grade record"""
        self.setup_test_data()
        
        # Create grade record
        grade_record = GradingService.create_grade_record({
            'course': self.course.id,
            'student': self.student.id,
            'grade_value': 92.0,
            'semester': 'Fall 2024',
            'academic_year': '2024-2025',
        })
        
        assert grade_record.finalized is False
        
        # Finalize it
        finalized_grade = GradingService.finalize_grade_record(
            grade_record_id=str(grade_record.id),
            finalized_by_id=str(self.faculty.id)
        )
        
        assert finalized_grade.finalized is True
        assert finalized_grade.finalized_by == self.faculty
        assert finalized_grade.finalized_at is not None
    
    def test_cannot_update_finalized_grade(self):
        """Test that finalized grades cannot be updated"""
        self.setup_test_data()
        
        # Create and finalize grade record
        grade_record = GradingService.create_grade_record({
            'course': self.course.id,
            'student': self.student.id,
            'grade_value': 85.0,
            'semester': 'Fall 2024',
            'academic_year': '2024-2025',
        })
        
        GradingService.finalize_grade_record(
            grade_record_id=str(grade_record.id),
            finalized_by_id=str(self.faculty.id)
        )
        
        # Try to update finalized grade
        from apps.core.exceptions import EMISException
        with pytest.raises(EMISException) as exc_info:
            GradingService.update_grade_record(
                grade_record_id=str(grade_record.id),
                data={'grade_value': 90.0}
            )
        
        assert 'Cannot update a finalized grade record' in str(exc_info.value)
    
    def test_calculate_gpa(self):
        """Test GPA calculation"""
        self.setup_test_data()
        
        # Create another course
        course2 = CourseService.create_course({
            'title': 'Data Structures',
            'code': 'CS201',
            'credits': 4,
            'status': 'active',
        }, str(self.faculty.id))
        
        # Create finalized grades
        # Course 1: Grade B (3.0 points) * 3 credits = 9.0
        grade1 = GradingService.create_grade_record({
            'course': self.course.id,
            'student': self.student.id,
            'grade_value': 85.0,
            'semester': 'Fall 2024',
            'academic_year': '2024-2025',
        })
        GradingService.finalize_grade_record(str(grade1.id), str(self.faculty.id))
        
        # Course 2: Grade A (4.0 points) * 4 credits = 16.0
        grade2 = GradingService.create_grade_record({
            'course': course2.id,
            'student': self.student.id,
            'grade_value': 95.0,
            'semester': 'Fall 2024',
            'academic_year': '2024-2025',
        })
        GradingService.finalize_grade_record(str(grade2.id), str(self.faculty.id))
        
        # Total: (9.0 + 16.0) / (3 + 4) = 25.0 / 7 = 3.57
        gpa = GradingService.calculate_gpa(str(self.student.id))
        
        assert gpa is not None
        assert 3.57 == float(gpa)
