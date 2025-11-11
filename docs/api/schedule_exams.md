# Schedule and Exam API Documentation

## Overview

This document describes the REST API endpoints for managing class schedules, exams, marks, and result sheets in the EMIS system.

**Base URL**: `/api/v1`

## Authentication

All endpoints require authentication via JWT token in the Authorization header:
```
Authorization: Bearer <token>
```

## Permissions

Each endpoint requires specific permissions as noted in the endpoint descriptions.

---

## Class Schedule Endpoints

### 1. Create Class Schedule

**Endpoint**: `POST /schedules/`

**Description**: Create a new class schedule entry

**Required Permission**: `schedule:create`

**Request Body**:
```json
{
  "course_id": 1,
  "instructor_id": 5,
  "day_of_week": "monday",
  "start_time": "09:00:00",
  "end_time": "10:30:00",
  "effective_from": "2024-01-15",
  "room_number": "A-101",
  "building": "Main Block",
  "effective_to": "2024-05-30",
  "notes": "Optional notes"
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "course_id": 1,
  "instructor_id": 5,
  "room_number": "A-101",
  "building": "Main Block",
  "day_of_week": "monday",
  "start_time": "09:00:00",
  "end_time": "10:30:00",
  "effective_from": "2024-01-15",
  "effective_to": "2024-05-30",
  "is_active": true,
  "notes": "Optional notes"
}
```

**Error Responses**:
- `409 Conflict`: Schedule conflict detected for instructor or room
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Insufficient permissions

---

### 2. Get Schedule by ID

**Endpoint**: `GET /schedules/{schedule_id}`

**Description**: Retrieve a specific schedule by ID

**Required Permission**: `schedule:read`

**Response** (200 OK):
```json
{
  "id": 1,
  "course_id": 1,
  "instructor_id": 5,
  "room_number": "A-101",
  "building": "Main Block",
  "day_of_week": "monday",
  "start_time": "09:00:00",
  "end_time": "10:30:00",
  "effective_from": "2024-01-15",
  "effective_to": "2024-05-30",
  "is_active": true,
  "notes": "Optional notes"
}
```

**Error Responses**:
- `404 Not Found`: Schedule not found

---

### 3. Get Schedules by Course

**Endpoint**: `GET /schedules/course/{course_id}`

**Description**: Get all schedules for a specific course

**Required Permission**: `schedule:read`

