# EMIS API - Complete Endpoint Reference

## Overview

Complete REST API for the Educational Management Information System (EMIS). All endpoints require JWT authentication unless specified otherwise.

**Base URL**: `http://localhost:8000`  
**API Version**: v1  
**Authentication**: Bearer Token (JWT)

---

## Table of Contents

1. [Students API](#students-api) - Student lifecycle management
2. [HR & Employees API](#hr--employees-api) - Employee management
3. [Payroll API](#payroll-api) - Salary processing
4. [Leave Management API](#leave-management-api) - Leave requests
5. [Library API](#library-api) - Library operations
6. [LMS API](#lms-api) - Learning management
7. [Finance API](#finance-api) - Financial operations
8. [Admissions API](#admissions-api) - Application processing
9. [Analytics API](#analytics-api) - Reports and dashboards
10. [Notifications API](#notifications-api) - Multi-channel notifications

---

## Authentication

All protected endpoints require a JWT token in the Authorization header:

```bash
Authorization: Bearer <your_jwt_token>
```

### Get Access Token

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

---

## Students API

**Prefix**: `/api/v1/students`

### Create Student
```http
POST /api/v1/students/
Permission: students:create

{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "date_of_birth": "2005-06-15",
  "phone": "+1234567890"
}
```

### Get Student
```http
GET /api/v1/students/{student_id}
Permission: students:read
```

### List Students
```http
GET /api/v1/students?status=active&page=1&size=20
Permission: students:read
```

### Update Student
```http
PATCH /api/v1/students/{student_id}
Permission: students:update

{
  "phone": "+9876543210",
  "address": "New Address"
}
```

### Admit Student
```http
POST /api/v1/students/{student_id}/admit
Permission: students:admit

{
  "admission_date": "2024-09-01T00:00:00Z"
}
```

### Graduate Student
```http
POST /api/v1/students/{student_id}/graduate
Permission: students:graduate

{
  "graduation_date": "2028-05-20T00:00:00Z",
  "degree_earned": "Bachelor of Science",
  "honors": "Magna Cum Laude"
}
```

---

## HR & Employees API

**Prefix**: `/api/v1/hr`

### Create Employee
```http
POST /api/v1/hr/employees
Permission: employees:create

{
  "employee_number": "EMP2024001",
  "first_name": "Alice",
  "last_name": "Johnson",
  "email": "alice@example.com",
  "date_of_joining": "2024-01-15",
  "department": "Computer Science",
  "designation": "Professor",
  "employment_type": "full-time"
}
```

### Get Employee
```http
GET /api/v1/hr/employees/{employee_id}
Permission: employees:read
```

### List Employees
```http
GET /api/v1/hr/employees?department=Engineering&page=1&size=20
Permission: employees:read
```

### Update Employee
```http
PATCH /api/v1/hr/employees/{employee_id}
Permission: employees:update

{
  "designation": "Senior Professor",
  "basic_salary": 75000
}
```

---

## Payroll API

**Prefix**: `/api/v1/hr/payroll`

### Create Payroll
```http
POST /api/v1/hr/payroll/
Permission: payroll:create

{
  "employee_id": "uuid",
  "month": "November",
  "year": 2024,
  "pay_period_start": "2024-11-01",
  "pay_period_end": "2024-11-30",
  "basic_salary": 50000,
  "hra": 10000,
  "provident_fund": 5000
}
```

### Get Payroll
```http
GET /api/v1/hr/payroll/{payroll_id}
Permission: payroll:read
```

### Process Payroll
```http
POST /api/v1/hr/payroll/{payroll_id}/process
Permission: payroll:process

{
  "payment_date": "2024-11-30"
}
```

---

## Leave Management API

**Prefix**: `/api/v1/hr/leave`

### Submit Leave Request
```http
POST /api/v1/hr/leave/
Permission: leave:create

{
  "employee_id": "uuid",
  "leave_type": "sick",
  "start_date": "2024-11-15",
  "end_date": "2024-11-17",
  "reason": "Medical appointment"
}
```

### Approve Leave
```http
PATCH /api/v1/hr/leave/{leave_id}/approve
Permission: leave:approve

{
  "comments": "Approved"
}
```

### Reject Leave
```http
PATCH /api/v1/hr/leave/{leave_id}/reject
Permission: leave:approve

{
  "reason": "Insufficient leave balance"
}
```

---

## Library API

**Prefix**: `/api/v1/library`

### Add Book
```http
POST /api/v1/library/books
Permission: library:create

{
  "isbn": "978-3-16-148410-0",
  "title": "Introduction to Algorithms",
  "author": "Thomas Cormen",
  "publisher": "MIT Press",
  "quantity": 5
}
```

### Search Books
```http
GET /api/v1/library/books/search?query=algorithms&category=Computer Science
Permission: library:read
```

### Issue Book
```http
POST /api/v1/library/books/issue
Permission: library:issue

{
  "member_id": "uuid",
  "book_id": "uuid",
  "issue_date": "2024-11-09",
  "due_date": "2024-11-23"
}
```

### Return Book
```http
POST /api/v1/library/books/return
Permission: library:return

{
  "transaction_id": "uuid",
  "return_date": "2024-11-20",
  "condition": "good"
}
```

---

## LMS API

**Prefix**: `/api/v1/lms`

### Create Course
```http
POST /api/v1/lms/courses
Permission: courses:create

{
  "course_code": "CS101",
  "course_name": "Introduction to Programming",
  "credits": 3,
  "instructor_id": "uuid",
  "academic_year": "2024-2025",
  "semester": "Fall"
}
```

### Get Course
```http
GET /api/v1/lms/courses/{course_id}
Permission: courses:read
```

### Create Assignment
```http
POST /api/v1/lms/assignments
Permission: assignments:create

{
  "course_id": "uuid",
  "title": "Homework 1",
  "description": "Complete exercises 1-10",
  "due_date": "2024-11-20T23:59:59Z",
  "max_marks": 100
}
```

### Submit Assignment
```http
POST /api/v1/lms/submissions
Permission: assignments:submit

{
  "assignment_id": "uuid",
  "student_id": "uuid",
  "submission_text": "My solution...",
  "attachment_url": "https://..."
}
```

### Enroll Student
```http
POST /api/v1/lms/courses/{course_id}/enroll/{student_id}
Permission: courses:enroll
```

---

## Finance API

**Prefix**: `/api/v1/finance`

### Create Fee Structure
```http
POST /api/v1/finance/fee-structures
Permission: finance:create

{
  "program_id": "uuid",
  "academic_year": "2024-2025",
  "semester": "Fall",
  "tuition_fee": 50000,
  "library_fee": 2000,
  "exam_fee": 1000
}
```

### Record Payment
```http
POST /api/v1/finance/payments
Permission: payments:create

{
  "student_id": "uuid",
  "amount": 25000,
  "payment_method": "bank_transfer",
  "payment_date": "2024-11-09",
  "fee_type": "tuition"
}
```

### Get Student Balance
```http
GET /api/v1/finance/students/{student_id}/balance
Permission: finance:read
```

### Award Scholarship
```http
POST /api/v1/finance/scholarships
Permission: scholarships:create

{
  "student_id": "uuid",
  "scholarship_name": "Merit Scholarship",
  "amount": 10000,
  "academic_year": "2024-2025"
}
```

---

## Admissions API

**Prefix**: `/api/v1/admissions`

### Submit Application
```http
POST /api/v1/admissions/applications
No authentication required

{
  "first_name": "John",
  "last_name": "Smith",
  "email": "john@example.com",
  "phone": "+1234567890",
  "date_of_birth": "2005-03-15",
  "program_id": "uuid",
  "academic_year": "2024-2025"
}
```

### Review Application
```http
PATCH /api/v1/admissions/applications/{application_id}/review
Permission: admissions:review

{
  "status": "shortlisted",
  "comments": "Strong candidate",
  "interview_date": "2024-11-20"
}
```

### Approve Application
```http
POST /api/v1/admissions/applications/{application_id}/approve
Permission: admissions:approve
```

### List Applications
```http
GET /api/v1/admissions/applications?status=pending&page=1&size=20
Permission: admissions:read
```

---

## Analytics API

**Prefix**: `/api/v1/analytics`

### Get Dashboard
```http
GET /api/v1/analytics/dashboard
Permission: analytics:read
```

### Enrollment Report
```http
GET /api/v1/analytics/reports/enrollment?start_date=2024-01-01&end_date=2024-12-31
Permission: analytics:read
```

### Attendance Report
```http
GET /api/v1/analytics/reports/attendance?start_date=2024-11-01&end_date=2024-11-30
Permission: analytics:read
```

### Financial Report
```http
GET /api/v1/analytics/reports/financial?start_date=2024-01-01&end_date=2024-12-31
Permission: analytics:financial
```

### Performance Report
```http
GET /api/v1/analytics/reports/performance?academic_year=2024-2025
Permission: analytics:read
```

### Download Report
```http
GET /api/v1/analytics/reports/{report_id}/download?format=pdf
Permission: analytics:read
```

---

## Notifications API

**Prefix**: `/api/v1/notifications`

### Send Notification
```http
POST /api/v1/notifications/send
Permission: notifications:send

{
  "recipient_id": "uuid",
  "recipient_type": "student",
  "channel": "email",
  "subject": "Important Announcement",
  "message": "Classes will resume on...",
  "priority": "high"
}
```

### Send Bulk Notification
```http
POST /api/v1/notifications/send-bulk
Permission: notifications:send

{
  "recipient_ids": ["uuid1", "uuid2"],
  "recipient_type": "student",
  "channel": "sms",
  "subject": "Reminder",
  "message": "Exam tomorrow"
}
```

### Get My Notifications
```http
GET /api/v1/notifications/my-notifications?unread_only=true&page=1&size=20
Permission: notifications:read
```

### Mark as Read
```http
PATCH /api/v1/notifications/{notification_id}/read
Permission: notifications:read
```

### Schedule Notification
```http
POST /api/v1/notifications/schedule
Permission: notifications:send

{
  "recipient_id": "uuid",
  "channel": "email",
  "subject": "Reminder",
  "message": "Payment due tomorrow",
  "scheduled_time": "2024-11-10T09:00:00Z"
}
```

---

## Common Response Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `204 No Content` - Successful deletion
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error

## Error Response Format

```json
{
  "detail": "Error message",
  "error_code": "ERROR_CODE",
  "fields": {
    "field_name": "Validation error"
  }
}
```

---

## Interactive Documentation

Visit these URLs when the server is running:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

## Testing with cURL

```bash
# Get token
TOKEN=$(curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}' \
  | jq -r '.access_token')

# Use token
curl -X GET http://localhost:8000/api/v1/students \
  -H "Authorization: Bearer $TOKEN"
```

---

**Total Endpoints**: 60+  
**Modules Covered**: 10  
**Authentication**: JWT with RBAC  
**Documentation**: Auto-generated OpenAPI
