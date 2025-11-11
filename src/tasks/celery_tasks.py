"""Background tasks for EMIS using Celery."""
from celery import Celery
from datetime import datetime, timedelta, date
from typing import List
import asyncio

from src.config import settings
from src.database import async_session
from src.services.notification_service import NotificationService
from src.services.library_service import LibraryService
from src.services.hr_service import HRService
from src.models.notification import NotificationChannel, NotificationPriority
from src.lib.logging import get_logger

logger = get_logger(__name__)

# Initialize Celery
celery_app = Celery(
    "emis_tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)


def async_task(func):
    """Decorator to run async functions in Celery tasks."""
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))
    return wrapper


@celery_app.task(name="tasks.send_pending_notifications")
@async_task
async def send_pending_notifications():
    """Send all pending notifications."""
    async with async_session() as db:
        notification_service = NotificationService(db)
        await notification_service.send_pending_notifications()
        logger.info("Pending notifications sent")


@celery_app.task(name="tasks.send_overdue_book_reminders")
@async_task
async def send_overdue_book_reminders():
    """Send reminders for overdue books."""
    async with async_session() as db:
        library_service = LibraryService(db)
        notification_service = NotificationService(db)
        
        overdue_books = await library_service.get_overdue_books()
        
        for transaction in overdue_books:
            days_overdue = (date.today() - transaction.due_date).days
            
            message = f"""
            Dear User,
            
            The book "{transaction.book.title}" issued to you is overdue by {days_overdue} days.
            
            Due Date: {transaction.due_date}
            Fine: ${transaction.fine_amount or days_overdue * 5.0}
            
            Please return the book at your earliest convenience.
            
            Thank you.
            """
            
            await notification_service.create_notification(
                recipient_id=transaction.borrower_id,
                title="Overdue Book Reminder",
                message=message,
                channel=NotificationChannel.EMAIL,
                priority=NotificationPriority.HIGH
            )
        
        logger.info(f"Sent {len(overdue_books)} overdue book reminders")


@celery_app.task(name="tasks.send_assignment_due_reminders")
@async_task
async def send_assignment_due_reminders():
    """Send reminders for assignments due soon."""
    from sqlalchemy import select, and_
    from src.models.course import Assignment, AssignmentSubmission
    from src.models.enrollment import Enrollment
    
    async with async_session() as db:
        notification_service = NotificationService(db)
        
        # Get assignments due in next 2 days
        tomorrow = datetime.utcnow() + timedelta(days=1)
        day_after = datetime.utcnow() + timedelta(days=2)
        
        result = await db.execute(
            select(Assignment).where(
                and_(
                    Assignment.due_date >= tomorrow,
                    Assignment.due_date <= day_after
                )
            )
        )
        assignments = list(result.scalars().all())
        
        for assignment in assignments:
            # Get enrolled students
            enrollment_result = await db.execute(
                select(Enrollment).where(
                    and_(
                        Enrollment.course_id == assignment.course_id,
                        Enrollment.status == "active"
                    )
                )
            )
            enrollments = list(enrollment_result.scalars().all())
            
            for enrollment in enrollments:
                # Check if already submitted
                submission_result = await db.execute(
                    select(AssignmentSubmission).where(
                        and_(
                            AssignmentSubmission.assignment_id == assignment.id,
                            AssignmentSubmission.student_id == enrollment.student_id
                        )
                    )
                )
                if submission_result.scalar_one_or_none():
                    continue  # Already submitted
                
                message = f"""
                Reminder: Assignment Due Soon
                
                Assignment: {assignment.title}
                Course: {assignment.course.course_name}
                Due Date: {assignment.due_date.strftime('%Y-%m-%d %H:%M')}
                
                Please submit your assignment before the deadline.
                """
                
                await notification_service.create_notification(
                    recipient_id=enrollment.student.user_id,
                    title=f"Assignment Due: {assignment.title}",
                    message=message,
                    channel=NotificationChannel.IN_APP,
                    priority=NotificationPriority.NORMAL
                )
        
        logger.info(f"Sent assignment reminders for {len(assignments)} assignments")


@celery_app.task(name="tasks.process_payroll")
@async_task
async def process_payroll(month: int, year: int):
    """Process monthly payroll for all employees."""
    async with async_session() as db:
        hr_service = HRService(db)
        notification_service = NotificationService(db)
        
        from sqlalchemy import select
        from src.models.employee import Employee, EmployeeStatus
        
        # Get all active employees
        result = await db.execute(
            select(Employee).where(Employee.status == EmployeeStatus.ACTIVE)
        )
        employees = list(result.scalars().all())
        
        for employee in employees:
            try:
                payroll = await hr_service.process_payroll(
                    employee_id=employee.id,
                    month=month,
                    year=year
                )
                
                # Send notification
                message = f"""
                Dear {employee.first_name},
                
                Your payroll for {month}/{year} has been processed.
                
                Gross Salary: ${payroll.gross_salary}
                Net Salary: ${payroll.net_salary}
                
                Payment Status: {payroll.payment_status}
                """
                
                await notification_service.create_notification(
                    recipient_id=employee.user_id,
                    title="Payroll Processed",
                    message=message,
                    channel=NotificationChannel.EMAIL,
                    priority=NotificationPriority.NORMAL
                )
                
            except Exception as e:
                logger.error(f"Failed to process payroll for {employee.employee_number}: {e}")
        
        logger.info(f"Processed payroll for {len(employees)} employees")


