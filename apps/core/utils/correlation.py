"""
Correlation ID generation and tracking utilities
"""
import uuid
from contextvars import ContextVar

# Context variable to store correlation ID for the current request
correlation_id_var: ContextVar[str] = ContextVar('correlation_id', default=None)


def generate_correlation_id() -> str:
    """Generate a new correlation ID"""
    return str(uuid.uuid4())


def get_correlation_id() -> str:
    """Get the current correlation ID or generate a new one"""
    correlation_id = correlation_id_var.get()
    if not correlation_id:
        correlation_id = generate_correlation_id()
        set_correlation_id(correlation_id)
    return correlation_id


def set_correlation_id(correlation_id: str):
    """Set the correlation ID for the current context"""
    correlation_id_var.set(correlation_id)


def clear_correlation_id():
    """Clear the current correlation ID"""
    correlation_id_var.set(None)


class CorrelationIDMiddleware:
    """
    Middleware to generate and track correlation IDs across requests
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Generate or use provided correlation ID
        correlation_id = request.META.get('HTTP_X_CORRELATION_ID') or generate_correlation_id()
        
        # Set in context
        set_correlation_id(correlation_id)
        
        # Add to request
        request.correlation_id = correlation_id
        
        # Get response
        response = self.get_response(request)
        
        # Add correlation ID to response headers
        response['X-Correlation-ID'] = correlation_id
        
        # Clear context
        clear_correlation_id()
        
        return response
