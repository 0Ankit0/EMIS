"""
Secure Authentication Views with Industry-Level Security
"""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
import json

from .models import (
    User, LoginAttempt, PasswordResetToken, UserSession, SecurityLog
)
from .security_utils import (
    PasswordValidator, RateLimiter, IPSecurityChecker,
    SessionSecurityManager, TwoFactorAuthManager, AuditLogger,
    get_client_ip, get_user_agent, generate_secure_token
)
from .forms import (
    LoginForm, RegisterForm, PasswordResetRequestForm,
    PasswordResetForm, TwoFactorForm, ChangePasswordForm
)


# ============================================================================
# Login Views
# ============================================================================

@csrf_protect
@require_http_methods(["GET", "POST"])
def login_view(request):
    """
    Secure login with rate limiting, 2FA, and security monitoring
    """
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    
    ip_address = get_client_ip(request)
    user_agent = get_user_agent(request)
    
    # Check if IP is blacklisted
    if IPSecurityChecker.is_ip_blacklisted(ip_address):
        messages.error(request, 'Access denied from this IP address.')
        return render(request, 'authentication/login.html')
    
    # Check rate limiting
    is_allowed, remaining, reset_time = RateLimiter.check_rate_limit(
        ip_address, 'login', max_attempts=5, window_minutes=15
    )
    
    if not is_allowed:
        messages.error(
            request,
            f'Too many login attempts. Please try again after {reset_time.strftime("%H:%M:%S")}'
        )
        return render(request, 'authentication/login.html')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data.get('remember_me', False)
            
            # Authenticate user
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                # Check if account is locked
                if user.is_account_locked():
                    LoginAttempt.objects.create(
                        user=user,
                        email=email,
                        ip_address=ip_address,
                        user_agent=user_agent,
                        success=False,
                        failure_reason='account_locked'
                    )
                    messages.error(request, 'Your account is temporarily locked. Please try again later.')
                    return render(request, 'authentication/login.html', {'form': form})
                
                # Check if account is active
                if user.account_status != 'active':
                    LoginAttempt.objects.create(
                        user=user,
                        email=email,
                        ip_address=ip_address,
                        user_agent=user_agent,
                        success=False,
                        failure_reason='account_inactive'
                    )
                    messages.error(request, f'Account is {user.account_status}. Please contact support.')
                    return render(request, 'authentication/login.html', {'form': form})
                
                # Check if 2FA is enabled
                if user.two_factor_enabled:
                    # Store user ID in session for 2FA verification
                    request.session['2fa_user_id'] = str(user.id)
                    request.session['2fa_ip'] = ip_address
                    
                    LoginAttempt.objects.create(
                        user=user,
                        email=email,
                        ip_address=ip_address,
                        user_agent=user_agent,
                        success=False,
                        two_factor_required=True
                    )
                    
                    return redirect('authentication:verify_2fa')
                
                # Successful login
                return complete_login(request, user, remember_me)
                
            else:
                # Failed login
                try:
                    failed_user = User.objects.get(email=email)
                    failed_user.record_failed_login()
                except User.DoesNotExist:
                    failed_user = None
                
                LoginAttempt.objects.create(
                    user=failed_user,
                    email=email,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    success=False,
                    failure_reason='invalid_credentials'
                )
                
                messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LoginForm()
    
    context = {
        'form': form,
        'remaining_attempts': remaining
    }
    
    return render(request, 'authentication/login.html', context)


