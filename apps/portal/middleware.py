from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .models import PortalActivity


class PortalActivityMiddleware(MiddlewareMixin):
    """Middleware to log portal activities"""
    
    def process_request(self, request):
        if request.user.is_authenticated and request.path.startswith('/portal/'):
            # Log page view
            PortalActivity.objects.create(
                user=request.user,
                activity_type='view_page',
                description=f'Viewed {request.path}',
                metadata={'path': request.path, 'method': request.method},
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:500]
            )
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
