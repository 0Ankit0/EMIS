"""Fee/Finance metrics service"""
from typing import Dict, Any
from django.db.models import Count, Sum, Q


class FeeMetricsService:
    """Service for calculating fee/finance metrics"""
    
    @staticmethod
    def calculate_collection() -> Dict[str, Any]:
        """Calculate fee collection metrics"""
        try:
            from apps.finance.models import FeePayment
            
            payments = FeePayment.objects.all()
            
            total_expected = payments.aggregate(Sum('amount'))['amount__sum'] or 0
            total_paid = payments.filter(status='paid').aggregate(Sum('amount'))['amount__sum'] or 0
            total_pending = payments.filter(status='pending').aggregate(Sum('amount'))['amount__sum'] or 0
            total_overdue = payments.filter(status='overdue').aggregate(Sum('amount'))['amount__sum'] or 0
            
            return {
                'total_expected': float(total_expected),
                'total_collected': float(total_paid),
                'total_pending': float(total_pending),
                'total_overdue': float(total_overdue),
                'collection_rate': round((total_paid / total_expected * 100) if total_expected > 0 else 0, 2),
            }
        except Exception:
            return {
                'total_expected': 0,
                'total_collected': 0,
                'total_pending': 0,
                'total_overdue': 0,
                'collection_rate': 0,
            }
    
    @staticmethod
    def get_by_program() -> list:
        """Get fee collection by program"""
        try:
            from apps.finance.models import FeePayment
            
            stats = FeePayment.objects.values('student__program').annotate(
                total=Sum('amount'),
                paid=Sum('amount', filter=Q(status='paid'))
            )
            
            return list(stats)
        except Exception:
            return []
    
    @staticmethod
    def get_outstanding_fees() -> Dict[str, Any]:
        """Get outstanding fees summary"""
        try:
            from apps.finance.models import FeePayment
            from django.utils import timezone
            from datetime import timedelta
            
            now = timezone.now()
            overdue = FeePayment.objects.filter(
                status='pending',
                due_date__lt=now
            )
            
            return {
                'total_overdue': overdue.count(),
                'total_amount': float(overdue.aggregate(Sum('amount'))['amount__sum'] or 0),
            }
        except Exception:
            return {
                'total_overdue': 0,
                'total_amount': 0,
            }
