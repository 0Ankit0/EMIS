from typing import List, Optional, Dict, Any
from django.utils import timezone
from django.db.models import Q
from apps.courses.models import Submission, Assignment
from apps.students.models import Student
from apps.core.exceptions import EMISException


class SubmissionService:
    """Service for managing assignment submissions with late flag detection"""
    
    @staticmethod
    def create_submission(data: Dict[str, Any]) -> Submission:
        """Create a new submission with automatic late detection"""
        assignment_id = data.get('assignment')
        student_id = data.get('student')
        
        # Verify assignment exists
        try:
            assignment = Assignment.objects.get(id=assignment_id)
        except Assignment.DoesNotExist:
            raise EMISException(
                code="COURSES_007",
                message=f"Assignment {assignment_id} not found"
            )
        
        # Verify student exists
        try:
            Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            raise EMISException(
                code="COURSES_002",
                message=f"Student {student_id} not found"
            )
        
        # Check if submission already exists
        if Submission.objects.filter(
            assignment_id=assignment_id,
            student_id=student_id
        ).exists():
            raise EMISException(
                code="COURSES_008",
                message="Submission already exists for this assignment"
            )
        
        # Check if assignment is available for submission
        now = timezone.now()
        if assignment.available_from and now < assignment.available_from:
            raise EMISException(
                code="COURSES_009",
                message="Assignment is not yet available for submission"
            )
        
        # Check if late submissions are allowed
        is_late = now > assignment.due_date
        if is_late and not assignment.late_submission_allowed:
            raise EMISException(
                code="COURSES_010",
                message="Late submissions are not allowed for this assignment"
            )
        
        # Create submission (late penalty will be calculated in model's save method)
        submission = Submission.objects.create(**data)
        return submission
    
    @staticmethod
    def get_submission(submission_id: str) -> Optional[Submission]:
        """Get a submission by ID"""
        try:
            return Submission.objects.select_related(
                'assignment',
                'student',
                'graded_by'
            ).get(id=submission_id)
        except Submission.DoesNotExist:
            return None
    
    @staticmethod
    def list_submissions(
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 50,
        offset: int = 0
    ) -> tuple[List[Submission], int]:
        """List submissions with optional filtering"""
        queryset = Submission.objects.all()
        
        # Apply filters
        if filters:
            if 'assignment' in filters:
                queryset = queryset.filter(assignment_id=filters['assignment'])
            if 'student' in filters:
                queryset = queryset.filter(student_id=filters['student'])
            if 'grade_status' in filters:
                queryset = queryset.filter(grade_status=filters['grade_status'])
            if 'is_late' in filters:
                queryset = queryset.filter(is_late=filters['is_late'])
        
        total = queryset.count()
        submissions = list(
            queryset.select_related('assignment', 'student', 'graded_by')[offset:offset + limit]
        )
        
        return submissions, total
    
    @staticmethod
    def update_submission(submission_id: str, data: Dict[str, Any]) -> Optional[Submission]:
        """Update a submission"""
        try:
            submission = Submission.objects.get(id=submission_id)
            
            # Don't allow updating assignment or student
            data.pop('assignment', None)
            data.pop('student', None)
            
            for key, value in data.items():
                setattr(submission, key, value)
            submission.save()
            return submission
        except Submission.DoesNotExist:
            return None
    
    @staticmethod
    def grade_submission(
        submission_id: str,
        score: float,
        feedback: str,
        graded_by_id: str
    ) -> Optional[Submission]:
        """Grade a submission"""
        try:
            submission = Submission.objects.get(id=submission_id)
            
            # Validate score
            if score < 0 or score > submission.assignment.max_score:
                raise EMISException(
                    code="COURSES_011",
                    message=f"Score must be between 0 and {submission.assignment.max_score}"
                )
            
            submission.score = score
            submission.feedback = feedback
            submission.grade_status = 'graded'
            submission.graded_at = timezone.now()
            submission.graded_by_id = graded_by_id
            submission.save()
            
            return submission
        except Submission.DoesNotExist:
            return None
    
    @staticmethod
    def get_student_submissions(
        student_id: str,
        course_id: Optional[str] = None
    ) -> List[Submission]:
        """Get all submissions for a student"""
        queryset = Submission.objects.filter(student_id=student_id)
        
        if course_id:
            queryset = queryset.filter(assignment__course_id=course_id)
        
        return list(
            queryset.select_related('assignment', 'assignment__course')
            .order_by('-submitted_at')
        )
    
    @staticmethod
    def get_assignment_submissions(assignment_id: str) -> List[Submission]:
        """Get all submissions for an assignment"""
        return list(
            Submission.objects.filter(assignment_id=assignment_id)
            .select_related('student', 'graded_by')
            .order_by('-submitted_at')
        )
    
    @staticmethod
    def calculate_submission_statistics(assignment_id: str) -> Dict[str, Any]:
        """Calculate statistics for an assignment's submissions"""
        submissions = Submission.objects.filter(assignment_id=assignment_id)
        
        total_submissions = submissions.count()
        graded_submissions = submissions.filter(grade_status='graded').count()
        late_submissions = submissions.filter(is_late=True).count()
        
        # Calculate average score for graded submissions
        graded = submissions.filter(grade_status='graded', score__isnull=False)
        if graded.exists():
            avg_score = sum(s.score for s in graded) / graded.count()
        else:
            avg_score = None
        
        return {
            'total_submissions': total_submissions,
            'graded_submissions': graded_submissions,
            'pending_submissions': total_submissions - graded_submissions,
            'late_submissions': late_submissions,
            'average_score': avg_score,
        }
