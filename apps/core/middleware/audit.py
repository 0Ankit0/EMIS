"""
Audit logging middleware and utilities
Records sensitive actions to AuditLog model
"""
from functools import wraps
from django.utils import timezone
from apps.authentication.models import AuditLog


def log_audit(action: str, actor=None, target_model: str = None, target_id: str = None,
              outcome: str = 'success', details: dict = None, request=None):
    """
    Create an audit log entry
    
    Args:
        action: Action performed (from AuditLog.ACTION_CHOICES)
        actor: User who performed the action
        target_model: Model name being acted upon
        target_id: ID of the target object
        outcome: Outcome of the action ('success', 'failure', 'denied')
        details: Additional context as dict
        request: HTTP request object (optional, for IP and user agent)
    """
    ip_address = None
    user_agent = ''
    
    if request:
        # Get client IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')
        
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]  # Limit length
    
    AuditLog.objects.create(
        actor=actor,
        action=action,
        target_model=target_model or '',
        target_id=str(target_id) if target_id else '',
        outcome=outcome,
        details=details or {},
        ip_address=ip_address,
        user_agent=user_agent,
    )


def audit_action(action: str, get_target_model=None, get_target_id=None):
    """
    Decorator to automatically audit a function/view
    
    Usage:
        @audit_action('create', get_target_model=lambda result: 'Student', get_target_id=lambda result: result.id)
        def create_student(request, data):
            ...
            return student
    
    Args:
        action: Action being performed
        get_target_model: Callable to extract target model from result
        get_target_id: Callable to extract target ID from result
    """
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            request = None
            actor = None
            
            # Try to extract request and user from arguments
            for arg in args:
                if hasattr(arg, 'user') and hasattr(arg, 'META'):
                    request = arg
                    actor = arg.user if arg.user.is_authenticated else None
                    break
            
            try:
                result = func(*args, **kwargs)
                
                target_model = get_target_model(result) if get_target_model else None
                target_id = get_target_id(result) if get_target_id else None
                
                log_audit(
                    action=action,
                    actor=actor,
                    target_model=target_model,
                    target_id=target_id,
                    outcome='success',
                    request=request,
                )
                
                return result
                
            except Exception as e:
                log_audit(
                    action=action,
                    actor=actor,
                    outcome='failure',
                    details={'error': str(e)},
                    request=request,
                )
                raise
        
        return wrapped
    return decorator


class AuditMiddleware:
    """
    Middleware to add audit logging helper to request
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Add audit logging method to request
        request.log_audit = lambda action, **kwargs: log_audit(
            action=action,
            actor=request.user if request.user.is_authenticated else None,
            request=request,
            **kwargs
        )
        
        response = self.get_response(request)
        
        # Log certain HTTP actions automatically
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            if response.status_code < 400:
                # Map HTTP methods to audit actions
                action_map = {
                    'POST': 'create',
                    'PUT': 'update',
                    'PATCH': 'update',
                    'DELETE': 'delete',
                }
                
                # Only log if path suggests it's a model operation
                if '/api/' in request.path:
                    log_audit(
                        action=action_map.get(request.method, 'update'),
                        actor=request.user if request.user.is_authenticated else None,
                        target_model=request.path.split('/api/')[-1].split('/')[0],
                        outcome='success',
                        request=request,
                    )
        
        return response
