from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
import uuid
import secrets
import hashlib
from datetime import timedelta
from .user_manager import UserManager

class User(AbstractUser):
    """
    Enhanced User model with security features
    """
    class AccountStatus(models.TextChoices):
        ACTIVE = 'active', 'Active'
        SUSPENDED = 'suspended', 'Suspended'
        DEACTIVATED = 'deactivated', 'Deactivated'
        PENDING = 'pending', 'Pending Verification'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, db_index=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profiles/%Y/%m/', blank=True, null=True)
    bio = models.TextField(blank=True)
    is_student = models.BooleanField(default=False)
    is_faculty = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    two_factor_enabled = models.BooleanField(default=False)
    two_factor_secret = models.CharField(max_length=32, blank=True, null=True)
    backup_codes = models.JSONField(default=list, help_text="Encrypted backup codes for 2FA")
    password_changed_at = models.DateTimeField(null=True, blank=True)
    password_reset_required = models.BooleanField(default=False)
    failed_login_attempts = models.IntegerField(default=0)
    account_locked_until = models.DateTimeField(null=True, blank=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    last_login_user_agent = models.TextField(blank=True)
    active_sessions = models.JSONField(default=list, help_text="List of active session tokens")
    max_concurrent_sessions = models.IntegerField(default=3)
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=64, blank=True, null=True)
    email_verification_sent_at = models.DateTimeField(null=True, blank=True)
    account_status = models.CharField(
        max_length=20,
        choices=AccountStatus.choices,
        default=AccountStatus.PENDING
    )
    suspension_reason = models.TextField(blank=True)
    suspended_until = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_activity_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_users'
    )
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['username']),
            models.Index(fields=['account_status']),
        ]
    def __str__(self):
        return self.email or self.username
    def is_account_locked(self):
        if self.account_locked_until:
            if timezone.now() < self.account_locked_until:
                return True
            else:
                self.account_locked_until = None
                self.failed_login_attempts = 0
                self.save(update_fields=['account_locked_until', 'failed_login_attempts'])
        return False
    def lock_account(self, duration_minutes=30):
        self.account_locked_until = timezone.now() + timedelta(minutes=duration_minutes)
        self.save(update_fields=['account_locked_until'])
    def record_failed_login(self):
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:
            self.lock_account(30)
        self.save(update_fields=['failed_login_attempts'])
    def reset_failed_logins(self):
        self.failed_login_attempts = 0
        self.save(update_fields=['failed_login_attempts'])
    def generate_2fa_secret(self):
        import pyotp
        self.two_factor_secret = pyotp.random_base32()
        self.save(update_fields=['two_factor_secret'])
        return self.two_factor_secret
    def verify_2fa_token(self, token):
        if not self.two_factor_enabled or not self.two_factor_secret:
            return False
        import pyotp
        totp = pyotp.TOTP(self.two_factor_secret)
        return totp.verify(token, valid_window=1)
    def generate_backup_codes(self, count=10):
        codes = []
        for _ in range(count):
            code = secrets.token_hex(4)
            hashed = hashlib.sha256(code.encode()).hexdigest()
            codes.append(code)
            self.backup_codes.append(hashed)
        self.save(update_fields=['backup_codes'])
        return codes
