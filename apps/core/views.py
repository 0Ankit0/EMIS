"""
Core views
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .permissions_utils import get_user_modules


def home(request):
    """Home page - redirect to dashboard if logged in, otherwise to login"""
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    return redirect('authentication:login')


@login_required
def dashboard(request):
    """Main dashboard - role-based modules display"""
    user = request.user
    
    # Get modules based on user's roles
    modules = get_user_modules(user)
    
    context = {
        'modules': modules,
        'user': user,
    }
    
    return render(request, 'core/dashboard.html', context)
