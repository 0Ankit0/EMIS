"""
Global error handling middleware for EMIS
Formats all errors with MODULE_ERROR_CODE, message, and correlation_id
"""
import uuid
import logging
import traceback
from django.http import JsonResponse
from django.core.exceptions import ValidationError, PermissionDenied, ObjectDoesNotExist
from rest_framework.exceptions import APIException
from rest_framework import status
from django.conf import settings

from apps.core.exceptions import EMISException
from apps.core.error_codes import get_error_message

logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware:
    """Middleware to handle and format all errors consistently"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Add correlation ID to request
        correlation_id = str(uuid.uuid4())
        request.correlation_id = correlation_id
        
        try:
            response = self.get_response(request)
            return response
        except Exception as exc:
            return self.handle_exception(request, exc, correlation_id)
    
    def handle_exception(self, request, exc, correlation_id):
        """Handle different types of exceptions and return consistent error response"""
        
        # Log the error
        logger.error(
            f"Error occurred: {str(exc)}",
            extra={
                'correlation_id': correlation_id,
                'path': request.path,
                'method': request.method,
                'user': request.user.username if request.user.is_authenticated else 'anonymous',
            },
            exc_info=True
        )
        
        # Handle EMIS custom exceptions
        if isinstance(exc, EMISException):
            return JsonResponse({
                'error': {
                    'code': exc.code,
                    'message': exc.message,
                    'details': exc.details,
                    'correlation_id': correlation_id,
                }
            }, status=self._get_status_code(exc.code))
        
        # Handle Django validation errors
        if isinstance(exc, ValidationError):
            return JsonResponse({
                'error': {
                    'code': 'CORE_001',
                    'message': 'Validation error',
                    'details': {'validation_errors': exc.message_dict if hasattr(exc, 'message_dict') else str(exc)},
                    'correlation_id': correlation_id,
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Handle permission denied
        if isinstance(exc, PermissionDenied):
            return JsonResponse({
                'error': {
                    'code': 'AUTH_002',
                    'message': 'Permission denied',
                    'details': {'reason': str(exc)},
                    'correlation_id': correlation_id,
                }
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Handle object not found
        if isinstance(exc, ObjectDoesNotExist):
            return JsonResponse({
                'error': {
                    'code': 'CORE_002',
                    'message': 'Resource not found',
                    'details': {'resource': str(exc)},
                    'correlation_id': correlation_id,
                }
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Handle DRF API exceptions
        if isinstance(exc, APIException):
            return JsonResponse({
                'error': {
                    'code': getattr(exc, 'default_code', 'CORE_000').upper(),
                    'message': exc.detail if isinstance(exc.detail, str) else str(exc.detail),
                    'details': {},
                    'correlation_id': correlation_id,
                }
            }, status=exc.status_code)
        
        # Handle all other exceptions
        return JsonResponse({
            'error': {
                'code': 'CORE_000',
                'message': 'An unexpected error occurred',
                'details': {'error_type': type(exc).__name__} if settings.DEBUG else {},
                'correlation_id': correlation_id,
            }
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _get_status_code(self, error_code):
        """Map error codes to HTTP status codes"""
        if error_code.startswith('AUTH_'):
            if error_code in ['AUTH_001', 'AUTH_003', 'AUTH_004', 'AUTH_009']:
                return status.HTTP_401_UNAUTHORIZED
            return status.HTTP_403_FORBIDDEN
        
        if error_code.startswith('CORE_002') or error_code.endswith('_NOT_FOUND'):
            return status.HTTP_404_NOT_FOUND
        
        if error_code.startswith('CORE_001') or 'INVALID' in error_code:
            return status.HTTP_400_BAD_REQUEST
        
        if error_code == 'CORE_007':  # Rate limit
            return status.HTTP_429_TOO_MANY_REQUESTS
        
        if error_code == 'CORE_008':  # Timeout
            return status.HTTP_504_GATEWAY_TIMEOUT
        
        return status.HTTP_500_INTERNAL_SERVER_ERROR
