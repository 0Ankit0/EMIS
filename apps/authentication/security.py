"""
Password hashing and security utilities for authentication
"""
from passlib.context import CryptContext
from django.contrib.auth.hashers import make_password, check_password
import secrets
import string


# Password context for bcrypt hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a password using Django's make_password (which supports bcrypt)
    
    Args:
        password: Plain text password
    
    Returns:
        Hashed password
    """
    return make_password(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password to verify against
    
    Returns:
        True if password matches, False otherwise
    """
    return check_password(plain_password, hashed_password)


def generate_secure_token(length: int = 32) -> str:
    """
    Generate a cryptographically secure random token
    
    Args:
        length: Length of the token
    
    Returns:
        Secure random token
    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def generate_2fa_secret() -> str:
    """
    Generate a secret for two-factor authentication
    
    Returns:
        32-character secret string
    """
    return generate_secure_token(32)


def is_password_strong(password: str) -> tuple[bool, list[str]]:
    """
    Check if password meets strength requirements
    
    Requirements:
    - At least 8 characters
    - Contains uppercase and lowercase
    - Contains at least one digit
    - Contains at least one special character
    
    Args:
        password: Password to check
    
    Returns:
        Tuple of (is_valid, list of error messages)
    """
    errors = []
    
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    
    if not any(c.isupper() for c in password):
        errors.append("Password must contain at least one uppercase letter")
    
    if not any(c.islower() for c in password):
        errors.append("Password must contain at least one lowercase letter")
    
    if not any(c.isdigit() for c in password):
        errors.append("Password must contain at least one digit")
    
    special_chars = set(string.punctuation)
    if not any(c in special_chars for c in password):
        errors.append("Password must contain at least one special character")
    
    return (len(errors) == 0, errors)
