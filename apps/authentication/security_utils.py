"""
Advanced Security Utilities for Authentication
"""
import hashlib
import hmac
import secrets
import re
from datetime import timedelta
from django.utils import timezone
from django.core.cache import cache
from django.conf import settings
import ipaddress


class PasswordValidator:
    """Enhanced password validation"""
    
    MIN_LENGTH = 12
    
    @staticmethod
    def validate_strength(password):
        """
        Validate password strength
        Returns: (is_valid, errors, strength_score)
        """
        errors = []
        score = 0
        
        # Length check
        if len(password) < PasswordValidator.MIN_LENGTH:
            errors.append(f"Password must be at least {PasswordValidator.MIN_LENGTH} characters long")
        else:
            score += min(len(password) - PasswordValidator.MIN_LENGTH, 10)
        
        # Uppercase check
        if not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter")
        else:
            score += 10
        
        # Lowercase check
        if not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter")
        else:
            score += 10
        
        # Digit check
        if not re.search(r'\d', password):
            errors.append("Password must contain at least one digit")
        else:
            score += 10
        
        # Special character check
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("Password must contain at least one special character")
        else:
            score += 15
        
        # Common password check
        common_passwords = [
            'password', '12345678', 'qwerty', 'abc123', 
            'password123', 'admin', 'letmein'
        ]
        if password.lower() in common_passwords:
            errors.append("Password is too common")
            score = max(0, score - 50)
        
        # Sequential characters
        if re.search(r'(012|123|234|345|456|567|678|789|abc|bcd|cde)', password.lower()):
            score -= 5
        
        # Repeated characters
        if re.search(r'(.)\1{2,}', password):
            score -= 5
        
        is_valid = len(errors) == 0
        strength_score = max(0, min(100, score))
        
        return is_valid, errors, strength_score
    
    @staticmethod
    def check_pwned_password(password):
        """
        Check if password has been pwned using Have I Been Pwned API
        Returns count of times password has been seen in breaches
        """
        import requests
        
        # Hash password with SHA-1
        sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
        prefix = sha1[:5]
        suffix = sha1[5:]
        
        try:
            url = f"https://api.pwnedpasswords.com/range/{prefix}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                hashes = response.text.split('\r\n')
                for h in hashes:
                    hash_suffix, count = h.split(':')
                    if hash_suffix == suffix:
                        return int(count)
        except Exception:
            # If API is unavailable, don't block user
            pass
        
        return 0


class RateLimiter:
    """Advanced rate limiting"""
    
    @staticmethod
    def check_rate_limit(identifier, action, max_attempts=5, window_minutes=15):
        """
        Check if action is rate limited
        Returns: (is_allowed, remaining_attempts, reset_time)
        """
        cache_key = f"rate_limit:{action}:{identifier}"
        
        attempts = cache.get(cache_key, 0)
        
        if attempts >= max_attempts:
            ttl = cache.ttl(cache_key)
            reset_time = timezone.now() + timedelta(seconds=ttl if ttl else 0)
            return False, 0, reset_time
        
        # Increment counter
        cache.set(cache_key, attempts + 1, window_minutes * 60)
        
        remaining = max_attempts - (attempts + 1)
        reset_time = timezone.now() + timedelta(minutes=window_minutes)
        
        return True, remaining, reset_time
    
    @staticmethod
    def reset_rate_limit(identifier, action):
        """Reset rate limit for identifier"""
        cache_key = f"rate_limit:{action}:{identifier}"
        cache.delete(cache_key)


class IPSecurityChecker:
    """IP-based security checks"""
    
    # Known malicious IP ranges (example)
    BLACKLISTED_RANGES = [
        # Add known malicious IP ranges
    ]
    
    WHITELISTED_RANGES = [
        # Add trusted IP ranges
    ]
    
    @staticmethod
    def is_ip_blacklisted(ip_address):
        """Check if IP is blacklisted"""
        try:
            ip = ipaddress.ip_address(ip_address)
            
            # Check against blacklisted ranges
            for range_str in IPSecurityChecker.BLACKLISTED_RANGES:
                network = ipaddress.ip_network(range_str)
                if ip in network:
                    return True
            
            # Check cache for temporarily blocked IPs
            cache_key = f"blocked_ip:{ip_address}"
            if cache.get(cache_key):
                return True
            
            return False
        except ValueError:
            return False
    
    @staticmethod
    def is_ip_whitelisted(ip_address):
        """Check if IP is whitelisted"""
        try:
            ip = ipaddress.ip_address(ip_address)
            
            for range_str in IPSecurityChecker.WHITELISTED_RANGES:
                network = ipaddress.ip_network(range_str)
                if ip in network:
                    return True
            
            return False
        except ValueError:
            return False
    
    @staticmethod
    def block_ip(ip_address, duration_hours=24):
        """Temporarily block an IP address"""
        cache_key = f"blocked_ip:{ip_address}"
        cache.set(cache_key, True, duration_hours * 3600)
    
    @staticmethod
    def check_suspicious_ip_activity(ip_address, threshold=10):
        """
        Check for suspicious activity from IP
        Returns: (is_suspicious, activity_count)
        """
        cache_key = f"ip_activity:{ip_address}"
        
        activity_count = cache.get(cache_key, 0)
        
        if activity_count >= threshold:
            return True, activity_count
        
        # Increment counter (1 hour window)
        cache.set(cache_key, activity_count + 1, 3600)
        
        return False, activity_count + 1