def complete_login(request, user, remember_me=False):
    """Complete the login process"""
    ip_address = get_client_ip(request)
    user_agent = get_user_agent(request)
    
    # Check for suspicious activity
    is_suspicious, reason = SessionSecurityManager.detect_session_hijacking(
        user, ip_address, user_agent
    )
    
    if is_suspicious:
        # Log security event
        AuditLogger.log_security_event(
            user=user,
            event_type='suspicious_activity',
            severity='warning',
            description=f'Suspicious login detected: {reason}',
            ip_address=ip_address,
            user_agent=user_agent,
            risk_score=60
        )
        
        # Still allow login but send notification
        # send_security_alert_email(user, reason)
    
    # Login user
    auth_login(request, user)
    
    # Update user info
    user.last_login_ip = ip_address
    user.last_login_user_agent = user_agent
    user.last_activity_at = timezone.now()
    user.reset_failed_logins()
    user.save(update_fields=[
        'last_login_ip', 'last_login_user_agent',
        'last_activity_at', 'failed_login_attempts'
    ])
    
    # Create session record
    session_expires = timezone.now() + timedelta(days=30 if remember_me else 1)
    UserSession.objects.create(
        user=user,
        session_key=request.session.session_key,
        ip_address=ip_address,
        user_agent=user_agent,
        expires_at=session_expires
    )
    
    # Log successful login
    LoginAttempt.objects.create(
        user=user,
        email=user.email,
        ip_address=ip_address,
        user_agent=user_agent,
        success=True
    )
    
    AuditLogger.log_security_event(
        user=user,
        event_type='login',
        severity='info',
        description='Successful login',
        ip_address=ip_address,
        user_agent=user_agent
    )
    
    # Reset rate limit
    RateLimiter.reset_rate_limit(ip_address, 'login')
    
    # Set session expiry
    if remember_me:
        request.session.set_expiry(2592000)  # 30 days
    else:
        request.session.set_expiry(0)  # Browser close
    
    messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
    
    # Redirect to next page or dashboard
    next_url = request.GET.get('next', 'core:dashboard')
    return redirect(next_url)


@csrf_protect
@require_http_methods(["GET", "POST"])
def verify_2fa(request):
    """Verify 2FA token"""
    user_id = request.session.get('2fa_user_id')
    session_ip = request.session.get('2fa_ip')
    current_ip = get_client_ip(request)
    
    if not user_id or session_ip != current_ip:
        messages.error(request, 'Invalid 2FA session.')
        return redirect('authentication:login')
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('authentication:login')
    
    if request.method == 'POST':
        form = TwoFactorForm(request.POST)
        
        if form.is_valid():
            token = form.cleaned_data['token']
            use_backup = form.cleaned_data.get('use_backup_code', False)
            
            is_valid = False
            
            if use_backup:
                is_valid = TwoFactorAuthManager.verify_backup_code(user, token)
            else:
                is_valid = user.verify_2fa_token(token)
            
            if is_valid:
                # Clear 2FA session data
                del request.session['2fa_user_id']
                del request.session['2fa_ip']
                
                # Update login attempt
                LoginAttempt.objects.filter(
                    user=user,
                    ip_address=current_ip
                ).order_by('-attempted_at').first().update(
                    two_factor_verified=True
                )
                
                # Complete login
                remember_me = request.POST.get('remember_me', False)
                return complete_login(request, user, remember_me)
            else:
                messages.error(request, 'Invalid 2FA token. Please try again.')
        else:
            messages.error(request, 'Please enter a valid token.')
    else:
        form = TwoFactorForm()
    
    return render(request, 'authentication/verify_2fa.html', {'form': form})


# ============================================================================
# Registration Views
# ============================================================================

