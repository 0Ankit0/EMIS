from typing import List, Optional, Dict, Any
from decimal import Decimal
from django.utils import timezone
from django.db.models import Avg
from apps.courses.models import GradeRecord, Course
from apps.students.models import Student
from apps.core.exceptions import EMISException


class GradingService:
    """Service for managing grade records with calculation and finalization"""
    
    @staticmethod
    def create_grade_record(data: Dict[str, Any]) -> GradeRecord:
        """Create a new grade record"""
        course_id = data.get('course')
        student_id = data.get('student')
        
        # Verify course exists
        try:
            Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise EMISException(
                code="COURSES_003",
                message=f"Course {course_id} not found"
            )
        
        # Verify student exists
        try:
            Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            raise EMISException(
                code="COURSES_002",
                message=f"Student {student_id} not found"
            )
        
        # Calculate letter grade and grade points
        grade_value = data.get('grade_value')
        
        grade_record = GradeRecord(**data)
        grade_record.grade_letter = grade_record.calculate_grade_letter()
        grade_record.grade_points = grade_record.calculate_grade_points()
        grade_record.save()
        
        return grade_record
    
    @staticmethod
    def get_grade_record(grade_record_id: str) -> Optional[GradeRecord]:
        """Get a grade record by ID"""
        try:
            return GradeRecord.objects.select_related(
                'course',
                'student',
                'finalized_by'
            ).get(id=grade_record_id)
        except GradeRecord.DoesNotExist:
            return None
    
    @staticmethod
    def list_grade_records(
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 50,
        offset: int = 0
    ) -> tuple[List[GradeRecord], int]:
        """List grade records with optional filtering"""
        queryset = GradeRecord.objects.all()
        
        # Apply filters
        if filters:
            if 'course' in filters:
                queryset = queryset.filter(course_id=filters['course'])
            if 'student' in filters:
                queryset = queryset.filter(student_id=filters['student'])
            if 'finalized' in filters:
                queryset = queryset.filter(finalized=filters['finalized'])
            if 'semester' in filters:
                queryset = queryset.filter(semester=filters['semester'])
            if 'academic_year' in filters:
                queryset = queryset.filter(academic_year=filters['academic_year'])
        
        total = queryset.count()
        grade_records = list(
            queryset.select_related('course', 'student', 'finalized_by')[offset:offset + limit]
        )
        
        return grade_records, total
    
    @staticmethod
    def update_grade_record(grade_record_id: str, data: Dict[str, Any]) -> Optional[GradeRecord]:
        """Update a grade record (only if not finalized)"""
        try:
            grade_record = GradeRecord.objects.get(id=grade_record_id)
            
            if grade_record.finalized:
                raise EMISException(
                    code="COURSES_012",
                    message="Cannot update a finalized grade record"
                )
            
            # Don't allow updating course or student
            data.pop('course', None)
            data.pop('student', None)
            data.pop('finalized', None)
            data.pop('finalized_at', None)
            data.pop('finalized_by', None)
            
            # Update grade value and recalculate letter grade and points
            if 'grade_value' in data:
                grade_record.grade_value = data['grade_value']
                grade_record.grade_letter = grade_record.calculate_grade_letter()
                grade_record.grade_points = grade_record.calculate_grade_points()
            
            for key, value in data.items():
                if key not in ['grade_value']:
                    setattr(grade_record, key, value)
            
            grade_record.save()
            return grade_record
        except GradeRecord.DoesNotExist:
            return None
    
    @staticmethod
    def finalize_grade_record(
        grade_record_id: str,
        finalized_by_id: str
    ) -> Optional[GradeRecord]:
        """Finalize a grade record (makes it immutable)"""
        try:
            grade_record = GradeRecord.objects.get(id=grade_record_id)
            
            if grade_record.finalized:
                raise EMISException(
                    code="COURSES_013",
                    message="Grade record is already finalized"
                )
            
            grade_record.finalized = True
            grade_record.finalized_at = timezone.now()
            grade_record.finalized_by_id = finalized_by_id
            grade_record.save()
            
            return grade_record
        except GradeRecord.DoesNotExist:
            return None
    
    @staticmethod
    def get_student_grades(
        student_id: str,
        finalized_only: bool = False,
        semester: Optional[str] = None,
        academic_year: Optional[str] = None
    ) -> List[GradeRecord]:
        """Get all grade records for a student"""
        queryset = GradeRecord.objects.filter(student_id=student_id)
        
        if finalized_only:
            queryset = queryset.filter(finalized=True)
        
        if semester:
            queryset = queryset.filter(semester=semester)
        
        if academic_year:
            queryset = queryset.filter(academic_year=academic_year)
        
        return list(queryset.select_related('course').order_by('-created_at'))
    
    @staticmethod
    def calculate_gpa(
        student_id: str,
        semester: Optional[str] = None,
        academic_year: Optional[str] = None
    ) -> Optional[Decimal]:
        """
        Calculate GPA for a student
        
        Args:
            student_id: Student ID
            semester: Optional semester filter
            academic_year: Optional academic year filter
            
        Returns:
            GPA as Decimal or None if no finalized grades
        """
        queryset = GradeRecord.objects.filter(
            student_id=student_id,
            finalized=True
        )
        
        if semester:
            queryset = queryset.filter(semester=semester)
        
        if academic_year:
            queryset = queryset.filter(academic_year=academic_year)
        
        grades = list(queryset.select_related('course'))
        
        if not grades:
            return None
        
        # Calculate weighted GPA (grade points * course credits)
        total_points = Decimal('0.00')
        total_credits = Decimal('0.00')
        
        for grade in grades:
            credits = Decimal(str(grade.course.credits))
            total_points += Decimal(str(grade.grade_points)) * credits
            total_credits += credits
        
        if total_credits == 0:
            return Decimal('0.00')
        
        gpa = total_points / total_credits
        return round(gpa, 2)
    
    @staticmethod
    def get_course_grade_statistics(course_id: str) -> Dict[str, Any]:
        """Calculate grade statistics for a course"""
        grades = GradeRecord.objects.filter(
            course_id=course_id,
            finalized=True
        )
        
        total_students = grades.count()
        
        if total_students == 0:
            return {
                'total_students': 0,
                'average_grade': None,
                'highest_grade': None,
                'lowest_grade': None,
                'grade_distribution': {},
            }
        
        grade_values = [float(g.grade_value) for g in grades]
        average_grade = sum(grade_values) / len(grade_values)
        
        # Grade distribution by letter grade
        grade_distribution = {}
        for grade in grades:
            letter = grade.grade_letter
            grade_distribution[letter] = grade_distribution.get(letter, 0) + 1
        
        return {
            'total_students': total_students,
            'average_grade': round(average_grade, 2),
            'highest_grade': max(grade_values),
            'lowest_grade': min(grade_values),
            'grade_distribution': grade_distribution,
        }
