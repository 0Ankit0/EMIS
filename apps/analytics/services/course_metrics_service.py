"""Course/Academic metrics service"""
from typing import Dict, Any
from django.db.models import Count, Avg, Q


class CourseMetricsService:
    """Service for calculating course/academic metrics"""
    
    @staticmethod
    def calculate_completion() -> Dict[str, Any]:
        """Calculate course completion metrics"""
        try:
            from apps.courses.models import Enrollment
            
            enrollments = Enrollment.objects.all()
            
            total = enrollments.count()
            completed = enrollments.filter(status='completed').count()
            in_progress = enrollments.filter(status='active').count()
            dropped = enrollments.filter(status='dropped').count()
            
            return {
                'total_enrollments': total,
                'completed': completed,
                'in_progress': in_progress,
                'dropped': dropped,
                'completion_rate': round((completed / total * 100) if total > 0 else 0, 2),
            }
        except Exception:
            return {
                'total_enrollments': 0,
                'completed': 0,
                'in_progress': 0,
                'dropped': 0,
                'completion_rate': 0,
            }
    
    @staticmethod
    def get_by_program() -> list:
        """Get course metrics by program"""
        try:
            from apps.courses.models import Enrollment
            
            stats = Enrollment.objects.values('course__program').annotate(
                total=Count('id'),
                completed=Count('id', filter=Q(status='completed'))
            )
            
            return list(stats)
        except Exception:
            return []
    
    @staticmethod
    def get_grade_distribution() -> Dict[str, Any]:
        """Get grade distribution"""
        try:
            from apps.courses.models import Enrollment
            
            grades = Enrollment.objects.exclude(
                final_grade__isnull=True
            ).values('final_grade').annotate(
                count=Count('id')
            )
            
            return list(grades)
        except Exception:
            return []
