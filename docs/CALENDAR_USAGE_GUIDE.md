# 📅 Academic Calendar System - Complete Guide

## Overview

The Academic Calendar system provides an easy and comprehensive way to manage all college events, examinations, holidays, deadlines, and program events in one centralized calendar.

## 🎯 Key Features

1. **Multiple Event Types**: Examinations, Holidays, Program Events, Deadlines, Seminars, etc.
2. **Easy Adding**: Quick methods to add different types of events
3. **Flexible Retrieval**: Get calendar by date range, month, week, or specific filters
4. **Bulk Operations**: Add multiple holidays at once
5. **Event Management**: Publish, cancel, or postpone events
6. **Color Coding**: Visual distinction with color codes
7. **Priority System**: Mark important events with priority levels

## 📝 Event Types Available

- `examination` - Exams and assessments
- `holiday` - College holidays
- `semester_start` - Academic semester begins
- `semester_end` - Academic semester ends
- `registration` - Course registration periods
- `admission` - Admission-related events
- `program_event` - Program-specific events
- `orientation` - Orientation programs
- `convocation` - Graduation ceremonies
- `workshop` - Workshops and training
- `seminar` - Academic seminars
- `sports` - Sports events
- `cultural` - Cultural activities
- `deadline` - Important deadlines
- `meeting` - Meetings and conferences
- `other` - Other events

## 🚀 Quick Start Examples

### 1. Add an Examination to Calendar

```bash
POST /api/calendar/events/examination
```

```json
{
  "exam_id": 123,
  "exam_title": "Mid-Semester Examination",
  "exam_date": "2024-03-15",
  "end_date": "2024-03-20",
  "academic_year": "2023-2024",
  "semester": 2,
  "venue": "Main Building",
  "description": "Mid-semester exams for all programs"
}
```

**Response:**
```json
{
  "id": "uuid-here",
  "title": "Examination: Mid-Semester Examination",
  "exam_id": 123,
  "start_date": "2024-03-15",
  "message": "Examination added to calendar"
}
```

### 2. Add a Holiday

```bash
POST /api/calendar/holidays
```

```json
{
  "name": "Independence Day",
  "holiday_date": "2024-08-15",
  "holiday_type": "national",
  "description": "National Holiday - Independence Day",
  "academic_year": "2023-2024"
}
```

### 3. Add Multiple Holidays (Bulk)

```bash
POST /api/calendar/holidays/bulk
```

```json
{
  "holidays": [
    {
      "name": "Republic Day",
      "date": "2024-01-26",
      "type": "national",
      "academic_year": "2023-2024"
    },
    {
      "name": "Holi",
      "date": "2024-03-25",
      "type": "religious",
      "academic_year": "2023-2024"
    },
    {
      "name": "Diwali",
      "date": "2024-11-12",
      "type": "religious",
      "academic_year": "2024-2025"
    }
  ]
}
```

**Response:**
```json
{
  "total_added": 3,
  "holidays": [
    {"name": "Republic Day", "date": "2024-01-26", "type": "national"},
    {"name": "Holi", "date": "2024-03-25", "type": "religious"},
    {"name": "Diwali", "date": "2024-11-12", "type": "religious"}
  ],
  "message": "Successfully added 3 holidays"
}
```

### 4. Add a Program Event

```bash
POST /api/calendar/events/program
```

```json
{
  "program_id": 5,
  "title": "Computer Science Department Annual Fest",
  "event_date": "2024-04-10",
  "end_date": "2024-04-12",
  "description": "Three-day tech fest with coding competitions",
  "location": "CS Department"
}
```

### 5. Add an Important Deadline

```bash
POST /api/calendar/deadlines
```

```json
{
  "title": "Last Date for Course Registration",
  "deadline_date": "2024-01-31",
  "deadline_time": "17:00:00",
  "category": "registration",
  "description": "Final deadline to register for courses",
  "academic_year": "2023-2024",
  "semester": 2
}
```

### 6. Add a General Event

```bash
POST /api/calendar/events
```

