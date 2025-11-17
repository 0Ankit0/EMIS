from typing import List, Optional, Dict, Any
from django.db.models import Q, Prefetch
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from apps.courses.models import Course
from apps.core.exceptions import EMISException


class CourseService:
    """Service for managing courses with CRUD operations and prerequisite validation"""
    
    @staticmethod
    def create_course(data: Dict[str, Any], created_by_id: str) -> Course:
        """Create a new course"""
        course = Course.objects.create(
            **data,
            created_by_id=created_by_id
        )
        return course
    
    @staticmethod
    def get_course(course_id: str) -> Optional[Course]:
        """Get a course by ID with related modules"""
        try:
            return Course.objects.prefetch_related('modules').get(id=course_id)
        except Course.DoesNotExist:
            return None
    
    @staticmethod
    def list_courses(
        filters: Optional[Dict[str, Any]] = None,
        search: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> tuple[List[Course], int]:
        """List courses with optional filtering and full-text search"""
        queryset = Course.objects.all()
        
        # Apply filters
        if filters:
            if 'status' in filters:
                queryset = queryset.filter(status=filters['status'])
            if 'department' in filters:
                queryset = queryset.filter(department=filters['department'])
            if 'semester' in filters:
                queryset = queryset.filter(semester=filters['semester'])
            if 'academic_year' in filters:
                queryset = queryset.filter(academic_year=filters['academic_year'])
            if 'created_by' in filters:
                queryset = queryset.filter(created_by_id=filters['created_by'])
        
        # Apply full-text search using PostgreSQL tsvector
        if search:
            search_vector = SearchVector('title', weight='A') + \
                          SearchVector('code', weight='A') + \
                          SearchVector('description', weight='B')
            search_query = SearchQuery(search)
            
            queryset = queryset.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
            ).filter(search=search_query).order_by('-rank')
        
        total = queryset.count()
        courses = list(queryset.prefetch_related('modules')[offset:offset + limit])
        
        return courses, total
    
    @staticmethod
    def update_course(course_id: str, data: Dict[str, Any]) -> Optional[Course]:
        """Update a course"""
        try:
            course = Course.objects.get(id=course_id)
            for key, value in data.items():
                setattr(course, key, value)
            course.save()
            return course
        except Course.DoesNotExist:
            return None
    
    @staticmethod
    def delete_course(course_id: str) -> bool:
        """Delete a course"""
        try:
            course = Course.objects.get(id=course_id)
            course.delete()
            return True
        except Course.DoesNotExist:
            return False
    
    @staticmethod
    def validate_prerequisites(
        student_id: str,
        course_id: str
    ) -> tuple[bool, Optional[List[str]]]:
        """
        Validate if a student has completed all prerequisites for a course
        
        Returns:
            tuple: (is_valid, list_of_missing_prerequisite_ids)
        """
        from apps.students.models import Student
        from apps.courses.models import GradeRecord
        
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise EMISException(
                code="COURSES_001",
                message=f"Course {course_id} not found"
            )
        
        # If no prerequisites, validation passes
        if not course.prerequisites:
            return True, None
        
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            raise EMISException(
                code="COURSES_002",
                message=f"Student {student_id} not found"
            )
        
        # Get student's completed courses (finalized grades with passing grade)
        completed_course_ids = set(
            GradeRecord.objects.filter(
                student=student,
                finalized=True,
                grade_value__gte=60  # Passing grade threshold
            ).values_list('course_id', flat=True)
        )
        
        # Check which prerequisites are missing
        missing_prerequisites = [
            str(prereq_id) for prereq_id in course.prerequisites
            if str(prereq_id) not in {str(cid) for cid in completed_course_ids}
        ]
        
        if missing_prerequisites:
            return False, missing_prerequisites
        
        return True, None
    
    @staticmethod
    def search_courses(query: str, limit: int = 20) -> List[Course]:
        """Full-text search for courses"""
        return list(
            Course.objects.filter(
                Q(title__icontains=query) |
                Q(code__icontains=query) |
                Q(description__icontains=query) |
                Q(department__icontains=query)
            )[:limit]
        )