**Query Parameters**:
- `active_only` (boolean, default: true): Return only active schedules

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "course_id": 1,
    "day_of_week": "monday",
    "start_time": "09:00:00",
    "end_time": "10:30:00",
    ...
  }
]
```

---

### 4. Get Schedules by Instructor

**Endpoint**: `GET /schedules/instructor/{instructor_id}`

**Description**: Get all schedules for a specific instructor

**Required Permission**: `schedule:read`

**Query Parameters**:
- `active_only` (boolean, default: true): Return only active schedules

---

### 5. Get Schedules by Day

**Endpoint**: `GET /schedules/day/{day}`

**Description**: Get all schedules for a specific day of week

**Required Permission**: `schedule:read`

**Path Parameters**:
- `day`: One of: `monday`, `tuesday`, `wednesday`, `thursday`, `friday`, `saturday`, `sunday`

**Query Parameters**:
- `active_only` (boolean, default: true): Return only active schedules

---

### 6. Update Schedule

**Endpoint**: `PUT /schedules/{schedule_id}`

**Description**: Update an existing schedule

**Required Permission**: `schedule:update`

**Request Body** (all fields optional):
```json
{
  "instructor_id": 6,
  "day_of_week": "tuesday",
  "start_time": "10:00:00",
  "end_time": "11:30:00",
  "room_number": "B-201",
  "building": "New Block",
  "effective_to": "2024-06-30",
  "notes": "Updated notes",
  "is_active": false
}
```

**Response** (200 OK): Updated schedule object

**Error Responses**:
- `404 Not Found`: Schedule not found
- `409 Conflict`: Schedule conflict detected

---

### 7. Delete Schedule

**Endpoint**: `DELETE /schedules/{schedule_id}`

**Description**: Delete a schedule

**Required Permission**: `schedule:delete`

**Response** (204 No Content): Empty response

**Error Responses**:
- `404 Not Found`: Schedule not found

---

## Exam Endpoints

### 1. Create Exam

**Endpoint**: `POST /exams/`

**Description**: Create a new exam

**Required Permission**: `exam:create`

**Request Body**:
```json
{
  "course_id": 1,
  "exam_name": "Midterm Exam - Mathematics",
  "exam_type": "midterm",
  "exam_code": "MATH101-MT-2024",
  "exam_date": "2024-03-15",
  "start_time": "2024-03-15T10:00:00",
  "end_time": "2024-03-15T12:00:00",
  "duration_minutes": 120,
  "max_marks": 100,
  "passing_marks": 40,
  "weightage_percentage": 30.0,
  "venue": "Exam Hall A",
  "room_number": "EH-A-01",
  "instructions": "Bring calculator and ID card",
  "syllabus_topics": "Chapters 1-5"
}
```

**Exam Types**:
- `internal`, `external`, `midterm`, `final`, `assignment`, `quiz`, `practical`, `viva`

**Response** (201 Created):
```json
{
  "id": 1,
  "course_id": 1,
  "exam_name": "Midterm Exam - Mathematics",
  "exam_type": "midterm",
  "exam_code": "MATH101-MT-2024",
  "exam_date": "2024-03-15",
  "start_time": "2024-03-15T10:00:00",
  "end_time": "2024-03-15T12:00:00",
  "duration_minutes": 120,
  "max_marks": 100,
  "passing_marks": 40,
  "status": "scheduled"
}
```

**Error Responses**:
- `409 Conflict`: Exam code already exists

---

### 2. Get Exam by ID

**Endpoint**: `GET /exams/{exam_id}`

**Description**: Retrieve a specific exam by ID

**Required Permission**: `exam:read`

**Response** (200 OK): Exam object

**Error Responses**:
- `404 Not Found`: Exam not found

---

### 3. Get Exams by Course

**Endpoint**: `GET /exams/course/{course_id}`

**Description**: Get all exams for a specific course

**Required Permission**: `exam:read`

**Query Parameters**:
- `active_only` (boolean, default: true): Return only active exams

**Response** (200 OK): Array of exam objects

---

### 4. Get Upcoming Exams

**Endpoint**: `GET /exams/upcoming`

**Description**: Get upcoming exams

**Required Permission**: `exam:read`

**Query Parameters**:
- `days` (integer, default: 7): Number of days to look ahead

**Response** (200 OK): Array of upcoming exam objects

---

## Marks Endpoints

### 1. Create Marks Entry

**Endpoint**: `POST /exams/{exam_id}/marks`

**Description**: Create marks entry for a student in an exam

**Required Permission**: `marks:create`

**Request Body**:
```json
{
  "student_id": 10,
  "exam_id": 1,
  "enrollment_id": 5,
  "marks_obtained": 85.5,
  "max_marks": 100,
  "is_absent": false,
  "remarks": "Good performance"
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "student_id": 10,
  "exam_id": 1,
  "enrollment_id": 5,
  "marks_obtained": 85.5,
  "max_marks": 100,
  "grade": "A",
  "grade_points": 9.0,
  "status": "pending",
  "is_absent": false
}
```

**Error Responses**:
- `400 Bad Request`: Exam ID mismatch

---

### 2. Update Marks

**Endpoint**: `PUT /exams/marks/{marks_id}`

**Description**: Update marks for a student

**Required Permission**: `marks:update`

**Request Body**:
```json
{
  "marks_obtained": 87.5,
  "evaluator_comments": "Improved after re-evaluation"
}
```

**Response** (200 OK): Updated marks object

**Error Responses**:
- `404 Not Found`: Marks not found

---

### 3. Verify Marks

**Endpoint**: `POST /exams/marks/{marks_id}/verify`

**Description**: Verify marks (must be submitted first)

**Required Permission**: `marks:verify`

**Response** (200 OK): Verified marks object

**Error Responses**:
- `404 Not Found`: Marks not found or not submitted

---

### 4. Publish Marks

**Endpoint**: `POST /exams/marks/{marks_id}/publish`

**Description**: Publish marks (must be verified first)

**Required Permission**: `marks:publish`

**Response** (200 OK): Published marks object

**Error Responses**:
- `404 Not Found`: Marks not found or not verified

---

### 5. Bulk Publish Marks

**Endpoint**: `POST /exams/{exam_id}/marks/publish-all`

**Description**: Publish all verified marks for an exam

**Required Permission**: `marks:publish`

**Response** (200 OK):
```json
{
  "published_count": 45
}
```

---

### 6. Get Exam Marks

**Endpoint**: `GET /exams/{exam_id}/marks`

**Description**: Get all marks for an exam

**Required Permission**: `marks:read`

**Response** (200 OK): Array of marks objects

---

### 7. Get Student Marks

**Endpoint**: `GET /exams/student/{student_id}/marks`

**Description**: Get all marks for a student across all exams

**Required Permission**: `marks:read`

**Response** (200 OK): Array of marks objects

---

## Result Sheet Endpoints

### 1. Generate Result Sheet

**Endpoint**: `POST /exams/results/generate`

**Description**: Generate a consolidated result sheet for a student

**Required Permission**: `result:generate`

**Query Parameters**:
- `student_id` (integer, required): Student ID
- `enrollment_id` (integer, required): Enrollment ID
- `result_type` (string, required): One of `semester`, `annual`, `cumulative`, `transcript`, `provisional`, `final`
- `academic_year` (string, required): Academic year (e.g., "2023-2024")
- `semester` (integer, optional): Semester number

**Response** (201 Created):
```json
{
  "id": 1,
  "student_id": 10,
  "enrollment_id": 5,
  "result_type": "semester",
  "academic_year": "2023-2024",
  "semester": 1,
  "total_marks_obtained": 425.5,
  "total_max_marks": 500,
  "percentage": 85.1,
  "cgpa": 8.5,
  "sgpa": 8.7,
  "is_passed": true,
  "has_backlogs": false,
  "status": "draft"
}
```

---

### 2. Get Result by ID

**Endpoint**: `GET /exams/results/{result_id}`

**Description**: Retrieve a specific result sheet by ID

**Required Permission**: `result:read`

**Response** (200 OK): Result sheet object

**Error Responses**:
- `404 Not Found`: Result not found

---

### 3. Get Student Results

**Endpoint**: `GET /exams/student/{student_id}/results`

**Description**: Get all result sheets for a student

**Required Permission**: `result:read`

**Query Parameters**:
- `published_only` (boolean, default: false): Return only published results

**Response** (200 OK): Array of result sheet objects

---

### 4. Verify Result

**Endpoint**: `POST /exams/results/{result_id}/verify`

**Description**: Verify a result sheet

**Required Permission**: `result:verify`

**Response** (200 OK): Verified result sheet object

**Error Responses**:
- `404 Not Found`: Result not found or not generated

---

### 5. Publish Result

**Endpoint**: `POST /exams/results/{result_id}/publish`

**Description**: Publish a result sheet (must be verified first)

**Required Permission**: `result:publish`

**Response** (200 OK): Published result sheet object

**Error Responses**:
- `404 Not Found`: Result not found or not verified

---

## Data Models

### DayOfWeek Enum
- `monday`, `tuesday`, `wednesday`, `thursday`, `friday`, `saturday`, `sunday`

### ExamType Enum
- `internal`, `external`, `midterm`, `final`, `assignment`, `quiz`, `practical`, `viva`

### ExamStatus Enum
- `scheduled`, `ongoing`, `completed`, `cancelled`, `postponed`

### MarksStatus Enum
- `pending`, `submitted`, `verified`, `published`, `withheld`, `absent`

### GradeType Enum
- `A+`, `A`, `B+`, `B`, `C+`, `C`, `D`, `F`, `P` (Pass), `I` (Incomplete), `W` (Withdrawn)

### ResultType Enum
- `semester`, `annual`, `cumulative`, `transcript`, `provisional`, `final`

### ResultStatus Enum
- `draft`, `generated`, `verified`, `published`, `withheld`, `cancelled`

---

## Business Logic

### Schedule Conflict Detection

When creating or updating schedules, the system automatically checks for conflicts:
- **Instructor conflict**: Same instructor cannot have overlapping schedules
- **Room conflict**: Same room cannot be booked for overlapping time slots
- Conflicts are checked based on day of week, start time, and end time

### Marks Workflow

1. **Create**: Marks entry created with `pending` status
2. **Submit**: Evaluator submits marks (status → `submitted`)
3. **Verify**: Verifier reviews and verifies marks (status → `verified`)
4. **Publish**: Administrator publishes marks (status → `published`)

### Result Sheet Generation

Result sheets are automatically calculated based on:
- All marks entries for the student in the specified period
- Internal and external marks separation
- Grade point calculation based on institution's grading scheme
- Pass/Fail determination based on passing marks threshold
- Backlog calculation (subjects with marks below passing threshold)

---

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 201 | Created |
| 204 | No Content (successful deletion) |
| 400 | Bad Request (validation error) |
| 401 | Unauthorized (missing/invalid token) |
| 403 | Forbidden (insufficient permissions) |
| 404 | Not Found |
| 409 | Conflict (duplicate or constraint violation) |
| 500 | Internal Server Error |

---

## Rate Limiting

All endpoints are subject to rate limiting:
- **Standard users**: 100 requests per minute
- **Admin users**: 1000 requests per minute

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```

---

## Pagination

List endpoints support pagination via query parameters:
- `page` (default: 1): Page number
- `per_page` (default: 20, max: 100): Items per page

Pagination metadata is included in response headers:
```
X-Total-Count: 250
X-Page: 1
X-Per-Page: 20
X-Total-Pages: 13
```

---

## Audit Logging

All create, update, delete, verify, and publish operations are automatically logged to the audit trail with:
- User ID
- Timestamp
- Action performed
- Resource affected
- Changes made (for updates)

---

## Best Practices

1. **Schedule Management**:
   - Always check for conflicts before creating schedules
   - Use effective_from and effective_to dates to manage schedule changes
   - Mark old schedules as inactive instead of deleting them

2. **Exam Management**:
   - Use unique exam codes following institutional naming convention
   - Set appropriate weightage percentages for different exam types
   - Provide clear instructions and syllabus topics for students

3. **Marks Entry**:
   - Follow the workflow: create → submit → verify → publish
   - Use bulk publish for efficiency when publishing exam results
   - Record evaluator comments for transparency

4. **Result Sheets**:
   - Generate results only after all marks are verified
   - Verify results before publishing
   - Use appropriate result types for different scenarios

---

## Support

For API support, contact: support@emis.edu
