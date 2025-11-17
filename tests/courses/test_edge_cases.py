"""Edge case tests for courses (T186-T189)"""
import pytest
from django.utils import timezone
from datetime import timedelta
from apps.courses.models import Course, Assignment, Submission, Module
from apps.courses.services import (
    CourseService,
    AssignmentService,
    SubmissionService,
    ModuleService
)
from apps.authentication.models import User
from apps.students.models import Student


@pytest.mark.django_db
class TestCourseEdgeCases:
    """Test edge cases for course functionality"""
    
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
        
        self.course = CourseService.create_course({
            'title': 'Programming 101',
            'code': 'CS101',
            'credits': 3,
            'status': 'active',
        }, str(self.faculty.id))
    
    def test_assignment_submission_one_second_past_deadline(self):
        """Test assignment submission exactly one second past deadline (T186)"""
        self.setup_test_data()
        
        # Create assignment with very recent deadline
        due_date = timezone.now() - timedelta(seconds=1)
        assignment = AssignmentService.create_assignment({
            'course': self.course.id,
            'title': 'Strict Deadline Assignment',
            'description': 'Test assignment',
            'max_score': 100.0,
            'due_date': due_date,
            'late_submission_allowed': True,
            'late_penalty_percentage': 10.0,
            'assignment_type': 'quiz',
            'is_published': True,
        })
        
        # Submit one second late
        submission = SubmissionService.create_submission({
            'assignment': assignment.id,
            'student': self.student.id,
            'content': 'Slightly late submission',
        })
        
        assert submission.is_late is True
        assert submission.late_penalty_applied > 0
    
    def test_transcript_request_with_incomplete_grades(self):
        """Test transcript generation when some grades are incomplete (T187)"""
        from apps.courses.services import GradingService
        from apps.students.services import TranscriptService
        
        self.setup_test_data()
        
        course2 = CourseService.create_course({
            'title': 'Data Structures',
            'code': 'CS201',
            'credits': 4,
            'status': 'active',
        }, str(self.faculty.id))
        
        # Create one finalized grade
        grade1 = GradingService.create_grade_record({
            'course': self.course.id,
            'student': self.student.id,
            'grade_value': 85.0,
            'semester': 'Fall 2024',
            'academic_year': '2024-2025',
        })
        GradingService.finalize_grade_record(str(grade1.id), str(self.faculty.id))
        
        # Create one incomplete (non-finalized) grade
        grade2 = GradingService.create_grade_record({
            'course': course2.id,
            'student': self.student.id,
            'grade_value': 90.0,
            'semester': 'Fall 2024',
            'academic_year': '2024-2025',
        })
        # Don't finalize this one
        
        # Generate transcript - should only include finalized grades
        transcript = TranscriptService.generate_transcript(
            student_id=str(self.student.id),
            transcript_type='unofficial'
        )
        
        # Should only include the finalized grade
        assert len(transcript.grade_records_snapshot['grades']) == 1
        assert transcript.grade_records_snapshot['grades'][0]['course_code'] == 'CS101'
        assert transcript.total_credits_attempted == 3  # Only finalized course
    
    def test_deleted_course_content_access(self):
        """Test accessing content from a deleted course (T188)"""
        self.setup_test_data()
        
        # Create module
        module = ModuleService.create_module({
            'course': self.course.id,
            'title': 'Week 1 - Introduction',
            'content': 'Course introduction content',
            'sequence_order': 1,
            'is_published': True,
        })
        
        # Create assignment
        assignment = AssignmentService.create_assignment({
            'course': self.course.id,
            'title': 'Assignment 1',
            'description': 'First assignment',
            'max_score': 100.0,
            'due_date': timezone.now() + timedelta(days=7),
            'is_published': True,
        })
        
        module_id = str(module.id)
        assignment_id = str(assignment.id)
        
        # Delete the course (cascade delete)
        CourseService.delete_course(str(self.course.id))
        
        # Try to access deleted content
        deleted_module = ModuleService.get_module(module_id)
        deleted_assignment = AssignmentService.get_assignment(assignment_id)
        
        assert deleted_module is None
        assert deleted_assignment is None
    
    def test_course_withdrawal_impact_on_grades(self):
        """Test impact of course withdrawal on grade records (T189)"""
        from apps.courses.services import GradingService
        
        self.setup_test_data()
        
        # Create grade record
        grade = GradingService.create_grade_record({
            'course': self.course.id,
            'student': self.student.id,
            'grade_value': 85.0,
            'semester': 'Fall 2024',
            'academic_year': '2024-2025',
        })
        
        # Simulate withdrawal by updating grade letter to 'W'
        from apps.courses.models import GradeRecord
        grade_obj = GradeRecord.objects.get(id=grade.id)
        grade_obj.grade_letter = 'W'
        grade_obj.grade_value = 0.0
        grade_obj.grade_points = 0.0
        grade_obj.save()
        
        # Verify withdrawal grade
        withdrawn_grade = GradingService.get_grade_record(str(grade.id))
        assert withdrawn_grade.grade_letter == 'W'
        assert withdrawn_grade.grade_points == 0.0
    
    def test_assignment_with_zero_max_score(self):
        """Test creating assignment with zero max score (edge case)"""
        self.setup_test_data()
        
        # Create assignment with zero points (e.g., practice assignment)
        assignment = AssignmentService.create_assignment({
            'course': self.course.id,
            'title': 'Practice Exercise',
            'description': 'Ungraded practice',
            'max_score': 0.0,
            'due_date': timezone.now() + timedelta(days=7),
            'is_published': True,
        })
        
        assert assignment.max_score == 0.0
    
    def test_simultaneous_submissions(self):
        """Test handling of near-simultaneous submission attempts"""
        self.setup_test_data()
        
        assignment = AssignmentService.create_assignment({
            'course': self.course.id,
            'title': 'Test Assignment',
            'description': 'Test',
            'max_score': 100.0,
            'due_date': timezone.now() + timedelta(days=7),
            'is_published': True,
        })
        
        # First submission succeeds
        submission1 = SubmissionService.create_submission({
            'assignment': assignment.id,
            'student': self.student.id,
            'content': 'First submission',
        })
        
        assert submission1 is not None
        
        # Second submission should fail (duplicate)
        from apps.core.exceptions import EMISException
        with pytest.raises(EMISException) as exc_info:
            SubmissionService.create_submission({
                'assignment': assignment.id,
                'student': self.student.id,
                'content': 'Second submission',
            })
        
        assert 'already exists' in str(exc_info.value)
    
    def test_grade_boundary_values(self):
        """Test grade calculations at boundary values"""
        from apps.courses.services import GradingService
        
        self.setup_test_data()
        
        # Test exact boundary values
        boundary_tests = [
            (100.0, 'A+'),
            (97.0, 'A+'),
            (96.9, 'A'),
            (93.0, 'A'),
            (92.9, 'A-'),
            (90.0, 'A-'),
            (60.0, 'D'),
            (59.9, 'F'),
            (0.0, 'F'),
        ]
        
        for grade_value, expected_letter in boundary_tests:
            grade = GradingService.create_grade_record({
                'course': self.course.id,
                'student': self.student.id,
                'grade_value': grade_value,
                'semester': f'Test {grade_value}',
                'academic_year': '2024-2025',
            })
            
            assert grade.grade_letter == expected_letter, \
                f"Grade {grade_value} should be {expected_letter}, got {grade.grade_letter}"
    
    def test_module_reordering(self):
        """Test reordering modules in a course"""
        self.setup_test_data()
        
        # Create multiple modules
        module1 = ModuleService.create_module({
            'course': self.course.id,
            'title': 'Week 1',
            'sequence_order': 1,
        })
        
        module2 = ModuleService.create_module({
            'course': self.course.id,
            'title': 'Week 2',
            'sequence_order': 2,
        })
        
        module3 = ModuleService.create_module({
            'course': self.course.id,
            'title': 'Week 3',
            'sequence_order': 3,
        })
        
        # Reorder: 3, 1, 2
        new_order = [str(module3.id), str(module1.id), str(module2.id)]
        result = ModuleService.reorder_modules(str(self.course.id), new_order)
        
        assert result is True
        
        # Verify new order
        modules = ModuleService.list_modules_for_course(str(self.course.id))
        assert modules[0].id == module3.id
        assert modules[0].sequence_order == 1
        assert modules[1].id == module1.id
        assert modules[1].sequence_order == 2
        assert modules[2].id == module2.id
        assert modules[2].sequence_order == 3
