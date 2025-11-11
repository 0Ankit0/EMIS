# Hostel Management API Documentation

## Overview

The Hostel Management API manages student housing, room allocations, mess menus, visitors, and complaints.

## Base URL

```
/api/v1/hostel
```

## Authentication

All endpoints require authentication and appropriate permissions.

## Endpoints

### Hostel Management

#### Create Hostel

```http
POST /hostels
```

**Request Body:**

```json
{
  "hostel_name": "Boys Hostel A",
  "hostel_code": "BHA",
  "gender": "male",
  "total_capacity": 200,
  "monthly_fee": 5000.00,
  "warden_id": 1,
  "has_mess": true,
  "has_gym": true,
  "description": "Main boys hostel with modern facilities"
}
```

**Permissions:** `hostel:admin`

---

### Room Management

#### Create Room

```http
POST /rooms
```

**Request Body:**

```json
{
  "hostel_id": 1,
  "room_number": "101",
  "floor": 1,
  "room_type": "double",
  "bed_capacity": 2,
  "monthly_rent": 5000.00,
  "has_ac": true,
  "has_attached_bathroom": true
}
```

**Room Types:**
- `single` - 1 bed
- `double` - 2 beds
- `triple` - 3 beds
- `quad` - 4 beds
- `dormitory` - 6+ beds

#### Get Available Rooms

```http
GET /rooms/available?hostel_id=1&room_type=double
```

**Response:**

```json
{
  "rooms": [
    {
      "id": 1,
      "room_number": "101",
      "hostel_id": 1,
      "room_type": "double",
      "bed_capacity": 2,
      "current_occupancy": 0,
      "available_beds": 2,
      "monthly_rent": 5000.00
    }
  ]
}
```

---

### Room Allocation (T140)

#### Allocate Room

```http
POST /allocations
```

Allocate room to student.

**Request Body:**

```json
{
  "student_id": 123,
  "room_id": 1,
  "start_date": "2025-06-01",
  "academic_year": "2025-2026",
  "semester": 1
}
```

**Response:**

```json
{
  "id": 1,
  "student_id": 123,
  "room_id": 1,
  "bed_number": 1,
  "start_date": "2025-06-01",
  "monthly_fee": 5000.00
}
```

**Permissions:** `hostel:allocate`

**Business Rules:**
- Room must have available beds
- Student cannot have multiple active allocations
- Automatically assigns bed number
- Updates room and hostel occupancy

#### Deallocate Room

```http
POST /allocations/{allocation_id}/deallocate
```

Release student's room allocation.

#### Transfer Room

```http
POST /allocations/transfer
```

**Request Body:**

```json
{
  "student_id": 123,
  "new_room_id": 5,
  "reason": "Medical reasons - needs ground floor"
}
```

Transfers student from current room to new room.

#### Get Student Allocation

```http
GET /allocations/student/{student_id}
```

Get student's current room allocation.

---

### Mess Menu Management (T141)

#### Create Mess Menu

```http
POST /mess-menu
```

**Request Body:**

```json
{
  "hostel_id": 1,
  "day_of_week": "Monday",
  "meal_type": "breakfast",
  "menu_items": "Idli, Sambar, Chutney, Tea/Coffee",
  "effective_from": "2025-06-01",
  "description": "South Indian breakfast",
  "is_vegetarian": true
}
```

**Meal Types:**
- `breakfast` - Morning meal
- `lunch` - Afternoon meal
- `dinner` - Evening meal
- `snacks` - Evening snacks

#### Get Weekly Mess Menu

```http
GET /mess-menu/{hostel_id}/weekly?effective_date=2025-06-01
```

Returns complete week's menu for all meals.

**Response:**

```json
{
  "menus": [
    {
      "id": 1,
      "day_of_week": "Monday",
      "meal_type": "breakfast",
      "menu_items": "Idli, Sambar, Chutney, Tea/Coffee",
      "description": "South Indian breakfast",
      "is_vegetarian": true
    }
  ]
}
```

---

### Visitor Management

#### Register Visitor

```http
POST /visitors
```

**Request Body:**

```json
{
  "hostel_id": 1,
  "student_id": 123,
  "visitor_name": "Mr. Parent Name",
  "visitor_phone": "+91-9876543210",
  "relationship": "parent"
}
```

**Permissions:** `hostel:manage`

#### Checkout Visitor