class SessionSecurityManager:
    """Manage session security"""
    
    @staticmethod
    def generate_session_token():
        """Generate cryptographically secure session token"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def validate_session_token(token, expected_token):
        """Safely compare session tokens (timing attack resistant)"""
        return hmac.compare_digest(token, expected_token)
    
    @staticmethod
    def detect_session_hijacking(user, current_ip, current_user_agent):
        """
        Detect potential session hijacking
        Returns: (is_suspicious, reason)
        """
        from apps.authentication.models import UserSession
        
        # Get user's last session
        last_session = UserSession.objects.filter(
            user=user,
            is_active=True
        ).order_by('-last_activity').first()
        
        if not last_session:
            return False, None
        
        # Check IP change
        if last_session.ip_address != current_ip:
            # Check if IPs are in same subnet
            try:
                last_ip = ipaddress.ip_address(last_session.ip_address)
                curr_ip = ipaddress.ip_address(current_ip)
                
                # If IPs are very different, flag as suspicious
                if last_ip.version != curr_ip.version:
                    return True, "IP version changed"
                
                # Check if in different countries (would need GeoIP)
                # For now, just flag significant IP changes
                
            except ValueError:
                pass
        
        # Check user agent change
        if last_session.user_agent and current_user_agent:
            if last_session.user_agent != current_user_agent:
                return True, "User agent changed"
        
        return False, None
    
    @staticmethod
    def terminate_all_sessions(user, except_current=None):
        """Terminate all active sessions for user"""
        from apps.authentication.models import UserSession
        
        sessions = UserSession.objects.filter(user=user, is_active=True)
        
        if except_current:
            sessions = sessions.exclude(id=except_current)
        
        sessions.update(is_active=False)


class TwoFactorAuthManager:
    """Manage 2FA operations"""
    
    @staticmethod
    def generate_qr_code(user):
        """Generate QR code for 2FA setup"""
        import pyotp
        import qrcode
        from io import BytesIO
        import base64
        
        if not user.two_factor_secret:
            user.generate_2fa_secret()
        
        # Generate provisioning URI
        totp = pyotp.TOTP(user.two_factor_secret)
        provisioning_uri = totp.provisioning_uri(
            name=user.email,
            issuer_name="EMIS"
        )
        
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(provisioning_uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    
    @staticmethod
    def verify_backup_code(user, code):
        """Verify and consume a backup code"""
        hashed_code = hashlib.sha256(code.encode()).hexdigest()
        
        if hashed_code in user.backup_codes:
            user.backup_codes.remove(hashed_code)
            user.save(update_fields=['backup_codes'])
            return True
        
        return False


class CSRFProtection:
    """Enhanced CSRF protection"""
    
    @staticmethod
    def generate_csrf_token():
        """Generate CSRF token"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def validate_csrf_token(token, expected_token):
        """Validate CSRF token"""
        return hmac.compare_digest(token, expected_token)


class AuditLogger:
    """Security audit logging"""
    
    @staticmethod
    def log_security_event(
        user=None,
        event_type='',
        severity='info',
        description='',
        ip_address=None,
        user_agent='',
        metadata=None,
        risk_score=0
    ):
        """Log security event"""
        from apps.authentication.models import SecurityLog
        
        SecurityLog.objects.create(
            user=user,
            event_type=event_type,
            severity=severity,
            description=description,
            ip_address=ip_address,
            user_agent=user_agent,
            metadata=metadata or {},
            risk_score=risk_score
        )
    
    @staticmethod
    def get_user_security_summary(user, days=30):
        """Get security summary for user"""
        from apps.authentication.models import SecurityLog, LoginAttempt
        from django.db.models import Count, Q
        
        cutoff_date = timezone.now() - timedelta(days=days)
        
        # Get security logs
        logs = SecurityLog.objects.filter(
            user=user,
            created_at__gte=cutoff_date
        )
        
        # Get login attempts
        login_attempts = LoginAttempt.objects.filter(
            user=user,
            attempted_at__gte=cutoff_date
        )
        
        summary = {
            'total_events': logs.count(),
            'critical_events': logs.filter(severity='critical').count(),
            'warning_events': logs.filter(severity='warning').count(),
            'total_logins': login_attempts.filter(success=True).count(),
            'failed_logins': login_attempts.filter(success=False).count(),
            'unique_ips': login_attempts.values('ip_address').distinct().count(),
            'high_risk_events': logs.filter(risk_score__gte=70).count(),
        }
        
        return summary


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_user_agent(request):
    """Get user agent from request"""
    return request.META.get('HTTP_USER_AGENT', '')


def generate_secure_token(length=32):
    """Generate cryptographically secure random token"""
    return secrets.token_urlsafe(length)
