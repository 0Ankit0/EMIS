"""CLI commands for library management"""
import asyncio
import click
from datetime import date
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.config import settings
from src.services.fine_service import FineService
from src.models.library_settings import MemberType


# Create async engine and session
engine = create_async_engine(settings.DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


@click.group()
def library():
    """Library management commands"""
    pass


@library.command()
def init_settings():
    """Initialize default library settings for all member types"""
    async def _init():
        async with AsyncSessionLocal() as session:
            service = FineService(session)
            await service.initialize_default_settings(created_by=1)
            click.echo("✓ Default library settings initialized successfully")
            
            # Display created settings
            all_settings = await service.get_all_library_settings()
            click.echo("\nCreated settings:")
            for setting in all_settings:
                click.echo(f"  {setting.member_type.value}: "
                          f"{setting.max_books_allowed} books, "
                          f"{setting.borrowing_period_days} days, "
                          f"₹{setting.fine_per_day}/day")
    
    asyncio.run(_init())


@library.command()
@click.argument('member_type', type=click.Choice(['student', 'faculty', 'staff', 'alumni', 'guest']))
@click.option('--max-books', type=int, help='Maximum books allowed')
@click.option('--period', type=int, help='Borrowing period in days')
@click.option('--fine', type=float, help='Fine per day')
@click.option('--grace', type=int, help='Grace period in days')
@click.option('--max-fine', type=float, help='Maximum fine amount')
def update_settings(member_type, max_books, period, fine, grace, max_fine):
    """Update library settings for a member type"""
    async def _update():
        async with AsyncSessionLocal() as session:
            service = FineService(session)
            
            # Get existing settings
            member = MemberType(member_type)
            settings = await service.get_library_settings(member)
            
            if not settings:
                click.echo(f"✗ No settings found for {member_type}. Run init-settings first.")
                return
            
            # Prepare updates
            updates = {}
            if max_books is not None:
                updates['max_books_allowed'] = max_books
            if period is not None:
                updates['borrowing_period_days'] = period
            if fine is not None:
                updates['fine_per_day'] = fine
            if grace is not None:
                updates['grace_period_days'] = grace
            if max_fine is not None:
                updates['max_fine_amount'] = max_fine
            
            if not updates:
                click.echo("✗ No updates provided. Use --max-books, --period, --fine, --grace, or --max-fine")
                return
            
            # Update
            for key, value in updates.items():
                setattr(settings, key, value)
            
            await session.commit()
            await session.refresh(settings)
            
            click.echo(f"✓ Updated settings for {member_type}:")
            click.echo(f"  Max books: {settings.max_books_allowed}")
            click.echo(f"  Period: {settings.borrowing_period_days} days")
            click.echo(f"  Fine: ₹{settings.fine_per_day}/day")
            click.echo(f"  Grace: {settings.grace_period_days} days")
            click.echo(f"  Max fine: ₹{settings.max_fine_amount}")
    
    asyncio.run(_update())


@library.command()
@click.argument('member_type', type=click.Choice(['student', 'faculty', 'staff', 'alumni', 'guest']))
@click.argument('due_date', type=click.DateTime(formats=['%Y-%m-%d']))
@click.option('--return-date', type=click.DateTime(formats=['%Y-%m-%d']), help='Return date (default: today)')
def calculate_fine(member_type, due_date, return_date):
    """Calculate fine for an overdue book"""
    async def _calculate():
        async with AsyncSessionLocal() as session:
            service = FineService(session)
            
            member = MemberType(member_type)
            due = due_date.date()
            ret = return_date.date() if return_date else date.today()
            
            fine_amount, days_overdue = await service.calculate_fine(member, due, ret)
            
            click.echo(f"\nFine Calculation for {member_type}:")
            click.echo(f"  Due date: {due}")
            click.echo(f"  Return date: {ret}")
            click.echo(f"  Days overdue: {days_overdue}")
            click.echo(f"  Fine amount: ₹{fine_amount:.2f}")
    
    asyncio.run(_calculate())


@library.command()
def show_settings():
    """Display current library settings for all member types"""
    async def _show():
        async with AsyncSessionLocal() as session:
            service = FineService(session)
            all_settings = await service.get_all_library_settings()
            
            if not all_settings:
                click.echo("✗ No library settings found. Run init-settings first.")
                return
            
            click.echo("\nLibrary Settings:")
            click.echo("=" * 80)
            
            for setting in all_settings:
                click.echo(f"\n{setting.member_type.value.upper()}")
                click.echo("-" * 40)
                click.echo(f"  Max books: {setting.max_books_allowed}")
                click.echo(f"  Borrowing period: {setting.borrowing_period_days} days")
                click.echo(f"  Fine per day: ₹{setting.fine_per_day}")
                click.echo(f"  Grace period: {setting.grace_period_days} days")
                click.echo(f"  Max fine: ₹{setting.max_fine_amount}")
                click.echo(f"  Max reservations: {setting.max_reservations}")
                click.echo(f"  Max renewals: {setting.max_renewals}")
                click.echo(f"  Digital access: {'Yes' if setting.digital_access_enabled else 'No'}")
    
    asyncio.run(_show())


if __name__ == '__main__':
    library()