@csrf_protect
@require_http_methods(["GET", "POST"])
def register_view(request):
    """User registration with email verification"""
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    
    ip_address = get_client_ip(request)
    
    # Check rate limiting
    is_allowed, remaining, reset_time = RateLimiter.check_rate_limit(
        ip_address, 'register', max_attempts=3, window_minutes=60
    )
    
    if not is_allowed:
        messages.error(request, 'Too many registration attempts. Please try again later.')
        return render(request, 'authentication/register.html')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            
            # Validate password strength
            is_valid, errors, strength = PasswordValidator.validate_strength(password)
            
            if not is_valid:
                for error in errors:
                    messages.error(request, error)
                return render(request, 'authentication/register.html', {'form': form})
            
            # Check if password is pwned
            pwned_count = PasswordValidator.check_pwned_password(password)
            if pwned_count > 0:
                messages.warning(
                    request,
                    f'This password has appeared in {pwned_count} data breaches. Please choose a different password.'
                )
                return render(request, 'authentication/register.html', {'form': form})
            
            # Create user
            user = User.objects.create_user(
                email=email,
                username=username,
                password=password,
                first_name=form.cleaned_data.get('first_name', ''),
                last_name=form.cleaned_data.get('last_name', ''),
                account_status='pending'
            )
            
            # Generate email verification token
            user.email_verification_token = generate_secure_token()
            user.email_verification_sent_at = timezone.now()
            user.save()
            
            # Send verification email
            # send_verification_email(user)
            
            # Log security event
            AuditLogger.log_security_event(
                user=user,
                event_type='registration',
                severity='info',
                description='New user registration',
                ip_address=ip_address
            )
            
            messages.success(
                request,
                'Registration successful! Please check your email to verify your account.'
            )
            return redirect('authentication:login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()
    
    return render(request, 'authentication/register.html', {'form': form})


# ============================================================================
# Password Reset Views
# ============================================================================

@csrf_protect
@require_http_methods(["GET", "POST"])
def password_reset_request(request):
    """Request password reset"""
    ip_address = get_client_ip(request)
    
    # Rate limiting
    is_allowed, remaining, reset_time = RateLimiter.check_rate_limit(
        ip_address, 'password_reset', max_attempts=3, window_minutes=60
    )
    
    if not is_allowed:
        messages.error(request, 'Too many password reset requests. Please try again later.')
        return render(request, 'authentication/password_reset_request.html')
    
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            
            try:
                user = User.objects.get(email=email)
                
                # Create password reset token
                token = PasswordResetToken.create_token(
                    user=user,
                    ip_address=ip_address,
                    user_agent=get_user_agent(request),
                    expiry_hours=1
                )
                
                # Send reset email
                # send_password_reset_email(user, token)
                
                # Log security event
                AuditLogger.log_security_event(
                    user=user,
                    event_type='password_reset',
                    severity='info',
                    description='Password reset requested',
                    ip_address=ip_address
                )
                
            except User.DoesNotExist:
                # Don't reveal if user exists
                pass
            
            messages.success(
                request,
                'If an account exists with that email, you will receive password reset instructions.'
            )
            return redirect('authentication:login')
        else:
            messages.error(request, 'Please enter a valid email address.')
    else:
        form = PasswordResetRequestForm()
    
    return render(request, 'authentication/password_reset_request.html', {'form': form})


@csrf_protect
@require_http_methods(["GET", "POST"])
def password_reset_confirm(request, token):
    """Confirm password reset with token"""
    try:
        reset_token = PasswordResetToken.objects.get(token=token)
        
        if not reset_token.is_valid():
            messages.error(request, 'This password reset link has expired or been used.')
            return redirect('authentication:password_reset_request')
        
        if request.method == 'POST':
            form = PasswordResetForm(request.POST)
            
            if form.is_valid():
                password = form.cleaned_data['password1']
                
                # Validate password
                is_valid, errors, strength = PasswordValidator.validate_strength(password)
                
                if not is_valid:
                    for error in errors:
                        messages.error(request, error)
                    return render(request, 'authentication/password_reset_confirm.html', {'form': form})
                
                # Update password
                user = reset_token.user
                user.set_password(password)
                user.password_changed_at = timezone.now()
                user.password_reset_required = False
                user.save()
                
                # Mark token as used
                reset_token.is_used = True
                reset_token.used_at = timezone.now()
                reset_token.save()
                
                # Terminate all sessions
                SessionSecurityManager.terminate_all_sessions(user)
                
                # Log security event
                AuditLogger.log_security_event(
                    user=user,
                    event_type='password_change',
                    severity='warning',
                    description='Password changed via reset',
                    ip_address=get_client_ip(request)
                )
                
                messages.success(request, 'Your password has been reset successfully. Please login.')
                return redirect('authentication:login')
            else:
                messages.error(request, 'Please correct the errors below.')
        else:
            form = PasswordResetForm()
        
        return render(request, 'authentication/password_reset_confirm.html', {'form': form})
        
    except PasswordResetToken.DoesNotExist:
        messages.error(request, 'Invalid password reset link.')
        return redirect('authentication:password_reset_request')


# ============================================================================
# Logout View
# ============================================================================

@login_required
def logout_view(request):
    """Secure logout"""
    user = request.user
    ip_address = get_client_ip(request)
    
    # Deactivate current session
    try:
        UserSession.objects.filter(
            user=user,
            session_key=request.session.session_key
        ).update(is_active=False)
    except Exception:
        pass
    
    # Log security event
    AuditLogger.log_security_event(
        user=user,
        event_type='logout',
        severity='info',
        description='User logged out',
        ip_address=ip_address
    )
    
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('authentication:login')


# ============================================================================
# 2FA Management Views
# ============================================================================

@login_required
@require_http_methods(["GET", "POST"])
def setup_2fa(request):
    """Setup 2FA for user account"""
    user = request.user
    
    if request.method == 'POST':
        token = request.POST.get('token')
        
        if user.verify_2fa_token(token):
            user.two_factor_enabled = True
            backup_codes = user.generate_backup_codes()
            user.save()
            
            # Log security event
            AuditLogger.log_security_event(
                user=user,
                event_type='2fa_enabled',
                severity='info',
                description='2FA enabled',
                ip_address=get_client_ip(request)
            )
            
            return render(request, 'authentication/2fa_backup_codes.html', {
                'backup_codes': backup_codes
            })
        else:
            messages.error(request, 'Invalid token. Please try again.')
    
    # Generate QR code
    qr_code = TwoFactorAuthManager.generate_qr_code(user)
    
    return render(request, 'authentication/setup_2fa.html', {
        'qr_code': qr_code,
        'secret': user.two_factor_secret
    })


@login_required
@require_http_methods(["POST"])
def disable_2fa(request):
    """Disable 2FA"""
    user = request.user
    password = request.POST.get('password')
    
    # Verify password
    if user.check_password(password):
        user.two_factor_enabled = False
        user.two_factor_secret = None
        user.backup_codes = []
        user.save()
        
        # Log security event
        AuditLogger.log_security_event(
            user=user,
            event_type='2fa_disabled',
            severity='warning',
            description='2FA disabled',
            ip_address=get_client_ip(request),
            risk_score=50
        )
        
        messages.success(request, '2FA has been disabled.')
    else:
        messages.error(request, 'Invalid password.')
    
    return redirect('authentication:security_settings')


# ============================================================================
# Security Settings
# ============================================================================

@login_required
def security_settings(request):
    """User security settings page"""
    user = request.user
    
    # Get active sessions
    active_sessions = UserSession.objects.filter(
        user=user,
        is_active=True
    ).order_by('-last_activity')
    
    # Get recent login attempts
    recent_logins = LoginAttempt.objects.filter(
        user=user
    ).order_by('-attempted_at')[:10]
    
    # Get security summary
    security_summary = AuditLogger.get_user_security_summary(user, days=30)
    
    context = {
        'active_sessions': active_sessions,
        'recent_logins': recent_logins,
        'security_summary': security_summary,
        '2fa_enabled': user.two_factor_enabled,
    }
    
    return render(request, 'authentication/security_settings.html', context)


@login_required
@require_http_methods(["POST"])
def terminate_session(request, session_id):
    """Terminate a specific session"""
    user = request.user
    
    try:
        session = UserSession.objects.get(id=session_id, user=user)
        session.is_active = False
        session.save()
        
        messages.success(request, 'Session terminated successfully.')
    except UserSession.DoesNotExist:
        messages.error(request, 'Session not found.')
    
    return redirect('authentication:security_settings')


@login_required
@require_http_methods(["POST"])
def terminate_all_sessions(request):
    """Terminate all other sessions"""
    user = request.user
    current_session = request.session.session_key
    
    SessionSecurityManager.terminate_all_sessions(user, except_current=current_session)
    
    messages.success(request, 'All other sessions have been terminated.')
    return redirect('authentication:security_settings')
