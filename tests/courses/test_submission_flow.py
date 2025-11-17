"""Integration tests for assignment submission with timestamp (T182)"""
import pytest
from django.utils import timezone
from datetime import timedelta
from apps.courses.models import Course, Assignment, Submission
from apps.courses.services import CourseService, AssignmentService, SubmissionService
from apps.authentication.models import User
from apps.students.models import Student


@pytest.mark.django_db
class TestSubmissionFlow:
    """Test assignment submission workflow"""
    
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
    
    def test_on_time_submission(self):
        """Test submission before deadline"""
        self.setup_test_data()
        
        # Create assignment with future deadline
        assignment = AssignmentService.create_assignment({
            'course': self.course.id,
            'title': 'Homework 1',
            'description': 'Complete exercises 1-10',
            'instructions': 'Submit Python files',
            'max_score': 100.0,
            'due_date': timezone.now() + timedelta(days=7),
            'late_submission_allowed': True,
            'late_penalty_percentage': 10.0,
            'assignment_type': 'homework',
            'is_published': True,
        })
        
        # Submit assignment on time
        submission = SubmissionService.create_submission({
            'assignment': assignment.id,
            'student': self.student.id,
            'content': 'My submission content',
            'files': ['solution.py'],
        })
        
        assert submission.is_late is False
        assert submission.late_penalty_applied == 0.0
        assert submission.assignment == assignment
        assert submission.student == self.student
    
    def test_late_submission(self):
        """Test submission after deadline with late penalty"""
        self.setup_test_data()
        
        # Create assignment with past deadline
        assignment = AssignmentService.create_assignment({
            'course': self.course.id,
            'title': 'Homework 2',
            'description': 'Complete exercises',
            'max_score': 100.0,
            'due_date': timezone.now() - timedelta(days=2),
            'late_submission_allowed': True,
            'late_penalty_percentage': 10.0,
            'assignment_type': 'homework',
            'is_published': True,
        })
        
        # Submit assignment late
        submission = SubmissionService.create_submission({
            'assignment': assignment.id,
            'student': self.student.id,
            'content': 'Late submission',
            'files': [],
        })
        
        assert submission.is_late is True
        assert submission.late_penalty_applied > 0
    
    def test_late_submission_not_allowed(self):
        """Test that late submission is rejected when not allowed"""
        self.setup_test_data()
        
        # Create assignment with past deadline and no late submissions allowed
        assignment = AssignmentService.create_assignment({
            'course': self.course.id,
            'title': 'Quiz 1',
            'description': 'Timed quiz',
            'max_score': 100.0,
            'due_date': timezone.now() - timedelta(hours=1),
            'late_submission_allowed': False,
            'assignment_type': 'quiz',
            'is_published': True,
        })
        
        # Try to submit late
        from apps.core.exceptions import EMISException
        with pytest.raises(EMISException) as exc_info:
            SubmissionService.create_submission({
                'assignment': assignment.id,
                'student': self.student.id,
                'content': 'Late submission attempt',
            })
        
        assert 'Late submissions are not allowed' in str(exc_info.value)
    
    def test_duplicate_submission_rejected(self):
        """Test that duplicate submissions are rejected"""
        self.setup_test_data()
        
        # Create assignment
        assignment = AssignmentService.create_assignment({
            'course': self.course.id,
            'title': 'Project 1',
            'description': 'Final project',
            'max_score': 100.0,
            'due_date': timezone.now() + timedelta(days=7),
            'is_published': True,
        })
        
        # First submission
        SubmissionService.create_submission({
            'assignment': assignment.id,
            'student': self.student.id,
            'content': 'First submission',
        })
        
        # Try duplicate submission
        from apps.core.exceptions import EMISException
        with pytest.raises(EMISException) as exc_info:
            SubmissionService.create_submission({
                'assignment': assignment.id,
                'student': self.student.id,
                'content': 'Second submission',
            })
        
        assert 'Submission already exists' in str(exc_info.value)
    
    def test_submission_timestamp_accuracy(self):
        """Test that submission timestamp is accurate"""
        self.setup_test_data()
        
        # Create assignment
        assignment = AssignmentService.create_assignment({
            'course': self.course.id,
            'title': 'Assignment 1',
            'description': 'Test assignment',
            'max_score': 100.0,
            'due_date': timezone.now() + timedelta(days=1),
            'is_published': True,
        })
        
        before_submission = timezone.now()
        
        # Submit assignment
        submission = SubmissionService.create_submission({
            'assignment': assignment.id,
            'student': self.student.id,
            'content': 'Submission content',
        })
        
        after_submission = timezone.now()
        
        # Verify timestamp is between before and after
        assert before_submission <= submission.submitted_at <= after_submission