```json
{
  "title": "Guest Lecture on AI & Machine Learning",
  "description": "Dr. John Smith from MIT",
  "event_type": "seminar",
  "start_date": "2024-02-15",
  "start_time": "14:00:00",
  "end_time": "16:00:00",
  "is_all_day": false,
  "location": "Auditorium",
  "venue": "Main Campus Auditorium",
  "organizer": "CS Department",
  "academic_year": "2023-2024",
  "semester": 2,
  "color_code": "#2ECC71",
  "priority": 1,
  "is_for_students": true,
  "is_for_faculty": true
}
```

## 📅 Retrieving Calendar Data

### 1. Get Full Calendar with Filters

```bash
GET /api/calendar/?start_date=2024-01-01&end_date=2024-12-31&academic_year=2023-2024
```

**Query Parameters:**
- `start_date` - Filter from this date
- `end_date` - Filter up to this date
- `event_types` - Array of event types (e.g., `examination,holiday`)
- `academic_year` - Filter by academic year
- `semester` - Filter by semester
- `program_id` - Filter by program

**Response:**
```json
{
  "total": 45,
  "events": [
    {
      "id": "uuid",
      "title": "Mid-Semester Examination",
      "description": "Mid-semester exams",
      "event_type": "examination",
      "start_date": "2024-03-15",
      "end_date": "2024-03-20",
      "is_all_day": true,
      "location": "Main Building",
      "status": "scheduled",
      "color_code": "#FF5733",
      "icon": "exam",
      "priority": 2,
      "is_upcoming": true,
      "is_today": false,
      "duration_days": 6
    }
  ]
}
```

### 2. Get Calendar for a Specific Month

```bash
GET /api/calendar/month/2024/3
```

This returns all events in March 2024.

### 3. Get Today's Events

```bash
GET /api/calendar/today
```

**Response:**
```json
{
  "date": "2024-02-15",
  "total": 2,
  "events": [
    {
      "id": "uuid",
      "title": "Guest Lecture on AI",
      "event_type": "seminar",
      "start_time": "14:00:00",
      "end_time": "16:00:00",
      "location": "Auditorium",
      "color_code": "#2ECC71"
    }
  ]
}
```

### 4. Get Upcoming Events

```bash
GET /api/calendar/upcoming?days=7
```

Get events for the next 7 days.

### 5. Get All Holidays

```bash
GET /api/calendar/holidays?academic_year=2023-2024
```

**Response:**
```json
{
  "total": 15,
  "holidays": [
    {
      "id": "uuid",
      "name": "Independence Day",
      "holiday_date": "2024-08-15",
      "holiday_type": "national",
      "description": "National Holiday",
      "is_restricted": false
    }
  ]
}
```

### 6. Get Important Deadlines

```bash
GET /api/calendar/deadlines?category=registration&academic_year=2023-2024
```

### 7. Get Calendar Summary

```bash
GET /api/calendar/summary?academic_year=2023-2024&semester=2
```

**Response:**
```json
{
  "total_events": 85,
  "by_type": {
    "examination": 12,
    "holiday": 15,
    "program_event": 8,
    "seminar": 10,
    "deadline": 5
  },
  "by_status": {
    "scheduled": 60,
    "completed": 20,
    "cancelled": 5
  },
  "total_holidays": 15,
  "upcoming_events": 40,
  "past_events": 45
}
```

## 🔧 Event Management

### Publish an Event

```bash
POST /api/calendar/events/{event_id}/publish
```

Makes the event visible to all users.

### Cancel an Event

```bash
POST /api/calendar/events/{event_id}/cancel
```

```json
{
  "reason": "Due to unforeseen circumstances"
}
```

### Postpone an Event

```bash
POST /api/calendar/events/{event_id}/postpone
```

```json
{
  "new_date": "2024-04-20"
}
```

## 🎨 UI Display Guide

### Color Codes

Events come with color codes for easy visual identification:

- **Examinations**: `#FF5733` (Red/Orange)
- **Holidays**: `#E74C3C` (Red)
- **Deadlines**: `#F39C12` (Orange)
- **Program Events**: `#3498DB` (Blue)
- **Seminars**: `#2ECC71` (Green)
- Custom colors can be assigned