```http
POST /visitors/{visitor_id}/checkout
```

Mark visitor as checked out.

---

### Complaint Management

#### Create Complaint

```http
POST /complaints
```

**Request Body:**

```json
{
  "hostel_id": 1,
  "student_id": 123,
  "category": "maintenance",
  "title": "AC not working",
  "description": "Air conditioner in room 101 stopped working",
  "room_id": 1,
  "priority": "high"
}
```

**Categories:**
- `maintenance` - Room/facility maintenance
- `cleanliness` - Cleaning issues
- `noise` - Noise complaints
- `security` - Security concerns
- `food` - Mess food quality
- `other` - Other issues

**Priority Levels:**
- `low` - Can be handled later
- `medium` - Normal priority (default)
- `high` - Needs urgent attention
- `urgent` - Critical issue

#### Resolve Complaint

```http
POST /complaints/{complaint_id}/resolve
```

**Request Body:**

```json
{
  "resolution_notes": "AC technician fixed the compressor"
}
```

**Permissions:** `hostel:admin`

---

### Reports

#### Occupancy Report

```http
GET /occupancy-report?hostel_id=1
```

Get hostel occupancy statistics.

**Response:**

```json
{
  "hostels": [
    {
      "hostel_id": 1,
      "hostel_name": "Boys Hostel A",
      "total_capacity": 200,
      "current_occupancy": 180,
      "available_beds": 20,
      "occupancy_rate": 90.0
    }
  ],
  "total_capacity": 500,
  "total_occupancy": 450,
  "overall_occupancy_rate": 90.0
}
```

---

## Permissions

- `hostel:read` - View hostel information
- `hostel:admin` - Full hostel administration
- `hostel:allocate` - Allocate/deallocate rooms
- `hostel:manage` - Manage visitors and complaints
- `hostel:complaint` - Create complaints (students)

---

## Workflows

### Student Hostel Admission

1. **Check availability**: `GET /rooms/available`
2. **Allocate room**: `POST /allocations`
3. **Generate hostel fee bill**: (Billing API)
4. **Student checks in**: Update allocation

### Room Transfer

1. **Check available rooms**: `GET /rooms/available`
2. **Transfer student**: `POST /allocations/transfer`
3. **Previous room becomes available automatically**

### Complaint Resolution

1. **Student creates complaint**: `POST /complaints`
2. **Admin assigns to maintenance staff**: Update complaint
3. **Resolve complaint**: `POST /complaints/{id}/resolve`
4. **Student provides feedback**: Update complaint

---

## Room Status

- `available` - Room has free beds
- `occupied` - Room is fully occupied
- `maintenance` - Under maintenance
- `reserved` - Reserved for someone

---

## Business Rules

### Room Allocation

- Student can have only one active allocation
- Room must have available beds
- Bed number auto-assigned sequentially
- Room status changes to 'occupied' when full
- Hostel occupancy auto-updated

### Room Deallocation

- Marks allocation as inactive
- Frees up bed in room
- Updates room and hostel occupancy
- Security deposit handling tracked

### Mess Menu

- Menu valid for specific date range
- Can have multiple effective periods
- Supports vegetarian/vegan indicators
- Weekly planning supported

### Visitors

- Check-in time recorded automatically
- Requires approval from warden/admin
- ID proof details captured
- Check-out time tracked

### Complaints

- Auto-generated complaint number
- Priority-based handling
- Status tracking (open → in_progress → resolved → closed)
- Satisfaction rating from students

---

## Integration

### With Billing

When room is allocated:
```javascript
// Create hostel fee bill
POST /api/v1/billing/bills
{
  "bill_type": "hostel_fee",
  "student_id": 123,
  "items": [{
    "name": "Hostel Fee",
    "unit_price": 5000.00,
    "quantity": 1
  }]
}
```

### With Student Records

Room allocation updates student profile with hostel information.

---

## Implementation Status

✅ All endpoints implemented (T133-T144)
- [X] T133 - Hostel model
- [X] T134 - Room model
- [X] T135 - RoomAllocation model
- [X] T136 - MessMenu model
- [X] T137 - HostelVisitor model
- [X] T138 - HostelComplaint model
- [X] T139 - HostelService
- [X] T140 - Room allocation logic
- [X] T141 - Mess menu management
- [X] T142 - Hostel management endpoints
- [X] T143 - Room allocation endpoints
- [X] T144 - API documentation
