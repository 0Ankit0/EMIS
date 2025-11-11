# 📚 EMIS API Documentation - Complete

**Version**: 1.0.0  
**Base URL**: `http://localhost:8000/api/v1`  
**Authentication**: JWT Bearer Token

---

## 🔐 Authentication

### POST /auth/login
Login to get access token.

**Request:**
```json
{
  "email": "user@emis.edu",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

### POST /auth/refresh
Refresh access token.

**Request:**
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### POST /auth/logout
Logout and invalidate token.

### POST /auth/change-password
Change current user password.

**Request:**
```json
{
  "old_password": "old_pass",
  "new_password": "new_pass"
}
```

---

## 👨‍🎓 Students

### GET /students
List all students.

**Query Parameters:**
- `page` (int): Page number (default: 1)
- `page_size` (int): Items per page (default: 50)
- `status` (string): Filter by status
- `search` (string): Search by name/email

**Response:**
```json
{
  "items": [
    {
      "id": "uuid",
      "student_number": "STU2024001",
      "first_name": "John",
      "last_name": "Doe",
      "email": "john.doe@emis.edu",
      "status": "active",
      "program_id": "uuid",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 100,
  "page": 1,
  "page_size": 50
}
```

### POST /students
Create a new student.

**Request:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@emis.edu",
  "phone": "+1234567890",
  "date_of_birth": "2000-01-01",
  "gender": "male",
  "nationality": "US",
  "address": "123 Main St"
}
```

### GET /students/{id}
Get student details.

### PUT /students/{id}
Update student information.

### DELETE /students/{id}
Delete student (soft delete).

### GET /students/{id}/courses
Get student's enrolled courses.

### GET /students/{id}/grades
Get student's academic records.

### GET /students/{id}/attendance
Get student's attendance records.

---

## 👨‍💼 HR & Employees

### GET /hr/employees
List all employees.

**Query Parameters:**
- `department` (string): Filter by department
- `status` (string): Filter by status
- `employment_type` (string): Filter by type

### POST /hr/employees
Create a new employee.

**Request:**
```json
{
  "employee_number": "EMP2024001",
  "first_name": "Jane",
  "last_name": "Smith",
  "email": "jane.smith@emis.edu",
  "department": "Computer Science",
  "designation": "Professor",
  "employment_type": "full-time",
  "date_of_joining": "2024-01-01",
  "basic_salary": 75000
}
```

### GET /hr/employees/{id}
Get employee details.

### PUT /hr/employees/{id}
Update employee information.

### GET /hr/employees/{id}/payroll
Get employee payroll history.

### POST /hr/payroll/process
Process monthly payroll.

**Request:**
```json
{
  "month": 1,
  "year": 2024,
  "employee_ids": ["uuid1", "uuid2"]
}
```

### GET /hr/leave
List leave requests.

### POST /hr/leave
Submit leave request.

**Request:**
```json
{
  "employee_id": "uuid",
  "leave_type": "sick",
  "start_date": "2024-01-15",
  "end_date": "2024-01-17",
  "reason": "Medical appointment"
}
```

### PUT /hr/leave/{id}/approve
Approve leave request.

### PUT /hr/leave/{id}/reject
Reject leave request.

### GET /hr/performance-reviews
List performance reviews.

### POST /hr/performance-reviews
Create performance review.

---

## 📚 Courses & LMS

### GET /lms/courses
List all courses.

**Query Parameters:**
- `academic_year` (string): Filter by academic year
- `semester` (string): Filter by semester
- `department` (string): Filter by department

### POST /lms/courses
Create a new course.

**Request:**
```json
{
  "course_code": "CS101",
  "course_name": "Introduction to Programming",
  "credits": 3,
  "instructor_id": "uuid",
  "academic_year": "2024-2025",
  "semester": "Fall",
  "description": "Basic programming concepts",
  "max_students": 50
}
```

### GET /lms/courses/{id}
Get course details.

### PUT /lms/courses/{id}
Update course information.

### POST /lms/courses/{id}/enroll
Enroll student in course.

**Request:**
```json
{
  "student_id": "uuid"
}
```

### GET /lms/courses/{id}/students
Get enrolled students.

### GET /lms/courses/{id}/assignments
Get course assignments.

### POST /lms/assignments
Create assignment.

**Request:**
```json
{
  "course_id": "uuid",
  "title": "Programming Assignment 1",
  "description": "Implement a sorting algorithm",
  "due_date": "2024-02-15T23:59:59Z",
  "max_marks": 100,
  "attachment_url": "https://..."
}
```

### POST /lms/assignments/{id}/submit
Submit assignment.

**Request:**
```json
{
  "student_id": "uuid",
  "submission_text": "Solution description",
  "attachment_url": "https://..."
}
```

### PUT /lms/submissions/{id}/grade
Grade assignment submission.

**Request:**
```json
{
  "marks_obtained": 95,
  "feedback": "Excellent work!"
}
```

---

## 📖 Library

### GET /library/books
Search and list books.

**Query Parameters:**
- `search` (string): Search by title/author/ISBN
- `category` (string): Filter by category
- `available_only` (boolean): Show only available books

### POST /library/books
Add new book to library.

**Request:**
```json
{
  "isbn": "978-0132350884",
  "title": "Clean Code",
  "author": "Robert C. Martin",
  "publisher": "Prentice Hall",
  "publication_year": 2008,
  "category": "Software Engineering",
  "total_copies": 5,
  "shelf_location": "A-101"
}
```

### GET /library/books/{id}
Get book details.

### POST /library/books/{id}/issue
Issue book to borrower.

**Request:**
```json
{
  "borrower_id": "uuid",
  "borrower_type": "student",
  "due_date": "2024-02-01"
}
```

### POST /library/transactions/{id}/return
Return book.

**Request:**
```json
{
  "condition_notes": "Good condition",
  "fine_amount": 0
}
```

### POST /library/transactions/{id}/renew
Renew book loan.

### GET /library/transactions/overdue
Get overdue books.

### GET /library/transactions/history
Get borrower's transaction history.

**Query Parameters:**
- `borrower_id` (uuid): Borrower UUID
- `borrower_type` (string): "student" or "employee"

---

## 💰 Finance

### GET /finance/programs
List academic programs.

### POST /finance/programs
Create academic program.

**Request:**
```json
{
  "program_code": "CS-BSC",
  "program_name": "Bachelor of Science in Computer Science",
  "degree_level": "Undergraduate",
  "duration_years": 4,
  "department": "Computer Science"
}
```

### GET /finance/fee-structures
List fee structures.

**Query Parameters:**
- `program_id` (uuid): Filter by program
- `academic_year` (string): Filter by academic year

### POST /finance/fee-structures
Create fee structure.

**Request:**
```json
{
  "program_id": "uuid",
  "academic_year": "2024-2025",
  "semester": "Fall",
  "tuition_fee": 5000,
  "lab_fee": 500,
  "library_fee": 200,
  "sports_fee": 100,
  "other_fees": 200
}
```

### GET /finance/payments
List payments.

**Query Parameters:**
- `student_id` (uuid): Filter by student
- `status` (string): Filter by status

### POST /finance/payments
Record payment.

**Request:**
```json
{
  "student_id": "uuid",
  "fee_structure_id": "uuid",
  "amount": 5800,
  "payment_method": "card",
  "transaction_id": "TXN123456",
  "payment_date": "2024-01-15"
}
```

### GET /finance/students/{id}/fee-status
Get student's fee payment status.

**Query Parameters:**
- `academic_year` (string): Academic year
- `semester` (string): Semester (optional)

**Response:**
```json
{
  "student_id": "uuid",
  "student_number": "STU2024001",
  "academic_year": "2024-2025",
  "semester": "Fall",
  "total_fee": 6000,
  "total_paid": 5800,
  "total_scholarship": 1000,
  "balance": -800
}
```

### GET /finance/scholarships
List scholarships.

### POST /finance/scholarships
Award scholarship.

**Request:**
```json
{
  "student_id": "uuid",
  "scholarship_name": "Merit Scholarship",
  "amount": 1000,
  "academic_year": "2024-2025",
  "description": "Academic excellence"
}
```

---

## 📝 Admissions

### GET /admissions/applications
List applications.

**Query Parameters:**
- `status` (string): Filter by status
- `academic_year` (string): Filter by academic year
- `program_id` (uuid): Filter by program

### POST /admissions/applications
Submit application.

**Request:**
```json
{
  "program_id": "uuid",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@email.com",
  "phone": "+1234567890",
  "date_of_birth": "2000-01-01",
  "academic_year": "2024-2025",
  "previous_education": {
    "high_school": "ABC High School",
    "gpa": 3.8
  },
  "documents": {
    "transcript": "url_to_transcript",
    "certificate": "url_to_certificate"
  }
}
```

### GET /admissions/applications/{id}
Get application details.

### PUT /admissions/applications/{id}/status
Update application status.

**Request:**
```json
{
  "status": "approved",
  "comments": "Application approved"
}
```

### POST /admissions/applications/{id}/approve
Approve application and create student.

### POST /admissions/applications/{id}/reject
Reject application.

**Request:**
```json
{
  "rejection_reason": "Does not meet minimum requirements"
}
```

### POST /admissions/applications/{id}/schedule-interview
Schedule interview.

**Request:**
```json
{
  "interview_date": "2024-01-20T10:00:00Z"
}
```

---

## 🔔 Notifications

### GET /notifications
Get user notifications.

**Query Parameters:**
- `unread_only` (boolean): Show only unread
- `limit` (int): Maximum notifications to return

**Response:**
```json
{
  "items": [
    {
      "id": "uuid",
      "title": "Assignment Due",
      "message": "Your assignment is due tomorrow",
      "channel": "in_app",
      "priority": "normal",
      "read_at": null,
      "created_at": "2024-01-15T10:00:00Z"
    }
  ]
}
```

### POST /notifications/mark-read/{id}
Mark notification as read.

### POST /notifications/send
Send notification (admin only).

**Request:**
```json
{
  "recipient_ids": ["uuid1", "uuid2"],
  "title": "System Maintenance",
  "message": "System will be down for maintenance",
  "channel": "email",
  "priority": "high"
}
```

### POST /notifications/send-template
Send notification from template.

**Request:**
```json
{
  "recipient_id": "uuid",
  "template_code": "WELCOME_EMAIL",
  "variables": {
    "name": "John Doe",
    "student_number": "STU2024001"
  },
  "channel": "email"
}
```

---

## 📊 Analytics

### GET /analytics/dashboard
Get dashboard statistics.

**Response:**
```json
{
  "total_students": 1500,
  "total_employees": 250,
  "total_courses": 120,
  "active_enrollments": 4500,
  "pending_applications": 45,
  "overdue_books": 12
}
```

### GET /analytics/students/enrollment-trends
Get student enrollment trends.

**Query Parameters:**
- `start_date` (string): Start date
- `end_date` (string): End date

### GET /analytics/finance/revenue
Get revenue statistics.

### GET /analytics/courses/performance
Get course performance metrics.

---

## 🏥 Health & Monitoring

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:00:00Z",
  "version": "1.0.0",
  "database": "connected",
  "cache": "connected"
}
```

### GET /metrics
Prometheus metrics endpoint.

---

## 📄 Common Response Formats

### Success Response
```json
{
  "success": true,
  "data": {...},
  "message": "Operation successful"
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "email": ["Invalid email format"]
    }
  }
}
```

### Pagination
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "page_size": 50,
  "pages": 2
}
```

---

## 🔒 Authentication & Authorization

All endpoints (except `/auth/login` and `/health`) require authentication.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Permissions:**
- `student.*` - Student operations
- `employee.*` - Employee operations
- `course.*` - Course operations
- `finance.*` - Finance operations
- `library.*` - Library operations
- `admin.*` - Administrative operations

---

## 📋 Rate Limiting

- **Per Minute**: 60 requests
- **Per Hour**: 1000 requests

**Headers:**
```
X-RateLimit-Limit-Minute: 60
X-RateLimit-Remaining-Minute: 45
X-RateLimit-Limit-Hour: 1000
X-RateLimit-Remaining-Hour: 850
```

When rate limit is exceeded:
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Please try again later."
  }
}
```

---

## 🔧 Error Codes

- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `409` - Conflict
- `422` - Validation Error
- `429` - Rate Limit Exceeded
- `500` - Internal Server Error

---

**Generated**: 2024-01-15  
**Last Updated**: 2024-01-15

For more information, visit the OpenAPI documentation at `/docs`
