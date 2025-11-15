"""
Core views
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def home(request):
    """Home page - redirect to dashboard if logged in"""
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    return render(request, 'core/home.html')


@login_required
def dashboard(request):
    """Main dashboard - role-based redirect"""
    user = request.user
    
    # Redirect based on user role
    if hasattr(user, 'student_profile'):
        return redirect('students:dashboard')
    elif hasattr(user, 'faculty_profile'):
        return redirect('faculty:dashboard')
    elif user.is_staff:
        return redirect('hr:dashboard')
    
    return render(request, 'core/dashboard.html')