@celery_app.task(name="tasks.cleanup_old_notifications")
@async_task
async def cleanup_old_notifications(days: int = 90):
    """Delete old notifications."""
    from sqlalchemy import delete
    from src.models.notification import Notification
    
    async with async_session() as db:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        result = await db.execute(
            delete(Notification).where(
                Notification.created_at < cutoff_date
            )
        )
        
        await db.commit()
        logger.info(f"Deleted {result.rowcount} old notifications")


@celery_app.task(name="tasks.generate_attendance_report")
@async_task
async def generate_attendance_report(course_id: str, date_from: str, date_to: str):
    """Generate attendance report for a course."""
    from uuid import UUID
    from datetime import date as dt_date
    from sqlalchemy import select, and_, func
    from src.models.attendance import Attendance
    from src.models.enrollment import Enrollment
    
    async with async_session() as db:
        course_uuid = UUID(course_id)
        start_date = dt_date.fromisoformat(date_from)
        end_date = dt_date.fromisoformat(date_to)
        
        # Get attendance records
        result = await db.execute(
            select(Attendance)
            .join(Enrollment)
            .where(
                and_(
                    Enrollment.course_id == course_uuid,
                    Attendance.date >= start_date,
                    Attendance.date <= end_date
                )
            )
        )
        attendance_records = list(result.scalars().all())
        
        # Calculate statistics
        total_classes = len(set(a.date for a in attendance_records))
        
        report = {
            "course_id": course_id,
            "period": f"{date_from} to {date_to}",
            "total_classes": total_classes,
            "records": len(attendance_records),
        }
        
        logger.info(f"Generated attendance report for course {course_id}")
        return report


@celery_app.task(name="tasks.backup_database")
@async_task
async def backup_database():
    """Backup database (placeholder)."""
    # TODO: Implement database backup logic
    logger.info("Database backup task executed")
    pass


@celery_app.task(name="tasks.send_fee_reminders")
@async_task
async def send_fee_reminders():
    """Send fee payment reminders to students with pending dues."""
    from sqlalchemy import select
    from src.models.student import Student, StudentStatus
    from src.services.finance_service import FinanceService
    
    async with async_session() as db:
        finance_service = FinanceService(db)
        notification_service = NotificationService(db)
        
        # Get all active students
        result = await db.execute(
            select(Student).where(Student.status == StudentStatus.ACTIVE)
        )
        students = list(result.scalars().all())
        
        current_year = f"{datetime.utcnow().year}-{datetime.utcnow().year + 1}"
        
        for student in students:
            try:
                fee_status = await finance_service.get_student_fee_status(
                    student_id=student.id,
                    academic_year=current_year
                )
                
                if fee_status["balance"] > 0:
                    message = f"""
                    Dear {student.first_name},
                    
                    This is a reminder about your pending fee payment.
                    
                    Academic Year: {current_year}
                    Total Fee: ${fee_status['total_fee']}
                    Paid: ${fee_status['total_paid']}
                    Scholarship: ${fee_status['total_scholarship']}
                    Balance Due: ${fee_status['balance']}
                    
                    Please make the payment at your earliest convenience.
                    """
                    
                    await notification_service.create_notification(
                        recipient_id=student.user_id,
                        title="Fee Payment Reminder",
                        message=message,
                        channel=NotificationChannel.EMAIL,
                        priority=NotificationPriority.HIGH
                    )
            except Exception as e:
                logger.error(f"Failed to send fee reminder to {student.student_number}: {e}")
        
        logger.info("Fee reminders sent")


# Celery Beat Schedule
celery_app.conf.beat_schedule = {
    "send-pending-notifications-every-5-minutes": {
        "task": "tasks.send_pending_notifications",
        "schedule": 300.0,  # 5 minutes
    },
    "send-overdue-book-reminders-daily": {
        "task": "tasks.send_overdue_book_reminders",
        "schedule": 86400.0,  # Daily
    },
    "send-assignment-reminders-daily": {
        "task": "tasks.send_assignment_due_reminders",
        "schedule": 86400.0,  # Daily
    },
    "cleanup-old-notifications-weekly": {
        "task": "tasks.cleanup_old_notifications",
        "schedule": 604800.0,  # Weekly
    },
    "send-fee-reminders-weekly": {
        "task": "tasks.send_fee_reminders",
        "schedule": 604800.0,  # Weekly
    },
    "backup-database-daily": {
        "task": "tasks.backup_database",
        "schedule": 86400.0,  # Daily at midnight
    },
}
