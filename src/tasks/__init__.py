"""Background tasks for EMIS."""

from .celery_tasks import (
    celery_app,
    send_pending_notifications,
    send_overdue_book_reminders,
    send_assignment_due_reminders,
    process_payroll,
    cleanup_old_notifications,
    generate_attendance_report,
    backup_database,
    send_fee_reminders,
)

__all__ = [
    "celery_app",
    "send_pending_notifications",
    "send_overdue_book_reminders",
    "send_assignment_due_reminders",
    "process_payroll",
    "cleanup_old_notifications",
    "generate_attendance_report",
    "backup_database",
    "send_fee_reminders",
]