### Priority Levels

- `0` - Normal
- `1` - High
- `2` - Urgent

### Event Properties for UI

Each event has:
- `is_upcoming` - Boolean indicating if event is in future
- `is_today` - Boolean indicating if event is today
- `is_past` - Boolean indicating if event is completed
- `duration_days` - Number of days the event spans

## 📋 Complete Usage Example: Setting Up Annual Calendar

```python
import requests

base_url = "http://localhost:8000/api/calendar"
headers = {"Authorization": "Bearer YOUR_TOKEN"}

# 1. Add all holidays for the year
holidays = {
    "holidays": [
        {"name": "New Year", "date": "2024-01-01", "type": "national", "academic_year": "2023-2024"},
        {"name": "Republic Day", "date": "2024-01-26", "type": "national", "academic_year": "2023-2024"},
        {"name": "Holi", "date": "2024-03-25", "type": "religious", "academic_year": "2023-2024"},
        {"name": "Independence Day", "date": "2024-08-15", "type": "national", "academic_year": "2023-2024"},
        {"name": "Gandhi Jayanti", "date": "2024-10-02", "type": "national", "academic_year": "2024-2025"},
        {"name": "Diwali", "date": "2024-11-12", "type": "religious", "academic_year": "2024-2025"}
    ]
}
requests.post(f"{base_url}/holidays/bulk", json=holidays, headers=headers)

# 2. Add examination periods
exam_data = {
    "exam_id": 101,
    "exam_title": "End Semester Examination",
    "exam_date": "2024-05-01",
    "end_date": "2024-05-15",
    "academic_year": "2023-2024",
    "semester": 2,
    "venue": "All Examination Halls"
}
requests.post(f"{base_url}/events/examination", json=exam_data, headers=headers)

# 3. Add important deadlines
deadlines = [
    {
        "title": "Course Registration Deadline",
        "deadline_date": "2024-01-15",
        "category": "registration",
        "academic_year": "2023-2024",
        "semester": 2
    },
    {
        "title": "Fee Payment Last Date",
        "deadline_date": "2024-01-31",
        "category": "fee_payment",
        "academic_year": "2023-2024",
        "semester": 2
    }
]
for deadline in deadlines:
    requests.post(f"{base_url}/deadlines", json=deadline, headers=headers)

# 4. Add program events
program_event = {
    "program_id": 5,
    "title": "Annual Tech Fest",
    "event_date": "2024-03-20",
    "end_date": "2024-03-22",
    "location": "Main Campus"
}
requests.post(f"{base_url}/events/program", json=program_event, headers=headers)

# 5. Publish all events
# (Get event IDs and publish them)

print("✅ Annual calendar setup complete!")
```

## 🔐 Required Permissions

- `calendar:create` - Create calendar events
- `calendar:read` - View calendar
- `calendar:update` - Update/cancel/postpone events
- `calendar:publish` - Publish events

## 💡 Best Practices

1. **Always set academic_year** - Makes filtering easier
2. **Use color codes consistently** - Helps users identify event types quickly
3. **Set appropriate priorities** - Mark critical events as high priority
4. **Publish events** - Events are only visible after publishing
5. **Bulk operations** - Use bulk APIs when adding multiple similar items
6. **Use event_type correctly** - Helps with filtering and reporting

## 🎯 Common Use Cases

### Display Calendar on Homepage
```bash
GET /api/calendar/upcoming?days=7
```

### Show Monthly Calendar View
```bash
GET /api/calendar/month/2024/3?academic_year=2023-2024
```

### Student Dashboard - Next 30 Days
```bash
GET /api/calendar/upcoming?days=30
```

### Examination Schedule Only
```bash
GET /api/calendar/?event_types=examination&academic_year=2023-2024
```

### Holidays List
```bash
GET /api/calendar/holidays?academic_year=2023-2024
```

---

✅ **The Academic Calendar system is now fully implemented and ready to use!**
