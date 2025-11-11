"""CLI commands for EMIS database management."""
import click
import asyncio
from datetime import date

from src.database import async_session
from src.services.auth_service import AuthService
from src.models.auth import User, Role, Permission
from src.lib.logging import get_logger

logger = get_logger(__name__)


@click.group()
def db():
    """Database management commands."""
    pass


@db.command()
def init():
    """Initialize database with default data."""
    click.echo("Initializing database...")
    asyncio.run(_init_db())
    click.echo("✅ Database initialized successfully!")


@db.command()
def seed():
    """Seed database with sample data."""
    click.echo("Seeding database with sample data...")
    asyncio.run(_seed_db())
    click.echo("✅ Database seeded successfully!")


@db.command()
def reset():
    """Reset database (WARNING: This will delete all data)."""
    if click.confirm("⚠️  This will delete all data. Are you sure?"):
        click.echo("Resetting database...")
        asyncio.run(_reset_db())
        click.echo("✅ Database reset successfully!")


async def _init_db():
    """Initialize database with default roles and permissions."""
    async with async_session() as db:
        auth_service = AuthService(db)
        
        # Create default permissions
        permissions_data = [
            # Student permissions
            ("student.view", "View students"),
            ("student.create", "Create students"),
            ("student.update", "Update students"),
            ("student.delete", "Delete students"),
            
            # Employee permissions
            ("employee.view", "View employees"),
            ("employee.create", "Create employees"),
            ("employee.update", "Update employees"),
            ("employee.delete", "Delete employees"),
            
            # Course permissions
            ("course.view", "View courses"),
            ("course.create", "Create courses"),
            ("course.update", "Update courses"),
            ("course.delete", "Delete courses"),
            
            # Finance permissions
            ("finance.view", "View finance"),
            ("finance.manage", "Manage finance"),
            
            # Library permissions
            ("library.view", "View library"),
            ("library.manage", "Manage library"),
            
            # Admin permissions
            ("admin.all", "Full admin access"),
        ]
        
        permissions = []
        for name, description in permissions_data:
            perm = Permission(name=name, description=description)
            db.add(perm)
            permissions.append(perm)
        
        await db.flush()
        
        # Create default roles
        roles_data = [
            ("admin", "Administrator", [p for p in permissions]),
            ("teacher", "Teacher", [p for p in permissions if "course" in p.name or "student.view" in p.name]),
            ("student", "Student", [p for p in permissions if ".view" in p.name and "student" in p.name]),
            ("librarian", "Librarian", [p for p in permissions if "library" in p.name]),
            ("accountant", "Accountant", [p for p in permissions if "finance" in p.name]),
        ]
        
        roles = []
        for name, description, perms in roles_data:
            role = Role(name=name, description=description)
            role.permissions = perms
            db.add(role)
            roles.append(role)
        
        await db.commit()
        
        # Create default admin user
        admin_role = next(r for r in roles if r.name == "admin")
        
        admin_user = await auth_service.create_user(
            email="admin@emis.edu",
            password="Admin@123",  # Change in production!
            first_name="System",
            last_name="Administrator",
            role_ids=[admin_role.id]
        )
        
        logger.info(f"Created admin user: {admin_user.email}")
        
        click.echo(f"Created {len(permissions)} permissions")
        click.echo(f"Created {len(roles)} roles")
        click.echo(f"Created admin user: admin@emis.edu / Admin@123")


async def _seed_db():
    """Seed database with sample data."""
    from src.services.student_service import StudentService
    from src.services.course_service import CourseService
    from src.services.library_service import LibraryService
    from src.services.finance_service import FinanceService
    
    async with async_session() as db:
        student_service = StudentService(db)
        course_service = CourseService(db)
        library_service = LibraryService(db)
        finance_service = FinanceService(db)
        
        # Create sample programs
        program = await finance_service.create_program(
            program_code="CS-BSC",
            program_name="Bachelor of Science in Computer Science",
            degree_level="Undergraduate",
            duration_years=4,
            department="Computer Science"
        )
        
        # Create sample students
        students = []
        for i in range(10):
            student = await student_service.create_student(
                first_name=f"Student{i+1}",
                last_name=f"Test{i+1}",
                email=f"student{i+1}@emis.edu",
                date_of_birth=date(2000 + i, 1, 1),
                phone=f"+1234567{i:04d}"
            )
            student.program_id = program.id
            students.append(student)
        
        await db.commit()
        
        # Create sample books
        books_data = [
            ("978-0132350884", "Clean Code", "Robert C. Martin"),
            ("978-0201616224", "The Pragmatic Programmer", "Andrew Hunt"),
            ("978-0596009205", "Head First Design Patterns", "Eric Freeman"),
        ]
        
        for isbn, title, author in books_data:
            await library_service.add_book(
                isbn=isbn,
                title=title,
                author=author,
                total_copies=5
            )
        
        click.echo(f"Created 1 program")
        click.echo(f"Created {len(students)} sample students")
        click.echo(f"Created {len(books_data)} sample books")


async def _reset_db():
    """Reset database."""
    from sqlalchemy import text
    from src.database import engine
    from src.models import Base
    
    async with engine.begin() as conn:
        # Drop all tables
        await conn.run_sync(Base.metadata.drop_all)
        # Recreate all tables
        await conn.run_sync(Base.metadata.create_all)
    
    # Reinitialize with default data
    await _init_db()


if __name__ == "__main__":
    db()
