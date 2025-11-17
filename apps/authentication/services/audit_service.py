"""
Audit log service for querying and reporting
"""
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from apps.authentication.models import AuditLog


class AuditService:
    """Service for audit log operations"""
    
    @staticmethod
    def get_audit_logs(page=1, page_size=50, actor_id=None, action=None, 
                       outcome=None, target_model=None, date_from=None, date_to=None):
        """Get paginated audit logs with filters"""
        queryset = AuditLog.objects.select_related('actor')
        
        # Apply filters
        if actor_id:
            queryset = queryset.filter(actor_id=actor_id)
        
        if action:
            queryset = queryset.filter(action=action)
        
        if outcome:
            queryset = queryset.filter(outcome=outcome)
        
        if target_model:
            queryset = queryset.filter(target_model=target_model)
        
        if date_from:
            queryset = queryset.filter(timestamp__gte=date_from)
        
        if date_to:
            queryset = queryset.filter(timestamp__lte=date_to)
        
        # Order by most recent first
        queryset = queryset.order_by('-timestamp')
        
        # Pagination
        offset = (page - 1) * page_size
        total = queryset.count()
        logs = list(queryset[offset:offset + page_size])
        
        return {
            'logs': logs,
            'total': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size
        }
    
    @staticmethod
    def get_user_activity(user_id, days=30):
        """Get user activity summary for the last N days"""
        since = timezone.now() - timedelta(days=days)
        
        logs = AuditLog.objects.filter(
            actor_id=user_id,
            timestamp__gte=since
        )
        
        # Count by action
        action_counts = logs.values('action').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Count by outcome
        outcome_counts = logs.values('outcome').annotate(
            count=Count('id')
        )
        
        # Recent activity
        recent_logs = logs.order_by('-timestamp')[:20]
        
        return {
            'total_actions': logs.count(),
            'action_breakdown': list(action_counts),
            'outcome_breakdown': list(outcome_counts),
            'recent_activity': list(recent_logs),
            'period_days': days
        }
    
    @staticmethod
    def get_failed_login_attempts(username=None, hours=24):
        """Get failed login attempts in the last N hours"""
        since = timezone.now() - timedelta(hours=hours)
        
        queryset = AuditLog.objects.filter(
            action='failed_login',
            outcome='failure',
            timestamp__gte=since
        )
        
        if username:
            queryset = queryset.filter(details__username=username)
        
        return queryset.order_by('-timestamp')
    
    @staticmethod
    def get_security_events(hours=24):
        """Get security-related events"""
        since = timezone.now() - timedelta(hours=hours)
        
        security_actions = ['failed_login', 'permission_change', 'role_change']
        
        events = AuditLog.objects.filter(
            action__in=security_actions,
            timestamp__gte=since
        ).select_related('actor').order_by('-timestamp')
        
        return {
            'events': list(events),
            'total': events.count(),
            'failed_logins': events.filter(action='failed_login').count(),
            'permission_changes': events.filter(action='permission_change').count(),
            'role_changes': events.filter(action='role_change').count()
        }
