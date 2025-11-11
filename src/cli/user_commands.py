"""CLI commands for EMIS user management."""
import click
import asyncio
from uuid import UUID

from src.database import async_session
from src.services.auth_service import AuthService
from src.models.auth import Role
from sqlalchemy import select
from src.lib.logging import get_logger

logger = get_logger(__name__)


@click.group()
def user():
    """User management commands."""
    pass


@user.command()
@click.option("--email", prompt=True, help="User email")
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True, help="User password")
@click.option("--first-name", prompt=True, help="First name")
@click.option("--last-name", prompt=True, help="Last name")
@click.option("--role", default="student", help="User role (admin/teacher/student/librarian/accountant)")
def create(email, password, first_name, last_name, role):
    """Create a new user."""
    click.echo(f"Creating user: {email}")
    asyncio.run(_create_user(email, password, first_name, last_name, role))
    click.echo("✅ User created successfully!")


@user.command()
@click.option("--email", prompt=True, help="User email")
def delete(email):
    """Delete a user."""
    if click.confirm(f"⚠️  Delete user {email}?"):
        asyncio.run(_delete_user(email))
        click.echo("✅ User deleted successfully!")


@user.command()
@click.option("--email", prompt=True, help="User email")
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True, help="New password")
def reset_password(email, password):
    """Reset user password."""
    asyncio.run(_reset_password(email, password))
    click.echo("✅ Password reset successfully!")


@user.command()
def list():
    """List all users."""
    asyncio.run(_list_users())


@user.command()
@click.option("--email", prompt=True, help="User email")
@click.option("--role", prompt=True, help="Role to assign")
def assign_role(email, role):
    """Assign role to user."""
    asyncio.run(_assign_role(email, role))
    click.echo("✅ Role assigned successfully!")


async def _create_user(email, password, first_name, last_name, role_name):
    """Create a new user."""
    async with async_session() as db:
        auth_service = AuthService(db)
        
        # Get role
        result = await db.execute(
            select(Role).where(Role.name == role_name)
        )
        role = result.scalar_one_or_none()
        
        if not role:
            click.echo(f"❌ Role '{role_name}' not found")
            return
        
        try:
            user = await auth_service.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role_ids=[role.id]
            )
            
            click.echo(f"User ID: {user.id}")
            click.echo(f"Email: {user.email}")
            click.echo(f"Role: {role_name}")
            
        except ValueError as e:
            click.echo(f"❌ Error: {e}")


async def _delete_user(email):
    """Delete a user."""
    from src.models.auth import User
    
    async with async_session() as db:
        result = await db.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            click.echo(f"❌ User {email} not found")
            return
        
        user.status = "inactive"
        await db.commit()


async def _reset_password(email, password):
    """Reset user password."""
    from src.models.auth import User
    
    async with async_session() as db:
        auth_service = AuthService(db)
        
        result = await db.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            click.echo(f"❌ User {email} not found")
            return
        
        user.password_hash = auth_service.hash_password(password)
        await db.commit()


async def _list_users():
    """List all users."""
    from src.models.auth import User
    from sqlalchemy.orm import selectinload
    
    async with async_session() as db:
        result = await db.execute(
            select(User).options(selectinload(User.roles))
        )
        users = list(result.scalars().all())
        
        if not users:
            click.echo("No users found")
            return
        
        click.echo(f"\n{'Email':<30} {'Name':<30} {'Roles':<30} {'Status':<10}")
        click.echo("-" * 100)
        
        for user in users:
            name = f"{user.first_name} {user.last_name}"
            roles = ", ".join(r.name for r in user.roles)
            click.echo(f"{user.email:<30} {name:<30} {roles:<30} {user.status:<10}")


async def _assign_role(email, role_name):
    """Assign role to user."""
    from src.models.auth import User
    
    async with async_session() as db:
        # Get user
        user_result = await db.execute(
            select(User).where(User.email == email)
        )
        user = user_result.scalar_one_or_none()
        
        if not user:
            click.echo(f"❌ User {email} not found")
            return
        
        # Get role
        role_result = await db.execute(
            select(Role).where(Role.name == role_name)
        )
        role = role_result.scalar_one_or_none()
        
        if not role:
            click.echo(f"❌ Role '{role_name}' not found")
            return
        
        # Add role if not already assigned
        if role not in user.roles:
            user.roles.append(role)
            await db.commit()
        else:
            click.echo(f"User already has role '{role_name}'")


if __name__ == "__main__":
    user()
