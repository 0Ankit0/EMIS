"""Comprehensive tests for Authentication Service"""
import pytest
from datetime import datetime, timedelta
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.auth import User, Role, Permission
from src.services.auth_service import AuthService


@pytest.fixture
def auth_service():
    """Create auth service instance"""
    return AuthService()


@pytest.mark.asyncio
async def test_user_registration(db_session: AsyncSession, auth_service: AuthService):
    """Test user registration"""
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "SecurePass123!",
        "first_name": "New",
        "last_name": "User"
    }
    
    user = await auth_service.register_user(db_session, user_data)
    
    assert user is not None
    assert user.username == "newuser"
    assert user.email == "newuser@example.com"
    assert user.hashed_password is not None
    assert user.hashed_password != "SecurePass123!"  # Password should be hashed


@pytest.mark.asyncio
async def test_user_login_success(db_session: AsyncSession, auth_service: AuthService, test_user):
    """Test successful user login"""
    token = await auth_service.login(
        db_session,
        username="testuser",
        password="testpassword"
    )
    
    assert token is not None
    assert "access_token" in token
    assert "token_type" in token
    assert token["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_user_login_invalid_password(db_session: AsyncSession, auth_service: AuthService, test_user):
    """Test login with invalid password"""
    with pytest.raises(Exception):  # Should raise authentication error
        await auth_service.login(
            db_session,
            username="testuser",
            password="wrongpassword"
        )


@pytest.mark.asyncio
async def test_user_login_nonexistent_user(db_session: AsyncSession, auth_service: AuthService):
    """Test login with non-existent user"""
    with pytest.raises(Exception):
        await auth_service.login(
            db_session,
            username="nonexistent",
            password="anypassword"
        )


@pytest.mark.asyncio
async def test_verify_token(db_session: AsyncSession, auth_service: AuthService, test_user):
    """Test token verification"""
    # Login to get token
    token_data = await auth_service.login(
        db_session,
        username="testuser",
        password="testpassword"
    )
    
    # Verify token
    payload = await auth_service.verify_token(token_data["access_token"])
    
    assert payload is not None
    assert payload.get("sub") == test_user.username


@pytest.mark.asyncio
async def test_verify_invalid_token(db_session: AsyncSession, auth_service: AuthService):
    """Test verification of invalid token"""
    with pytest.raises(Exception):
        await auth_service.verify_token("invalid.token.here")


@pytest.mark.asyncio
async def test_verify_expired_token(db_session: AsyncSession, auth_service: AuthService):
    """Test verification of expired token"""
    # Create expired token
    expired_token = auth_service.create_token(
        data={"sub": "testuser"},
        expires_delta=timedelta(seconds=-1)  # Already expired
    )
    
    with pytest.raises(Exception):
        await auth_service.verify_token(expired_token)


@pytest.mark.asyncio
async def test_change_password(db_session: AsyncSession, auth_service: AuthService, test_user):
    """Test password change"""
    success = await auth_service.change_password(
        db_session,
        user_id=test_user.id,
        old_password="testpassword",
        new_password="NewSecurePass123!"
    )
    
    assert success is True
    
    # Verify new password works
    token = await auth_service.login(
        db_session,
        username="testuser",
        password="NewSecurePass123!"
    )
    assert token is not None


@pytest.mark.asyncio
async def test_change_password_wrong_old_password(
    db_session: AsyncSession,
    auth_service: AuthService,
    test_user
):
    """Test password change with wrong old password"""
    with pytest.raises(Exception):
        await auth_service.change_password(
            db_session,
            user_id=test_user.id,
            old_password="wrongoldpassword",
            new_password="NewSecurePass123!"
        )


@pytest.mark.asyncio
async def test_reset_password(db_session: AsyncSession, auth_service: AuthService, test_user):
    """Test password reset"""
    # Generate reset token
    reset_token = await auth_service.generate_reset_token(
        db_session,
        email=test_user.email
    )
    
    assert reset_token is not None
    
    # Reset password
    success = await auth_service.reset_password(
        db_session,
        reset_token=reset_token,
        new_password="ResetPass123!"
    )
    
    assert success is True


@pytest.mark.asyncio
async def test_assign_role_to_user(
    db_session: AsyncSession,
    auth_service: AuthService,
    test_user,
    test_role
):
    """Test assigning role to user"""
    success = await auth_service.assign_role(
        db_session,
        user_id=test_user.id,
        role_id=test_role.id
    )
    
    assert success is True
    
    # Verify role assigned
    user = await auth_service.get_user_by_id(db_session, test_user.id)
    assert test_role.id in [r.id for r in user.roles]


@pytest.mark.asyncio
async def test_remove_role_from_user(
    db_session: AsyncSession,
    auth_service: AuthService,
    test_user,
    test_role
):
    """Test removing role from user"""
    # First assign role
    await auth_service.assign_role(db_session, test_user.id, test_role.id)
    
    # Then remove it
    success = await auth_service.remove_role(
        db_session,
        user_id=test_user.id,
        role_id=test_role.id
    )
    
    assert success is True


@pytest.mark.asyncio
async def test_check_permission(
    db_session: AsyncSession,
    auth_service: AuthService,
    test_user,
    test_role,
    test_permission
):
    """Test permission checking"""
    # Assign permission to role
    await auth_service.assign_permission_to_role(
        db_session,
        role_id=test_role.id,
        permission_id=test_permission.id
    )
    
    # Assign role to user
    await auth_service.assign_role(db_session, test_user.id, test_role.id)
    
    # Check permission
    has_permission = await auth_service.has_permission(
        db_session,
        user_id=test_user.id,
        resource=test_permission.resource,
        action=test_permission.action
    )
    
    assert has_permission is True


@pytest.mark.asyncio
async def test_deactivate_user(db_session: AsyncSession, auth_service: AuthService, test_user):
    """Test user deactivation"""
    success = await auth_service.deactivate_user(db_session, test_user.id)
    
    assert success is True
    
    # Verify user cannot login
    with pytest.raises(Exception):
        await auth_service.login(
            db_session,
            username="testuser",
            password="testpassword"
        )


@pytest.mark.asyncio
async def test_activate_user(db_session: AsyncSession, auth_service: AuthService, test_user):
    """Test user activation"""
    # First deactivate
    await auth_service.deactivate_user(db_session, test_user.id)
    
    # Then activate
    success = await auth_service.activate_user(db_session, test_user.id)
    
    assert success is True
    
    # Verify user can login
    token = await auth_service.login(
        db_session,
        username="testuser",
        password="testpassword"
    )
    assert token is not None


@pytest.mark.asyncio
async def test_refresh_token(db_session: AsyncSession, auth_service: AuthService, test_user):
    """Test token refresh"""
    # Get initial token
    initial_token = await auth_service.login(
        db_session,
        username="testuser",
        password="testpassword"
    )
    
    # Refresh token
    new_token = await auth_service.refresh_token(
        db_session,
        refresh_token=initial_token.get("refresh_token")
    )
    
    assert new_token is not None
    assert "access_token" in new_token


@pytest.mark.asyncio
async def test_get_user_permissions(
    db_session: AsyncSession,
    auth_service: AuthService,
    test_user,
    test_role,
    test_permission
):
    """Test getting all user permissions"""
    # Setup
    await auth_service.assign_permission_to_role(
        db_session, test_role.id, test_permission.id
    )
    await auth_service.assign_role(db_session, test_user.id, test_role.id)
    
    # Get permissions
    permissions = await auth_service.get_user_permissions(
        db_session,
        user_id=test_user.id
    )
    
    assert len(permissions) >= 1
    assert any(p.resource == test_permission.resource for p in permissions)


@pytest.mark.asyncio
async def test_password_strength_validation(auth_service: AuthService):
    """Test password strength validation"""
    # Weak passwords
    assert auth_service.validate_password_strength("weak") is False
    assert auth_service.validate_password_strength("12345678") is False
    assert auth_service.validate_password_strength("password") is False
    
    # Strong passwords
    assert auth_service.validate_password_strength("SecurePass123!") is True
    assert auth_service.validate_password_strength("MyP@ssw0rd2024") is True


@pytest.mark.asyncio
async def test_email_verification(db_session: AsyncSession, auth_service: AuthService, test_user):
    """Test email verification"""
    # Generate verification token
    verify_token = await auth_service.generate_email_verification_token(
        db_session,
        user_id=test_user.id
    )
    
    assert verify_token is not None
    
    # Verify email
    success = await auth_service.verify_email(db_session, verify_token)
    
    assert success is True
    
    # Check user is verified
    user = await auth_service.get_user_by_id(db_session, test_user.id)
    assert user.email_verified is True


@pytest.mark.asyncio
async def test_login_attempt_tracking(db_session: AsyncSession, auth_service: AuthService, test_user):
    """Test login attempt tracking"""
    # Multiple failed attempts
    for _ in range(3):
        try:
            await auth_service.login(
                db_session,
                username="testuser",
                password="wrongpassword"
            )
        except:
            pass
    
    # Check if account is locked
    attempts = await auth_service.get_failed_login_attempts(
        db_session,
        username="testuser"
    )
    
    assert attempts >= 3


@pytest.mark.asyncio
async def test_session_management(db_session: AsyncSession, auth_service: AuthService, test_user):
    """Test session creation and management"""
    # Create session
    session = await auth_service.create_session(
        db_session,
        user_id=test_user.id,
        ip_address="192.168.1.1",
        user_agent="Mozilla/5.0"
    )
    
    assert session is not None
    assert session.user_id == test_user.id
    
    # Verify session is active
    is_active = await auth_service.is_session_active(db_session, session.id)
    assert is_active is True
    
    # End session
    await auth_service.end_session(db_session, session.id)
    
    # Verify session ended
    is_active = await auth_service.is_session_active(db_session, session.id)
    assert is_active is False
