"""Models package for EMIS."""

# Auth models
from src.models.auth import User, Role, Permission

# Student models
from src.models.student import Student
from src.models.enrollment import Enrollment
from src.models.academic_record import AcademicRecord
from src.models.attendance import Attendance
from src.models.class_schedule import ClassSchedule
from src.models.exam import Exam
from src.models.marks import Marks
from src.models.result_sheet import ResultSheet

# Employee models
from src.models.employee import Employee
from src.models.payroll import Payroll
from src.models.leave import Leave
from src.models.performance import PerformanceReview
from src.models.recruitment import JobPosting

# Course/LMS models
from src.models.course import Course, Assignment, AssignmentSubmission

# Library models
from src.models.library import Book, BookTransaction
from src.models.library_settings import LibrarySettings, FineWaiver

# Finance models
from src.models.finance import (
    Program,
    FeeStructure,
    Payment,
    Scholarship,
)

# Admission models
from src.models.admission import Application

# Notification models
from src.models.notification import Notification, NotificationTemplate

__all__ = [
    # Auth
    "User",
    "Role",
    "Permission",
    # Students
    "Student",
    "Enrollment",
    "AcademicRecord",
    "Attendance",
    "ClassSchedule",
    "Exam",
    "Marks",
    "ResultSheet",
    # Employees
    "Employee",
    "Payroll",
    "Leave",
    "PerformanceReview",
    "JobPosting",
    # Courses
    "Course",
    "Assignment",
    "AssignmentSubmission",
    # Library
    "Book",
    "BookTransaction",
    "LibrarySettings",
    "FineWaiver",
    # Finance
    "Program",
    "FeeStructure",
    "Payment",
    "Scholarship",
    # Admissions
    "Application",
    # Notifications
    "Notification",
    "NotificationTemplate",
]
