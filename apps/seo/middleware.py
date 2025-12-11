"""SEO Middleware for Redirects"""
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from .models import Redirect


class RedirectMiddleware:
    """Handle SEO redirects"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Get the current path
        path = request.path
        
        # Check for redirect
        try:
            redirect_obj = Redirect.objects.get(old_path=path, is_active=True)
            redirect_obj.increment_hits()
            
            # Return appropriate redirect
            if redirect_obj.redirect_type == '301':
                return HttpResponsePermanentRedirect(redirect_obj.new_path)
            elif redirect_obj.redirect_type == '302':
                return HttpResponseRedirect(redirect_obj.new_path)
            elif redirect_obj.redirect_type == '307':
                response = HttpResponse(status=307)
                response['Location'] = redirect_obj.new_path
                return response
            elif redirect_obj.redirect_type == '308':
                response = HttpResponse(status=308)
                response['Location'] = redirect_obj.new_path
                return response
        except Redirect.DoesNotExist:
            pass
        
        response = self.get_response(request)
        return response
