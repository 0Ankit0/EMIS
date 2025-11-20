"""Attendance metrics service"""
from typing import Dict, Any
from django.db.models import Count, Avg, Q


class AttendanceMetricsService:
    """Service for calculating attendance metrics"""
    
    @staticmethod
    def calculate_rates() -> Dict[str, Any]:
        """Calculate attendance rates"""
        try:
            from apps.attendance.models import AttendanceRecord
            from django.utils import timezone
            from datetime import timedelta
            
            # Last 30 days
            end_date = timezone.now()
            start_date = end_date - timedelta(days=30)
            
            records = AttendanceRecord.objects.filter(
                date__gte=start_date,
                date__lte=end_date
            )
            
            total = records.count()
            present = records.filter(status='present').count()
            absent = records.filter(status='absent').count()
            late = records.filter(status='late').count()
            
            return {
                'total_records': total,
                'present': present,
                'absent': absent,
                'late': late,
                'attendance_rate': round((present / total * 100) if total > 0 else 0, 2),
            }
        except Exception:
            return {
                'total_records': 0,
                'present': 0,
                'absent': 0,
                'late': 0,
                'attendance_rate': 0,
            }
    
    @staticmethod
    def get_by_program() -> list:
        """Get attendance by program"""
        try:
            from apps.attendance.models import AttendanceRecord
            
            stats = AttendanceRecord.objects.values('student__program').annotate(
                total=Count('id'),
                present_count=Count('id', filter=Q(status='present'))
            )
            
            return list(stats)
        except Exception:
            return []
    
    @staticmethod
    def get_trends() -> list:
        """Get attendance trends"""
        try:
            from apps.attendance.models import AttendanceRecord
            from django.db.models.functions import TruncWeek
            
            trends = AttendanceRecord.objects.annotate(
                week=TruncWeek('date')
            ).values('week').annotate(
                total=Count('id'),
                present_count=Count('id', filter=Q(status='present'))
            ).order_by('week')
            
            return list(trends)
        except Exception:
            return []
