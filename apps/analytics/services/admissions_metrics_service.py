"""Admissions metrics service"""
from typing import Dict, Any
from django.db.models import Count, Q


class AdmissionsMetricsService:
    """Service for calculating admissions metrics"""
    
    @staticmethod
    def calculate_funnel() -> Dict[str, Any]:
        """Calculate admissions funnel metrics"""
        try:
            from apps.admissions.models import Application
            
            applications = Application.objects.all()
            
            total = applications.count()
            submitted = applications.filter(status='submitted').count()
            under_review = applications.filter(status='under_review').count()
            approved = applications.filter(status='approved').count()
            rejected = applications.filter(status='rejected').count()
            enrolled = applications.filter(status='enrolled').count()
            
            return {
                'total_applications': total,
                'submitted': submitted,
                'under_review': under_review,
                'approved': approved,
                'rejected': rejected,
                'enrolled': enrolled,
                'acceptance_rate': round((approved / total * 100) if total > 0 else 0, 2),
                'enrollment_rate': round((enrolled / approved * 100) if approved > 0 else 0, 2),
            }
        except Exception:
            return {
                'total_applications': 0,
                'submitted': 0,
                'under_review': 0,
                'approved': 0,
                'rejected': 0,
                'enrolled': 0,
                'acceptance_rate': 0,
                'enrollment_rate': 0,
            }
    
    @staticmethod
    def get_program_statistics() -> Dict[str, Any]:
        """Get statistics by program"""
        try:
            from apps.admissions.models import Application
            
            stats = Application.objects.values('program').annotate(
                total=Count('id'),
                approved=Count('id', filter=Q(status='approved'))
            )
            
            return list(stats)
        except Exception:
            return []
    
    @staticmethod
    def get_application_timeline() -> Dict[str, Any]:
        """Get application submission timeline"""
        try:
            from apps.admissions.models import Application
            from django.db.models.functions import TruncMonth
            
            timeline = Application.objects.annotate(
                month=TruncMonth('submitted_at')
            ).values('month').annotate(
                count=Count('id')
            ).order_by('month')
            
            return list(timeline)
        except Exception:
            return []
