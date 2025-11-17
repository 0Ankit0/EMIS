from typing import List, Optional, Dict, Any
from django.utils import timezone
from django.db.models import Q
from apps.courses.models import Assignment, Course
from apps.core.exceptions import EMISException


class AssignmentService:
    """Service for managing assignments with deadline enforcement"""
    
    @staticmethod
    def create_assignment(data: Dict[str, Any]) -> Assignment:
        """Create a new assignment"""
        course_id = data.get('course')
        
        # Verify course exists
        try:
            Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise EMISException(
                code="COURSES_003",
                message=f"Course {course_id} not found"
            )
        
        # Validate due date is in the future
        due_date = data.get('due_date')
        if due_date and due_date < timezone.now():
            raise EMISException(
                code="COURSES_005",
                message="Due date must be in the future"
            )
        
        # Validate available_from is before due_date
        available_from = data.get('available_from')
        if available_from and due_date and available_from >= due_date:
            raise EMISException(
                code="COURSES_006",
                message="Available date must be before due date"
            )
        
        assignment = Assignment.objects.create(**data)
        return assignment
    
    @staticmethod
    def get_assignment(assignment_id: str) -> Optional[Assignment]:
        """Get an assignment by ID"""
        try:
            return Assignment.objects.select_related('course').get(id=assignment_id)
        except Assignment.DoesNotExist:
            return None
    
    @staticmethod
    def list_assignments(
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 50,
        offset: int = 0
    ) -> tuple[List[Assignment], int]:
        """List assignments with optional filtering"""
        queryset = Assignment.objects.all()
        
        # Apply filters
        if filters:
            if 'course' in filters:
                queryset = queryset.filter(course_id=filters['course'])
            if 'assignment_type' in filters:
                queryset = queryset.filter(assignment_type=filters['assignment_type'])
            if 'is_published' in filters:
                queryset = queryset.filter(is_published=filters['is_published'])
            if 'overdue_only' in filters and filters['overdue_only']:
                queryset = queryset.filter(due_date__lt=timezone.now())
        
        total = queryset.count()
        assignments = list(queryset.select_related('course')[offset:offset + limit])
        
        return assignments, total
    
    @staticmethod
    def update_assignment(assignment_id: str, data: Dict[str, Any]) -> Optional[Assignment]:
        """Update an assignment"""
        try:
            assignment = Assignment.objects.get(id=assignment_id)
            
            # Validate due date if being updated
            if 'due_date' in data:
                due_date = data['due_date']
                if due_date < timezone.now():
                    raise EMISException(
                        code="COURSES_005",
                        message="Due date must be in the future"
                    )
            
            # Validate available_from vs due_date
            available_from = data.get('available_from', assignment.available_from)
            due_date = data.get('due_date', assignment.due_date)
            if available_from and due_date and available_from >= due_date:
                raise EMISException(
                    code="COURSES_006",
                    message="Available date must be before due date"
                )
            
            for key, value in data.items():
                setattr(assignment, key, value)
            assignment.save()
            return assignment
        except Assignment.DoesNotExist:
            return None
    
    @staticmethod
    def delete_assignment(assignment_id: str) -> bool:
        """Delete an assignment"""
        try:
            assignment = Assignment.objects.get(id=assignment_id)
            assignment.delete()
            return True
        except Assignment.DoesNotExist:
            return False
    
    @staticmethod
    def get_upcoming_assignments(
        course_id: Optional[str] = None,
        days_ahead: int = 7
    ) -> List[Assignment]:
        """Get assignments due in the next N days"""
        end_date = timezone.now() + timezone.timedelta(days=days_ahead)
        
        queryset = Assignment.objects.filter(
            due_date__gte=timezone.now(),
            due_date__lte=end_date,
            is_published=True
        )
        
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        
        return list(queryset.select_related('course').order_by('due_date'))
    
    @staticmethod
    def check_deadline_enforcement(assignment_id: str) -> Dict[str, Any]:
        """
        Check deadline status for an assignment
        
        Returns dict with:
        - is_available: bool
        - is_overdue: bool
        - can_submit: bool
        - time_remaining: timedelta or None
        """
        try:
            assignment = Assignment.objects.get(id=assignment_id)
        except Assignment.DoesNotExist:
            raise EMISException(
                code="COURSES_007",
                message=f"Assignment {assignment_id} not found"
            )
        
        now = timezone.now()
        
        # Check if available
        is_available = True
        if assignment.available_from:
            is_available = now >= assignment.available_from
        
        # Check if overdue
        is_overdue = now > assignment.due_date
        
        # Can submit if available and (not overdue OR late submissions allowed)
        can_submit = is_available and (not is_overdue or assignment.late_submission_allowed)
        
        # Calculate time remaining
        time_remaining = None
        if not is_overdue:
            time_remaining = assignment.due_date - now
        
        return {
            'is_available': is_available,
            'is_overdue': is_overdue,
            'can_submit': can_submit,
            'time_remaining': time_remaining,
            'late_submission_allowed': assignment.late_submission_allowed,
        }
