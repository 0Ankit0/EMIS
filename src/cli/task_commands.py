"""CLI commands for EMIS task management."""
import click
import asyncio
from datetime import datetime

from src.tasks.celery_tasks import (
    send_pending_notifications,
    send_overdue_book_reminders,
    send_assignment_due_reminders,
    send_fee_reminders,
    cleanup_old_notifications,
)
from src.lib.logging import get_logger

logger = get_logger(__name__)


@click.group()
def tasks():
    """Background task management commands."""
    pass


@tasks.command()
def send_notifications():
    """Send all pending notifications."""
    click.echo("Sending pending notifications...")
    send_pending_notifications.delay()
    click.echo("✅ Task queued!")


@tasks.command()
def overdue_books():
    """Send overdue book reminders."""
    click.echo("Sending overdue book reminders...")
    send_overdue_book_reminders.delay()
    click.echo("✅ Task queued!")


@tasks.command()
def assignment_reminders():
    """Send assignment due reminders."""
    click.echo("Sending assignment reminders...")
    send_assignment_due_reminders.delay()
    click.echo("✅ Task queued!")


@tasks.command()
def fee_reminders():
    """Send fee payment reminders."""
    click.echo("Sending fee reminders...")
    send_fee_reminders.delay()
    click.echo("✅ Task queued!")


@tasks.command()
@click.option("--days", default=90, help="Delete notifications older than this many days")
def cleanup_notifications(days):
    """Cleanup old notifications."""
    click.echo(f"Cleaning up notifications older than {days} days...")
    cleanup_old_notifications.delay(days=days)
    click.echo("✅ Task queued!")


@tasks.command()
def status():
    """Show Celery worker status."""
    from src.tasks.celery_tasks import celery_app
    
    try:
        inspect = celery_app.control.inspect()
        
        # Get active tasks
        active = inspect.active()
        if active:
            click.echo("\n📋 Active Tasks:")
            for worker, tasks in active.items():
                click.echo(f"\n  Worker: {worker}")
                for task in tasks:
                    click.echo(f"    - {task['name']} (ID: {task['id']})")
        else:
            click.echo("\n✅ No active tasks")
        
        # Get scheduled tasks
        scheduled = inspect.scheduled()
        if scheduled:
            click.echo("\n⏰ Scheduled Tasks:")
            for worker, tasks in scheduled.items():
                click.echo(f"\n  Worker: {worker}")
                for task in tasks:
                    click.echo(f"    - {task['request']['name']}")
        
        # Get registered tasks
        registered = inspect.registered()
        if registered:
            click.echo("\n📝 Registered Tasks:")
            for worker, tasks in registered.items():
                click.echo(f"\n  Worker: {worker}")
                for task in tasks:
                    if "tasks." in task:  # Only show our tasks
                        click.echo(f"    - {task}")
    
    except Exception as e:
        click.echo(f"❌ Error connecting to Celery: {e}")
        click.echo("Make sure Celery workers are running!")


@tasks.command()
def list_scheduled():
    """List all scheduled periodic tasks."""
    from src.tasks.celery_tasks import celery_app
    
    schedule = celery_app.conf.beat_schedule
    
    click.echo("\n⏰ Scheduled Periodic Tasks:\n")
    click.echo(f"{'Task':<50} {'Schedule':<20}")
    click.echo("-" * 70)
    
    for name, config in schedule.items():
        task_name = config['task']
        schedule_val = config['schedule']
        
        # Convert schedule to human-readable format
        if schedule_val >= 86400:
            schedule_str = f"{int(schedule_val / 86400)} day(s)"
        elif schedule_val >= 3600:
            schedule_str = f"{int(schedule_val / 3600)} hour(s)"
        elif schedule_val >= 60:
            schedule_str = f"{int(schedule_val / 60)} minute(s)"
        else:
            schedule_str = f"{schedule_val} second(s)"
        
        click.echo(f"{task_name:<50} {schedule_str:<20}")


if __name__ == "__main__":
    tasks()
