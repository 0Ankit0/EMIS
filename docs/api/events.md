# Events API Documentation

## Base URL
`/api/events`

## Overview
The Events API manages college events, registrations, budgets, and attendance.

## Authentication
All endpoints require authentication.

---

## Endpoints

### Event Management

#### Create Event
```http
POST /api/events/
```

**Request Body:**
```json
{
  "title": "Technical Symposium 2024",
  "description": "Annual technical symposium",
  "event_type": "technical",
  "start_date": "2024-03-15T09:00:00",
  "end_date": "2024-03-17T18:00:00",
  "registration_start": "2024-02-01T00:00:00",
  "registration_end": "2024-03-10T23:59:59",
  "venue": "Main Auditorium",
  "max_participants": 500,
  "registration_fee": 500.00,
  "is_paid_event": true,
  "coordinator_name": "Dr. Smith",
  "coordinator_contact": "+91-9876543210",
  "is_inter_college": true
}
```

#### Get All Events
```http
GET /api/events/?event_type=technical&status=published
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Technical Symposium 2024",
    "event_type": "technical",
    "status": "published",
    "start_date": "2024-03-15T09:00:00",
    "end_date": "2024-03-17T18:00:00",
    "venue": "Main Auditorium",
    "max_participants": 500,
    "current_participants": 250,
    "is_published": true
  }
]
```

#### Get Event Details
```http
GET /api/events/{event_id}
```

#### Update Event
```http
PUT /api/events/{event_id}
```

#### Delete Event
```http
DELETE /api/events/{event_id}
```

### Event Registration

#### Register for Event
```http
POST /api/events/{event_id}/register
```

**Request Body:**
```json
{
  "participant_name": "John Doe",
  "participant_email": "john@example.com",
  "participant_phone": "+91-9876543210",
  "college_name": "ABC College",
  "team_name": "Team Alpha",
  "remarks": "Interested in coding competition"
}
```

**Response:**
```json
{
  "message": "Registration successful",
  "registration_id": 123,
  "status": "pending"
}
```

#### Get Event Registrations
```http
GET /api/events/{event_id}/registrations?status=approved
```

#### Approve Registration
```http
POST /api/events/registrations/{registration_id}/approve
```

#### Reject Registration
```http
POST /api/events/registrations/{registration_id}/reject?reason=Capacity+full
```

### Event Budget

#### Add Budget Item
```http
POST /api/events/{event_id}/budget
```

**Request Body:**
```json
{
  "category": "Venue",
  "description": "Auditorium rental",
  "estimated_amount": 50000.00
}
```

#### Approve Budget
```http
POST /api/events/budget/{budget_id}/approve
```

**Request Body:**
```json
{
  "approved_amount": 45000.00
}
```

#### Get Budget Summary
```http
GET /api/events/{event_id}/budget/summary
```

**Response:**
```json
{
  "total_estimated": 200000.00,
  "total_approved": 180000.00,
  "total_actual": 175000.00,
  "variance": 5000.00,
  "items": []
}
```

### Event Attendance

#### Mark Attendance
```http
POST /api/events/{event_id}/attendance/{registration_id}
```

**Request Body:**
```json
{
  "participant_name": "John Doe",
  "check_in_time": "2024-03-15T09:30:00",
  "attendance_date": "2024-03-15"
}
```

#### Get Attendance Report
```http
GET /api/events/{event_id}/attendance/report
```

**Response:**
```json
{
  "total_registered": 500,
  "total_present": 450,
  "total_absent": 50,
  "attendance_percentage": 90.0
}
```

### Event Statistics

#### Get Event Statistics
```http
GET /api/events/{event_id}/statistics
```

**Response:**
```json
{
  "event": {
    "id": 1,
    "title": "Technical Symposium 2024",
    "status": "completed"
  },
  "registrations": {
    "total": 520,
    "approved": 500,
    "pending": 15,
    "rejected": 5,
    "waitlisted": 0
  },
  "budget": {
    "total_estimated": 200000.00,
    "total_approved": 180000.00,
    "total_actual": 175000.00
  },
  "attendance": {
    "total_present": 450,
    "attendance_percentage": 90.0
  }
}
```

---

## Data Models

### Event
```json
{
  "id": 1,
  "title": "Technical Symposium 2024",
  "event_type": "technical",
  "status": "published",
  "start_date": "2024-03-15T09:00:00",
  "end_date": "2024-03-17T18:00:00",
  "venue": "Main Auditorium",
  "max_participants": 500,
  "current_participants": 250,
  "registration_fee": 500.00,
  "is_paid_event": true,
  "is_published": true
}
```

### Event Registration
```json
{
  "id": 123,
  "event_id": 1,
  "participant_name": "John Doe",
  "participant_email": "john@example.com",
  "status": "approved",
  "registration_date": "2024-02-15T10:00:00",
  "payment_status": "paid"
}
```

### Event Budget
```json
{
  "id": 1,
  "event_id": 1,
  "category": "Venue",
  "estimated_amount": 50000.00,
  "approved_amount": 45000.00,
  "actual_amount": 44000.00,
  "is_approved": true
}
```

---

## Event Types

- `cultural` - Cultural events
- `sports` - Sports events
- `technical` - Technical events
- `workshop` - Workshops
- `seminar` - Seminars
- `conference` - Conferences
- `fest` - College fests
- `competition` - Competitions
- `ceremony` - Ceremonies

## Registration Status

- `pending` - Awaiting approval
- `approved` - Registration approved
- `rejected` - Registration rejected
- `cancelled` - Cancelled by participant
- `waitlisted` - On waiting list
