# 🛠️ EMIS Services Documentation

Complete documentation for all services, middleware, tasks, and libraries in the EMIS system.

---

## 📦 Services

### AuthService
**File**: `src/services/auth_service.py`

Handles authentication and authorization operations.

**Methods:**
- `hash_password(password)` - Hash password using bcrypt
- `verify_password(plain_password, hashed_password)` - Verify password
- `create_access_token(user_id, expires_delta)` - Create JWT access token
- `create_refresh_token(user_id)` - Create JWT refresh token
- `authenticate_user(email, password)` - Authenticate user by credentials
- `create_user(email, password, first_name, last_name, role_ids)` - Create new user
- `change_password(user_id, old_password, new_password)` - Change password
- `reset_password(email)` - Generate password reset token
- `get_user_permissions(user_id)` - Get all user permissions

**Usage:**
```python
from src.services.auth_service import AuthService

async with async_session() as db:
    auth_service = AuthService(db)
    user = await auth_service.authenticate_user("user@emis.edu", "password")
    token = auth_service.create_access_token(user.id)
```

---

### StudentService
**File**: `src/services/student_service.py`

Manages student lifecycle operations.

**Methods:**
- `create_student(...)` - Create new student record
- `get_student(student_id)` - Get student by ID
- `update_student(student_id, **kwargs)` - Update student information
- `delete_student(student_id)` - Soft delete student
- `search_students(query, filters)` - Search students
- `get_student_by_number(student_number)` - Get student by number
- `activate_student(student_id)` - Activate student account
- `suspend_student(student_id, reason)` - Suspend student
- `graduate_student(student_id, graduation_date)` - Mark student as graduated

---

### CourseService
**File**: `src/services/course_service.py`

Manages courses and assignments.

**Methods:**
- `create_course(...)` - Create new course
- `enroll_student(student_id, course_id)` - Enroll student in course
- `create_assignment(...)` - Create assignment for course
- `submit_assignment(...)` - Submit assignment solution
- `grade_assignment(submission_id, marks, feedback)` - Grade submission
- `get_course_students(course_id)` - Get all enrolled students
- `get_student_courses(student_id, academic_year)` - Get student's courses

**Usage:**
```python
from src.services.course_service import CourseService

async with async_session() as db:
    course_service = CourseService(db)
    
    # Create course
    course = await course_service.create_course(
        course_code="CS101",
        course_name="Intro to Programming",
        credits=3,
        instructor_id=instructor_id,
        academic_year="2024-2025",
        semester="Fall"
    )
    
    # Enroll student
    enrollment = await course_service.enroll_student(student_id, course.id)
```

---

### LibraryService
**File**: `src/services/library_service.py`

Manages library operations.

**Methods:**
- `add_book(...)` - Add book to library catalog
- `issue_book(book_id, borrower_id, borrower_type, due_date)` - Issue book
- `return_book(transaction_id, return_date, condition_notes)` - Return book
- `renew_book(transaction_id, new_due_date)` - Renew book loan
- `get_overdue_books()` - Get all overdue transactions
- `get_borrower_history(borrower_id, borrower_type)` - Get borrowing history
- `search_books(query, category, available_only)` - Search books

**Features:**
- Automatic fine calculation for overdue books ($5/day)
- Prevents issuing if borrower has overdue books
- Tracks book availability
- Supports both student and employee borrowers

---

### FinanceService
**File**: `src/services/finance_service.py`

Manages financial operations.

**Methods:**
- `create_program(...)` - Create academic program
- `create_fee_structure(...)` - Create fee structure for program
- `record_payment(...)` - Record fee payment
- `award_scholarship(...)` - Award scholarship to student
- `get_student_fee_status(student_id, academic_year, semester)` - Get fee status
- `get_payment_history(student_id, academic_year)` - Get payment history

**Usage:**
```python
from src/services.finance_service import FinanceService

async with async_session() as db:
    finance_service = FinanceService(db)
    
    # Get fee status
    status = await finance_service.get_student_fee_status(
        student_id=student_id,
        academic_year="2024-2025"
    )
    
    print(f"Balance: ${status['balance']}")
```

---

### AdmissionService
**File**: `src/services/admission_service.py`

Manages admission applications.

**Methods:**
- `create_application(...)` - Create admission application
- `update_application_status(application_id, status, reviewed_by, comments)` - Update status
- `approve_application(application_id, reviewed_by, create_student)` - Approve application
- `reject_application(application_id, reviewed_by, rejection_reason)` - Reject application
- `schedule_interview(application_id, interview_date, interviewer_id)` - Schedule interview
- `get_applications_by_status(status, academic_year)` - Get applications by status

**Application Workflow:**
1. `submitted` → Initial submission
2. `under_review` → Being reviewed
3. `interview_scheduled` → Interview scheduled
4. `approved` → Approved (student created)
5. `rejected` → Rejected

