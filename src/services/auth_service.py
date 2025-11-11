"""Authentication service for EMIS."""
from datetime import datetime, timedelta
from typing import Optional, Tuple
from uuid import UUID

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.models.auth import User, Role
from src.lib.audit import log_audit, AuditAction
from src.lib.logging import get_logger

logger = get_logger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Service for authentication and authorization operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt."""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(user_id: UUID, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token."""
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode = {
            "sub": str(user_id),
            "exp": expire,
            "iat": datetime.utcnow(),
        }
        
        return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    @staticmethod
    def create_refresh_token(user_id: UUID) -> str:
        """Create a JWT refresh token."""
        expire = datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
        
        to_encode = {
            "sub": str(user_id),
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "refresh"
        }
        
        return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate a user by email and password."""
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()

        if not user:
            logger.warning(f"Failed login attempt for non-existent user: {email}")
            return None

        if not self.verify_password(password, user.password_hash):
            logger.warning(f"Failed login attempt for user: {email}")
            await log_audit(
                self.db,
                action=AuditAction.LOGIN_FAILED,
                entity_type="User",
                entity_id=user.id,
                user_id=user.id,
                details={"email": email}
            )
            return None

        if user.status != "active":
            logger.warning(f"Login attempt for inactive user: {email}")
            return None

        # Update last login
        user.last_login = datetime.utcnow()
        await self.db.commit()

        await log_audit(
            self.db,
            action=AuditAction.LOGIN,
            entity_type="User",
            entity_id=user.id,
            user_id=user.id,
            details={"email": email}
        )

        logger.info(f"User authenticated successfully: {email}")
        return user

    async def create_user(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        role_ids: Optional[list[UUID]] = None,
    ) -> User:
        """Create a new user account."""
        # Check if email already exists
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        if result.scalar_one_or_none():
            raise ValueError(f"User with email {email} already exists")

        # Create user
        user = User(
            email=email,
            password_hash=self.hash_password(password),
            first_name=first_name,
            last_name=last_name,
            status="active"
        )
        self.db.add(user)
        await self.db.flush()

        # Assign roles
        if role_ids:
            roles_result = await self.db.execute(
                select(Role).where(Role.id.in_(role_ids))
            )
            roles = roles_result.scalars().all()
            user.roles = list(roles)

        await self.db.commit()
        await self.db.refresh(user)

        await log_audit(
            self.db,
            action=AuditAction.CREATE,
            entity_type="User",
            entity_id=user.id,
            details={"email": email, "roles": [str(r.id) for r in user.roles]}
        )

        logger.info(f"User created: {email}")
        return user

    async def change_password(self, user_id: UUID, old_password: str, new_password: str) -> bool:
        """Change user password."""
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            return False

        if not self.verify_password(old_password, user.password_hash):
            logger.warning(f"Failed password change attempt for user: {user.email}")
            return False

        user.password_hash = self.hash_password(new_password)
        await self.db.commit()

        await log_audit(
            self.db,
            action=AuditAction.UPDATE,
            entity_type="User",
            entity_id=user.id,
            user_id=user_id,
            details={"action": "password_change"}
        )

        logger.info(f"Password changed for user: {user.email}")
        return True

    async def reset_password(self, email: str) -> Optional[str]:
        """Generate password reset token."""
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()

        if not user:
            return None

        # Create reset token (valid for 1 hour)
        reset_token = self.create_access_token(
            user.id,
            expires_delta=timedelta(hours=1)
        )

        await log_audit(
            self.db,
            action=AuditAction.UPDATE,
            entity_type="User",
            entity_id=user.id,
            user_id=user.id,
            details={"action": "password_reset_requested"}
        )

        logger.info(f"Password reset requested for: {email}")
        return reset_token

    async def get_user_permissions(self, user_id: UUID) -> list[str]:
        """Get all permissions for a user."""
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            return []

        permissions = set()
        for role in user.roles:
            for permission in role.permissions:
                permissions.add(permission.name)

        return list(permissions)
