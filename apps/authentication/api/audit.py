"""Audit log API endpoints"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from apps.authentication.services.audit_service import AuditService
from apps.core.middleware.rbac import require_permission

User = get_user_model()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@require_permission('audit', 'view')
def list_audit_logs(request):
    """Get paginated audit logs with filters"""
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 50))
    actor_id = request.GET.get('actor_id')
    action = request.GET.get('action')
    outcome = request.GET.get('outcome')
    target_model = request.GET.get('target_model')
    
    result = AuditService.get_audit_logs(
        page=page,
        page_size=page_size,
        actor_id=actor_id,
        action=action,
        outcome=outcome,
        target_model=target_model
    )
    
    # Serialize logs
    logs_data = [
        {
            'id': str(log.id),
            'actor': log.actor.username if log.actor else None,
            'action': log.action,
            'target_model': log.target_model,
            'target_id': log.target_id,
            'outcome': log.outcome,
            'details': log.details,
            'ip_address': log.ip_address,
            'timestamp': log.timestamp.isoformat()
        }
        for log in result['logs']
    ]
    
    return Response({
        'results': logs_data,
        'page_info': {
            'total': result['total'],
            'page': result['page'],
            'page_size': result['page_size'],
            'total_pages': result['total_pages']
        }
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@require_permission('audit', 'view')
def user_activity(request, user_id):
    """Get user activity summary"""
    days = int(request.GET.get('days', 30))
    
    activity = AuditService.get_user_activity(user_id, days=days)
    
    # Serialize recent activity
    recent_logs = [
        {
            'action': log.action,
            'target_model': log.target_model,
            'outcome': log.outcome,
            'timestamp': log.timestamp.isoformat()
        }
        for log in activity['recent_activity']
    ]
    
    return Response({
        'total_actions': activity['total_actions'],
        'action_breakdown': activity['action_breakdown'],
        'outcome_breakdown': activity['outcome_breakdown'],
        'recent_activity': recent_logs,
        'period_days': activity['period_days']
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@require_permission('audit', 'view')
def security_events(request):
    """Get recent security events"""
    hours = int(request.GET.get('hours', 24))
    
    events = AuditService.get_security_events(hours=hours)
    
    # Serialize events
    events_data = [
        {
            'id': str(event.id),
            'actor': event.actor.username if event.actor else 'System',
            'action': event.action,
            'target_model': event.target_model,
            'outcome': event.outcome,
            'details': event.details,
            'ip_address': event.ip_address,
            'timestamp': event.timestamp.isoformat()
        }
        for event in events['events']
    ]
    
    return Response({
        'events': events_data,
        'summary': {
            'total': events['total'],
            'failed_logins': events['failed_logins'],
            'permission_changes': events['permission_changes'],
            'role_changes': events['role_changes']
        },
        'period_hours': hours
    })
