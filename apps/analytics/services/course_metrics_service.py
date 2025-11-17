"""Course metrics service"""
from typing import Dict, Any
from django.db.models import Count, Avg, Q
from apps.courses.models import Course, Submission, GradeRecord


class CourseMetricsService:
    """Service for calculating course completion metrics"""
    
    @staticmethod
    def calculate_completion() -> Dict[str, Any]:
        """Calculate course completion metrics"""
        courses = Course.objects.all()
        submissions = Submission.objects.all()
        grades = GradeRecord.objects.all()
        
        total_courses = courses.count()
        active_courses = courses.filter(status='active').count()
        total_submissions = submissions.count()
        graded = submissions.filter(grade_status='graded').count()
        
        # Calculate average completion rate
        finalized_grades = grades.filter(finalized=True)
        total_grades = finalized_grades.count()
        
        return {
            'total_courses': total_courses,
            'active_courses': active_courses,
            'total_submissions': total_submissions,
            'graded_submissions': graded,
            'finalized_grades': total_grades,
            'grading_completion_rate': round((graded / total_submissions * 100) if total_submissions > 0 else 0, 2),
        }
