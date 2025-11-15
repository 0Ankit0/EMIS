"""
Authentication views - Frontend
"""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def login_view(request):
    """Login page"""
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'core:dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'authentication/login.html')


def register_view(request):
    """Registration page"""
    if request.method == 'POST':
        # Handle registration
        pass
    
    return render(request, 'authentication/register.html')


def password_reset_view(request):
    """Password reset page"""
    return render(request, 'authentication/password_reset.html')


@login_required
def password_change_view(request):
    """Password change page"""
    return render(request, 'authentication/password_change.html')


@login_required
def profile_view(request):
    """User profile page"""
    return render(request, 'authentication/profile.html')


@login_required
def setup_2fa_view(request):
    """2FA setup page"""
    return render(request, 'authentication/setup_2fa.html')
