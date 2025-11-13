"""
Constants and Enums
"""
from enum import Enum


class UserRole(Enum):
    """User roles"""
    STUDENT = "student"
    TEACHER = "teacher"
    STAFF = "staff"
    ADMIN = "admin"


class Gender(Enum):
    """Gender options"""
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class AttendanceStatus(Enum):
    """Attendance status"""
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"
    EXCUSED = "excused"


class AssignmentStatus(Enum):
    """Assignment status"""
    PENDING = "pending"
    SUBMITTED = "submitted"
    GRADED = "graded"
    LATE = "late"


class ExamType(Enum):
    """Exam types"""
    MID_TERM = "mid_term"
    END_TERM = "end_term"
    QUIZ = "quiz"
    PRACTICAL = "practical"


class PaymentMethod(Enum):
    """Payment methods"""
    CASH = "cash"
    CARD = "card"
    UPI = "upi"
    NET_BANKING = "net_banking"
    CHEQUE = "cheque"


class PaymentStatus(Enum):
    """Payment status"""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class CourseType(Enum):
    """Course types"""
    THEORY = "theory"
    PRACTICAL = "practical"
    LAB = "lab"
    PROJECT = "project"


class LeaveStatus(Enum):
    """Leave status"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


class AdmissionStatus(Enum):
    """Admission status"""
    APPLIED = "applied"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    ADMITTED = "admitted"


# Constants
MAX_FILE_SIZE_MB = 10
ALLOWED_IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif']
ALLOWED_DOCUMENT_EXTENSIONS = ['pdf', 'doc', 'docx', 'txt']
ALLOWED_SPREADSHEET_EXTENSIONS = ['xls', 'xlsx', 'csv']

# Pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# Date formats
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DISPLAY_DATE_FORMAT = "%d-%m-%Y"
DISPLAY_DATETIME_FORMAT = "%d-%m-%Y %H:%M:%S"

# Grading
PASSING_PERCENTAGE = 40
GRADE_BOUNDARIES = {
    'A+': 90,
    'A': 80,
    'B+': 70,
    'B': 60,
    'C+': 50,
    'C': 40,
    'F': 0
}

# Attendance
MINIMUM_ATTENDANCE_PERCENTAGE = 75

# Academic
CREDITS_PER_SEMESTER = 20
MAX_CREDITS_PER_SEMESTER = 28

# Library
MAX_BOOKS_ISSUE = 3
BOOK_ISSUE_DAYS = 14
FINE_PER_DAY = 5

# Session timeout (minutes)
SESSION_TIMEOUT = 60

# API
API_TIMEOUT = 30
MAX_RETRIES = 3
