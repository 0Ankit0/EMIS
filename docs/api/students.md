# Students API Documentation

## Overview

The Students API provides endpoints for managing the complete student lifecycle from admission to graduation and alumni status.

**Base URL**: `/api/v1/students`

## Authentication

All endpoints require JWT authentication with appropriate permissions.

## Endpoints

### Create Student

Create a new student record.

**Endpoint**: `POST /api/v1/students/`

**Permission**: `students:create`

**Request Body**:
```json
{
  "first_name": "John",
  "middle_name": "Michael",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "phone": "+1234567890",
  "date_of_birth": "2005-06-15",
  "gender": "male",
  "nationality": "Indian",
  "address": "123 Main St, City, State"
}
```

**Response** (201 Created):
```json
{
  "id": "uuid",
  "student_number": "2024000001",
  "first_name": "John",
  "middle_name": "Michael",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "phone": "+1234567890",
  "date_of_birth": "2005-06-15",
  "gender": "male",
  "status": "applicant",
  "admission_date": null,
  "created_at": "2024-11-09T12:00:00Z"
}
```

**Errors**:
- `409 Conflict`: Student with email already exists
- `422 Unprocessable Entity`: Validation error

---

### Get Student

Retrieve a student by ID.

**Endpoint**: `GET /api/v1/students/{student_id}`

**Permission**: `students:read`

**Response** (200 OK):
```json
{
  "id": "uuid",
  "student_number": "2024000001",
  "first_name": "John",
  "middle_name": "Michael",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "status": "active",
  "admission_date": "2024-09-01T00:00:00Z",
  "created_at": "2024-11-09T12:00:00Z"
}
```

**Errors**:
- `404 Not Found`: Student not found

---

### List Students

List students with pagination and filters.

**Endpoint**: `GET /api/v1/students/`

**Permission**: `students:read`

**Query Parameters**:
- `status` (optional): Filter by student status (`applicant`, `active`, `suspended`, `withdrawn`, `graduated`, `alumni`)
- `page` (optional, default=1): Page number
- `size` (optional, default=20, max=100): Items per page

**Response** (200 OK):
```json
{
  "items": [
    {
      "id": "uuid",
      "student_number": "2024000001",
      "first_name": "John",
      "last_name": "Doe",
      "email": "john.doe@example.com",
      "status": "active"
    }
  ],
  "total": 100,
  "page": 1,
  "size": 20
}
```

---

### Update Student

Update student information.

**Endpoint**: `PATCH /api/v1/students/{student_id}`

**Permission**: `students:update`

**Request Body**:
```json
{
  "phone": "+9876543210",
  "address": "456 New Address",
  "emergency_contact_name": "Jane Doe",
  "emergency_contact_phone": "+1122334455"
}
```

**Response** (200 OK): Updated student object

**Errors**:
- `404 Not Found`: Student not found
- `400 Bad Request`: No fields to update

---

### Delete Student

Soft delete a student (sets status to withdrawn).

**Endpoint**: `DELETE /api/v1/students/{student_id}`

**Permission**: `students:delete`

**Response** (204 No Content)

**Errors**:
- `404 Not Found`: Student not found

---

### Admit Student

Admit a student (transition from applicant to active status).

**Endpoint**: `POST /api/v1/students/{student_id}/admit`

**Permission**: `students:admit`

**Request Body**:
```json
{
  "admission_date": "2024-09-01T00:00:00Z"
}
```

**Response** (200 OK): Updated student with active status

**Errors**:
- `404 Not Found`: Student not found or cannot be admitted

---

### Graduate Student

Graduate a student.

**Endpoint**: `POST /api/v1/students/{student_id}/graduate`

**Permission**: `students:graduate`

**Request Body**:
```json
{
  "graduation_date": "2028-05-20T00:00:00Z",
  "degree_earned": "Bachelor of Science in Computer Science",
  "honors": "Magna Cum Laude"
}
```

**Response** (200 OK): Updated student with graduated status

**Errors**:
- `404 Not Found`: Student not found or cannot be graduated

---

### Get Student GPA

Get a student's cumulative GPA.

**Endpoint**: `GET /api/v1/students/{student_id}/gpa`

**Permission**: `students:read`

**Response** (200 OK):
```json
{
  "student_id": "uuid",
  "cumulative_gpa": 3.75
}
```

**Errors**:
- `404 Not Found`: Student not found or no academic records

---

## Student Status Transitions

The student status follows this lifecycle:

```
APPLICANT → ACTIVE → GRADUATED → ALUMNI
    ↓          ↓
  [END]    SUSPENDED → ACTIVE
              ↓
          WITHDRAWN
```

- **APPLICANT**: Initial status when student record is created
- **ACTIVE**: Student is admitted and actively enrolled
- **SUSPENDED**: Temporarily suspended (can be reactivated)
- **WITHDRAWN**: Permanently withdrawn
- **GRADUATED**: Completed program successfully
- **ALUMNI**: Former student (converted from graduated)

## Permissions

Required permissions for each operation:

| Operation | Permission |
|-----------|-----------|
| Create student | `students:create` |
| Read student | `students:read` |
| Update student | `students:update` |
| Delete student | `students:delete` |
| Admit student | `students:admit` |
| Graduate student | `students:graduate` |

## Error Responses

All endpoints may return these common errors:

**401 Unauthorized**:
```json
{
  "error": "Unauthorized",
  "detail": "Could not validate credentials"
}
```

**403 Forbidden**:
```json
{
  "error": "Forbidden",
  "detail": "Permission denied. Required: students:read"
}
```

**422 Unprocessable Entity**:
```json
{
  "error": "Validation Error",
  "detail": "Request validation failed",
  "fields": {
    "email": "field required",
    "date_of_birth": "invalid date format"
  }
}
```

**500 Internal Server Error**:
```json
{
  "error": "Internal Server Error",
  "detail": "An unexpected error occurred"
}
```

## Examples

### Complete Student Lifecycle

```bash
# 1. Create student
curl -X POST http://localhost:8000/api/v1/students/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "date_of_birth": "2005-06-15"
  }'

# 2. Admit student
curl -X POST http://localhost:8000/api/v1/students/{student_id}/admit \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"admission_date": "2024-09-01T00:00:00Z"}'

# 3. Get student info
curl -X GET http://localhost:8000/api/v1/students/{student_id} \
  -H "Authorization: Bearer $TOKEN"

# 4. Graduate student
curl -X POST http://localhost:8000/api/v1/students/{student_id}/graduate \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "graduation_date": "2028-05-20T00:00:00Z",
    "degree_earned": "Bachelor of Science",
    "honors": "Magna Cum Laude"
  }'
```
