# EMIS API Endpoints Reference

Base URL: `http://localhost:8000/api/v1/`

## Authentication
- `POST /auth/register/` - Register new user
- `POST /auth/login/` - Login and get JWT tokens
- `POST /auth/logout/` - Logout
- `GET /auth/me/` - Get current user profile
- `POST /auth/refresh/` - Refresh access token

## Health & Monitoring
- `GET /health/` - Health check
- `GET /readiness/` - Readiness check
- `GET /liveness/` - Liveness check
- `GET /metrics/` - Application metrics

## Admissions
- `/admissions/applications/` - CRUD for applications
- `/admissions/applications/{id}/approve/` - Approve application
- `/admissions/applications/{id}/reject/` - Reject application
- `/admissions/applications/statistics/` - Get statistics
- `/admissions/merit-lists/` - CRUD for merit lists
- `/admissions/merit-lists/{id}/publish/` - Publish merit list

## Analytics
- `/analytics/metrics/` - Dashboard metrics
- `/analytics/metrics/refresh/` - Refresh specific metric
- `/analytics/reports/` - Generated reports
- `/analytics/reports/{id}/generate/` - Trigger report generation

## Attendance
- `/attendance/sessions/` - Attendance sessions
- `/attendance/sessions/today/` - Today's sessions
- `/attendance/records/` - Attendance records
- `/attendance/records/bulk_mark/` - Bulk mark attendance
- `/attendance/records/statistics/` - Attendance statistics

## Courses
- `/courses/courses/` - CRUD for courses
- `/courses/courses/{id}/modules/` - Get course modules
- `/courses/courses/{id}/assignments/` - Get course assignments
- `/courses/modules/` - CRUD for modules
- `/courses/assignments/` - CRUD for assignments
- `/courses/assignments/{id}/submissions/` - Get assignment submissions
- `/courses/submissions/` - CRUD for submissions
- `/courses/submissions/{id}/grade/` - Grade a submission
- `/courses/grades/` - Grade records

## Students
- `/students/students/` - CRUD for students
- `/students/students/{id}/profile/` - Detailed student profile
- `/students/students/{id}/enrollments/` - Student enrollments
- `/students/students/{id}/attendance/` - Student attendance
- `/students/students/statistics/` - Student statistics

## Timetable
- `/timetable/academic-years/` - Academic years
- `/timetable/semesters/` - Semesters
- `/timetable/timeslots/` - Time slots
- `/timetable/rooms/` - Room management
- `/timetable/entries/` - Timetable entries
- `/timetable/exceptions/` - Timetable exceptions

## Transport
- `/transport/vehicles/` - Vehicle management
- `/transport/routes/` - Route management
- `/transport/routes/{id}/stops/` - Route stops
- `/transport/stops/` - All stops
- `/transport/drivers/` - Driver management
- `/transport/assignments/` - Student transport assignments
- `/transport/maintenance/` - Vehicle maintenance records
- `/transport/fuel-logs/` - Fuel consumption logs

## Finance
- `/finance/fee-structures/` - Fee structures
- `/finance/invoices/` - Student invoices
- `/finance/invoices/statistics/` - Invoice statistics
- `/finance/payments/` - Payment records

## Faculty
- Existing API endpoints (already implemented)

## Exams
- Existing API endpoints (already implemented)

## Library
- Existing API endpoints (already implemented)

## HR
- Existing API endpoints (already implemented)

## Hostel
- Existing API endpoints (already implemented)

## Inventory
- Existing API endpoints (already implemented)

## LMS
- Existing API endpoints (already implemented)

## Notifications
- Existing API endpoints (already implemented)

## Reports
- Existing API endpoints (already implemented)

## CMS
- `/cms/` - Content management (basic structure)

## API Documentation
- `/api/schema/` - OpenAPI schema
- `/api/docs/` - Swagger UI
- `/api/redoc/` - ReDoc documentation

## Standard REST Operations

All resource endpoints support:
- `GET /resource/` - List all
- `POST /resource/` - Create new
- `GET /resource/{id}/` - Retrieve specific
- `PUT /resource/{id}/` - Full update
- `PATCH /resource/{id}/` - Partial update
- `DELETE /resource/{id}/` - Delete

## Common Query Parameters
- `?page=1` - Pagination
- `?page_size=20` - Items per page
- `?search=term` - Search
- `?ordering=-created_at` - Sort order
- `?{field}={value}` - Filter by field

## Authentication
All endpoints (except public ones like registration) require:
```
Authorization: Bearer {access_token}
```

## Response Format
Success responses return JSON:
```json
{
  "id": 1,
  "field": "value",
  ...
}
```

Error responses:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Error description"
  }
}
```
