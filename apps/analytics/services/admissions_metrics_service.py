"""Admissions metrics service"""
from typing import Dict, Any
from django.db.models import Count, Q
from apps.admissions.models import Application


class AdmissionsMetricsService:
    """Service for calculating admissions metrics"""
    
    @staticmethod
    def calculate_funnel() -> Dict[str, Any]:
        """Calculate admissions funnel metrics"""
        applications = Application.objects.all()
        
        total = applications.count()
        submitted = applications.filter(status='submitted').count()
        under_review = applications.filter(status='under_review').count()
        accepted = applications.filter(status='accepted').count()
        rejected = applications.filter(status='rejected').count()
        enrolled = applications.filter(status='enrolled').count()
        
        return {
            'total_applications': total,
            'submitted': submitted,
            'under_review': under_review,
            'accepted': accepted,
            'rejected': rejected,
            'enrolled': enrolled,
            'acceptance_rate': round((accepted / total * 100) if total > 0 else 0, 2),
            'enrollment_rate': round((enrolled / accepted * 100) if accepted > 0 else 0, 2),
        }
