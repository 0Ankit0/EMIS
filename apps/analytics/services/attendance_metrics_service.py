"""Attendance metrics service"""
from typing import Dict, Any
from django.db.models import Count, Avg, Q
from apps.students.models import AttendanceRecord


class AttendanceMetricsService:
    """Service for calculating attendance metrics"""
    
    @staticmethod
    def calculate_rates() -> Dict[str, Any]:
        """Calculate attendance rate metrics"""
        records = AttendanceRecord.objects.all()
        
        total = records.count()
        present = records.filter(status='present').count()
        absent = records.filter(status='absent').count()
        late = records.filter(status='late').count()
        
        attendance_rate = round((present / total * 100) if total > 0 else 0, 2)
        
        return {
            'total_records': total,
            'present': present,
            'absent': absent,
            'late': late,
            'attendance_rate': attendance_rate,
            'absence_rate': round((absent / total * 100) if total > 0 else 0, 2),
        }