---

### NotificationService
**File**: `src/services/notification_service.py`

Manages multi-channel notifications.

**Methods:**
- `create_notification(recipient_id, title, message, channel, priority)` - Create notification
- `create_from_template(recipient_id, template_code, variables, channel)` - Create from template
- `send_notification(notification_id)` - Send notification
- `mark_as_read(notification_id, recipient_id)` - Mark as read
- `get_user_notifications(user_id, unread_only, limit)` - Get user notifications
- `send_bulk_notification(recipient_ids, title, message, channel)` - Send to multiple users
- `create_template(template_code, name, subject, body, category)` - Create template
- `send_pending_notifications()` - Send all pending scheduled notifications

**Supported Channels:**
- `email` - Email notifications
- `sms` - SMS notifications
- `push` - Push notifications
- `in_app` - In-app notifications

**Priority Levels:**
- `low` - Low priority
- `normal` - Normal priority
- `high` - High priority
- `urgent` - Urgent priority

---

### HRService
**File**: `src/services/hr_service.py`

Manages employee and HR operations.

**Methods:**
- `create_employee(...)` - Create employee record
- `process_payroll(employee_id, month, year)` - Process monthly payroll
- `submit_leave_request(...)` - Submit leave request
- `approve_leave(leave_id, approved_by)` - Approve leave request
- `reject_leave(leave_id, rejected_by, reason)` - Reject leave request
- `create_performance_review(...)` - Create performance review
- `get_employee_attendance(employee_id, month, year)` - Get attendance

---

## 🔧 Middleware

### RateLimitMiddleware
**File**: `src/middleware/rate_limit.py`

Implements rate limiting using sliding window algorithm.

**Configuration:**
- Requests per minute: 60
- Requests per hour: 1000

**Headers Added:**
- `X-RateLimit-Limit-Minute`
- `X-RateLimit-Remaining-Minute`
- `X-RateLimit-Limit-Hour`
- `X-RateLimit-Remaining-Hour`

**Usage:**
```python
from src.middleware.rate_limit import RateLimitMiddleware

app.add_middleware(
    RateLimitMiddleware,
    requests_per_minute=60,
    requests_per_hour=1000
)
```

---

### RequestLoggingMiddleware
**File**: `src/middleware/logging.py`

Logs all requests and responses with timing information.

**Features:**
- Generates unique request ID
- Logs request method, path, query params
- Tracks response time
- Logs errors with stack traces

**Headers Added:**
- `X-Request-ID` - Unique request identifier
- `X-Response-Time` - Response time in milliseconds

---

### RBAC Middleware
**File**: `src/middleware/rbac.py`

Role-Based Access Control middleware.

**Functions:**
- `get_current_user(credentials)` - Get authenticated user from JWT
- `require_permissions(*permissions)` - Decorator to require permissions

**Usage:**
```python
from src.middleware.rbac import require_permissions

@router.post("/students")
@require_permissions("student.create")
async def create_student(...):
    pass
```

---

### Error Handler Middleware
**File**: `src/middleware/errors.py`

Centralized error handling.

**Handles:**
- Validation errors (422)
- Authentication errors (401)
- Authorization errors (403)
- Not found errors (404)
- Internal server errors (500)

---

### CORS Middleware
**File**: `src/middleware/cors.py`

Configure Cross-Origin Resource Sharing.

**Allowed Origins:**
- http://localhost:3000
- http://localhost:8000
- Additional from settings

---

## 🔄 Background Tasks

### Celery Tasks
**File**: `src/tasks/celery_tasks.py`

**Periodic Tasks:**

#### send_pending_notifications
**Schedule**: Every 5 minutes  
Sends all pending scheduled notifications.

#### send_overdue_book_reminders
**Schedule**: Daily  
Sends reminders for overdue library books with fine calculation.

#### send_assignment_due_reminders
**Schedule**: Daily  
Sends reminders for assignments due in next 2 days (only to students who haven't submitted).

#### send_fee_reminders
**Schedule**: Weekly  
Sends fee payment reminders to students with pending dues.

#### cleanup_old_notifications
**Schedule**: Weekly  
Deletes notifications older than 90 days.

#### backup_database
**Schedule**: Daily  
Performs database backup (placeholder for implementation).

**On-Demand Tasks:**

#### process_payroll(month, year)
Process monthly payroll for all active employees.

**Usage:**
```python
from src.tasks.celery_tasks import process_payroll

# Queue task
result = process_payroll.delay(month=1, year=2024)

# Get result
result.get()
```

---

## 📚 Libraries

### Email Service
**File**: `src/lib/email.py`

Send emails via SMTP.

**Methods:**
- `send_email(to_email, subject, body, html_body, attachments)` - Send email
- `send_template_email(to_email, template_name, context)` - Send using template
- `send_bulk_email(recipients, subject, body)` - Send bulk emails

**Configuration:**
```python
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-password
FROM_EMAIL=noreply@emis.edu
FROM_NAME=EMIS System
```

---

### File Storage
**File**: `src/lib/file_storage.py`

Handle file uploads and storage.

**Methods:**
- `save_upload_file(file, category, allowed_types)` - Save uploaded file
- `delete_file(file_path)` - Delete file
- `get_file_url(category, filename)` - Get file URL
- `save_profile_picture(file)` - Save profile picture
- `save_document(file)` - Save document
- `save_assignment_file(file)` - Save assignment file

**Features:**
- File size validation (10MB default)
- File type validation
- Unique filename generation
- Category-based organization
- SHA256 hash for duplicate detection

**Usage:**
```python
from src.lib.file_storage import file_storage

# Save upload
result = await file_storage.save_profile_picture(file)
print(result["url"])  # /uploads/profiles/uuid_hash.jpg
```

---

### Validation
**File**: `src/lib/validation.py`

Common validation utilities.

**Functions:**
- `validate_email(email)` - Validate email format
- `validate_phone(phone)` - Validate phone number
- `validate_student_number(student_number)` - Validate student number format
- `validate_employee_number(employee_number)` - Validate employee number format
- `validate_isbn(isbn)` - Validate ISBN-10/ISBN-13
- `validate_age_range(date_of_birth, min_age, max_age)` - Validate age
- `validate_academic_year(academic_year)` - Validate academic year format
- `validate_password_strength(password)` - Validate password requirements
- `sanitize_filename(filename)` - Sanitize filename for safety

**Password Requirements:**
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit
- At least one special character

---

### Logging
**File**: `src/lib/logging.py`

Structured logging configuration.

**Usage:**
```python
from src.lib.logging import get_logger

logger = get_logger(__name__)
logger.info("Operation completed", extra={"user_id": str(user_id)})
```

---

### Metrics
**File**: `src/lib/metrics.py`

Track application metrics.

**Metric Types:**
- `COUNTER` - Incrementing counter
- `GAUGE` - Value that can go up/down
- `HISTOGRAM` - Distribution of values
- `SUMMARY` - Summary statistics

**Usage:**
```python
from src.lib.metrics import track_metric, MetricType

track_metric(
    "student_created",
    value=1,
    metric_type=MetricType.COUNTER,
    labels={"department": "CS"}
)
```

---

### Audit Log
**File**: `src/lib/audit.py`

Audit trail logging.

**Actions:**
- `CREATE` - Entity created
- `UPDATE` - Entity updated
- `DELETE` - Entity deleted
- `LOGIN` - User logged in
- `LOGOUT` - User logged out
- `LOGIN_FAILED` - Failed login attempt

**Usage:**
```python
from src.lib.audit import log_audit, AuditAction

await log_audit(
    db,
    action=AuditAction.CREATE,
    entity_type="Student",
    entity_id=student.id,
    user_id=current_user.id,
    details={"student_number": student.student_number}
)
```

---

## 🖥️ CLI Commands

### Database Commands
```bash
# Initialize database
python -m src.cli db init

# Seed sample data
python -m src.cli db seed

# Reset database
python -m src.cli db reset
```

### User Commands
```bash
# Create user
python -m src.cli user create

# List users
python -m src.cli user list

# Reset password
python -m src.cli user reset-password

# Assign role
python -m src.cli user assign-role
```

### Task Commands
```bash
# Send pending notifications
python -m src.cli tasks send-notifications

# Send overdue book reminders
python -m src.cli tasks overdue-books

# Check Celery status
python -m src.cli tasks status

# List scheduled tasks
python -m src.cli tasks list-scheduled
```

---

## 🔐 Security Best Practices

1. **Authentication**
   - Use JWT tokens with expiration
   - Refresh tokens for extended sessions
   - Hash passwords with bcrypt

2. **Authorization**
   - Role-based access control (RBAC)
   - Permission-based operations
   - Validate user permissions on each request

3. **Input Validation**
   - Validate all user inputs
   - Sanitize file names
   - Use Pydantic schemas

4. **Rate Limiting**
   - Protect against abuse
   - Per-minute and per-hour limits
   - IP-based and user-based tracking

5. **Audit Logging**
   - Log all critical operations
   - Track user actions
   - Maintain audit trail

---

## 📊 Performance Optimization

1. **Database**
   - Use indexes on frequently queried fields
   - Implement query optimization
   - Use connection pooling

2. **Caching**
   - Cache frequently accessed data
   - Use Redis for session storage
   - Implement query result caching

3. **Asynchronous Operations**
   - Use async/await for I/O operations
   - Background tasks for long-running operations
   - Celery for distributed tasks

4. **File Storage**
   - Store files outside database
   - Use CDN for static files
   - Implement file size limits

---

**Last Updated**: 2024-01-15  
**Version**: 1.0.0
