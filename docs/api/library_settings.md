# Library Fine System API Documentation

## Overview

This document describes the REST API endpoints for managing library settings, fine configurations, and fine waivers in the EMIS library system.

**Base URL**: `/api/v1`

## Authentication

All endpoints require authentication via JWT token in the Authorization header:
```
Authorization: Bearer <token>
```

## Permissions

Each endpoint requires specific permissions as noted in the endpoint descriptions.

---

## Library Settings Endpoints

### 1. Create or Update Library Settings

**Endpoint**: `POST /library/settings/`

**Description**: Create or update library settings for a specific member type

**Required Permission**: `library:admin`

**Request Body**:
```json
{
  "member_type": "student",
  "max_books_allowed": 5,
  "borrowing_period_days": 14,
  "fine_per_day": 5.0,
  "grace_period_days": 1,
  "max_fine_amount": 500.0,
  "max_reservations": 3,
  "reservation_hold_days": 3,
  "max_renewals": 2,
  "digital_access_enabled": true,
  "digital_download_limit": 10,
  "description": "Settings for undergraduate students"
}
```

**Member Types**:
- `student`: Students (undergraduate/graduate)
- `faculty`: Faculty members
- `staff`: Staff members
- `alumni`: Alumni
- `guest`: Guest users

**Response** (201 Created):
```json
{
  "id": 1,
  "member_type": "student",
  "max_books_allowed": 5,
  "borrowing_period_days": 14,
  "fine_per_day": 5.0,
  "grace_period_days": 1,
  "max_fine_amount": 500.0,
  "max_reservations": 3,
  "reservation_hold_days": 3,
  "max_renewals": 2,
  "digital_access_enabled": true,
  "digital_download_limit": 10,
  "is_active": true,
  "description": "Settings for undergraduate students"
}
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Insufficient permissions

---

### 2. Get All Library Settings

**Endpoint**: `GET /library/settings/`

**Description**: Retrieve library settings for all member types

**Required Permission**: `library:read`

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "member_type": "student",
    "max_books_allowed": 5,
    "borrowing_period_days": 14,
    "fine_per_day": 5.0,
    "grace_period_days": 1,
    "max_fine_amount": 500.0,
    "max_reservations": 3,
    "reservation_hold_days": 3,
    "max_renewals": 2,
    "digital_access_enabled": true,
    "digital_download_limit": 10,
    "is_active": true,
    "description": "Settings for undergraduate students"
  },
  {
    "id": 2,
    "member_type": "faculty",
    "max_books_allowed": 10,
    "borrowing_period_days": 30,
    "fine_per_day": 0.0,
    "grace_period_days": 7,
    "max_fine_amount": 0.0,
    ...
  }
]
```

---

### 3. Get Settings by Member Type

**Endpoint**: `GET /library/settings/{member_type}`

**Description**: Retrieve library settings for a specific member type

**Required Permission**: `library:read`

**Path Parameters**:
- `member_type`: One of `student`, `faculty`, `staff`, `alumni`, `guest`

**Response** (200 OK): Library settings object

**Error Responses**:
- `404 Not Found`: Settings not found for member type

---

### 4. Initialize Default Settings

**Endpoint**: `POST /library/settings/initialize-defaults`

**Description**: Initialize default library settings for all member types (useful for first-time setup)

**Required Permission**: `library:admin`

**Response** (201 Created):
```json
{
  "message": "Default settings initialized successfully"
}
```

**Default Settings Created**:

| Member Type | Max Books | Borrowing Days | Fine/Day | Grace Days | Max Fine |
|-------------|-----------|----------------|----------|------------|----------|
| Student     | 3         | 14             | ₹5.00    | 0          | ₹500     |
| Faculty     | 10        | 30             | ₹0.00    | 7          | ₹0       |
| Staff       | 5         | 21             | ₹2.00    | 2          | ₹300     |
| Alumni      | 2         | 7              | ₹10.00   | 0          | ₹1000    |
| Guest       | 1         | 3              | ₹20.00   | 0          | ₹500     |

---

## Fine Calculation Endpoints

### 1. Calculate Fine

**Endpoint**: `POST /library/settings/calculate-fine`

**Description**: Calculate fine for an overdue book based on member type and dates

**Required Permission**: `library:read`

**Request Body**:
```json
{
  "member_type": "student",
  "due_date": "2024-01-15",
  "return_date": "2024-01-20"
}
```

**Notes**:
- If `return_date` is not provided, current date is used
- Grace period is applied automatically based on member type settings

**Response** (200 OK):
```json
{
  "fine_amount": 20.0,
  "days_overdue": 4,
  "member_type": "student"
}
```

**Fine Calculation Logic**:
1. Calculate days overdue: `return_date - due_date`
2. Subtract grace period: `overdue_days = max(0, days_overdue - grace_period_days)`
3. Calculate fine: `fine = overdue_days × fine_per_day`
4. Cap at max fine: `final_fine = min(fine, max_fine_amount)`

**Examples**:

```
Student borrows book on Jan 1, due Jan 15, returns Jan 20:
- Days overdue: 5
- Grace period: 0 (students have no grace)
- Fine: 5 days × ₹5/day = ₹25

Faculty borrows book on Jan 1, due Jan 31, returns Feb 5:
- Days overdue: 5
- Grace period: 7 (faculty get 7 days grace)
- Overdue after grace: 0 (within grace period)
- Fine: ₹0
```

---

## Fine Waiver Endpoints

### 1. Create Fine Waiver

**Endpoint**: `POST /library/settings/fine-waiver`

**Description**: Create a fine waiver (partial or full exemption from fine)

**Required Permission**: `library:admin`

**Request Body**:
```json
{
  "fine_id": 123,
  "member_id": 456,
  "original_amount": 150.0,
  "waived_amount": 100.0,
  "reason": "First-time offender, student requested waiver due to medical emergency"
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "fine_id": 123,
  "member_id": 456,
  "original_amount": 150.0,
  "waived_amount": 100.0,
  "final_amount": 50.0,
  "reason": "First-time offender, student requested waiver due to medical emergency",
  "approved_by": 789
}
```

**Notes**:
- `final_amount` is automatically calculated as: `original_amount - waived_amount`
- Waivers must be approved by a library administrator
- Full waiver: set `waived_amount = original_amount`
- Partial waiver: set `waived_amount < original_amount`

**Error Responses**:
- `400 Bad Request`: Invalid waiver amount (waived_amount > original_amount)
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Insufficient permissions

---

### 2. Get Member Waivers

**Endpoint**: `GET /library/settings/member/{member_id}/waivers`

**Description**: Get all fine waivers for a specific member

**Required Permission**: `library:read`

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "fine_id": 123,
    "member_id": 456,
    "original_amount": 150.0,
    "waived_amount": 100.0,
    "final_amount": 50.0,
    "reason": "Medical emergency",
    "approved_by": 789
  },
  {
    "id": 2,
    "fine_id": 145,
    "member_id": 456,
    "original_amount": 75.0,
    "waived_amount": 75.0,
    "final_amount": 0.0,
    "reason": "Book lost due to flood damage",
    "approved_by": 789
  }
]
```

---

## Configuration Fields Explained

### Borrowing Configuration

- **max_books_allowed**: Maximum number of books a member can borrow simultaneously
- **borrowing_period_days**: Number of days a book can be borrowed before it's due
- **max_renewals**: Maximum number of times a member can renew a borrowed book

### Fine Configuration

- **fine_per_day**: Amount charged per day after the book is overdue
- **grace_period_days**: Number of days after due date before fines start accruing
- **max_fine_amount**: Maximum fine amount that can be charged for a single book (cap)

### Reservation Configuration

- **max_reservations**: Maximum number of books a member can reserve at once
- **reservation_hold_days**: Number of days a reserved book is held before being released

### Digital Access Configuration

- **digital_access_enabled**: Whether member can access digital resources
- **digital_download_limit**: Maximum number of digital resources that can be downloaded per month

---

## Use Cases

### Use Case 1: Setting Up Library for First Time

```bash
# Step 1: Initialize default settings for all member types
POST /library/settings/initialize-defaults

# Step 2: Customize settings for specific member types
POST /library/settings/
{
  "member_type": "student",
  "max_books_allowed": 5,
  "fine_per_day": 10.0
}
```

### Use Case 2: Calculating Fine for Overdue Book

```bash
# When student returns book late
POST /library/settings/calculate-fine
{
  "member_type": "student",
  "due_date": "2024-01-15",
  "return_date": "2024-01-22"
}

# Response: fine_amount = 35.0 (7 days × ₹5/day)
```

### Use Case 3: Granting Fine Waiver

```bash
# Student requests waiver due to medical emergency
POST /library/settings/fine-waiver
{
  "fine_id": 123,
  "member_id": 456,
  "original_amount": 150.0,
  "waived_amount": 150.0,
  "reason": "Hospitalized during exam week, unable to return books"
}

# Result: final_amount = 0.0 (full waiver)
```

### Use Case 4: Different Fine Policies by Member Type

```
Students: ₹5/day, no grace period, max ₹500
Faculty: ₹0/day (no fines), 7 days grace
Alumni: ₹10/day, no grace period, max ₹1000
```

This ensures fair treatment based on member status and encourages timely returns.

---

## Business Rules

### Grace Period

- Grace period starts after the due date
- No fine is charged during the grace period
- After grace period expires, fines accrue from the first day after grace period
- Example: Due Jan 15, Grace 3 days
  - Return Jan 16-18: No fine
  - Return Jan 19+: Fine starts from Jan 19

### Maximum Fine

- Prevents excessive fines from accumulating
- Once max fine is reached, no additional fine is charged
- Example: Max fine ₹500, fine per day ₹5
  - After 100 days overdue, fine remains ₹500 (doesn't increase further)

### Fine Waivers

- Can only be created by library administrators
- Require documented reason
- Can be partial or full
- Cannot exceed original fine amount
- Waivers are permanent (cannot be revoked)

### Member Type Priorities

Typical hierarchy (most to least privileges):
1. Faculty: Highest privileges, longest borrowing period, no fines
2. Staff: Moderate privileges, reduced fines
3. Students: Standard privileges, standard fines
4. Alumni: Limited privileges, higher fines
5. Guest: Minimal privileges, highest fines, shortest period

---

## Fine Calculation Examples

### Example 1: Student - No Grace Period

```
Due date: Jan 15, 2024
Return date: Jan 20, 2024
Days overdue: 5
Grace period: 0
Fine per day: ₹5
Fine = 5 days × ₹5 = ₹25
```

### Example 2: Faculty - With Grace Period

```
Due date: Jan 31, 2024
Return date: Feb 5, 2024
Days overdue: 5
Grace period: 7 days
Overdue after grace: 0 (still within grace)
Fine = ₹0
```

### Example 3: Alumni - With Max Fine Cap

```
Due date: Jan 1, 2024
Return date: Mar 1, 2024
Days overdue: 60
Grace period: 0
Fine per day: ₹10
Calculated fine: 60 × ₹10 = ₹600
Max fine: ₹500
Final fine = ₹500 (capped)
```

### Example 4: Student - With Partial Waiver

```
Original fine: ₹150
Waiver reason: First offense, good academic record
Waived amount: ₹100
Final amount due: ₹150 - ₹100 = ₹50
```

---

## Common Scenarios

### Scenario 1: Lost Book

When a book is lost:
1. Calculate fine up to max fine amount
2. Add book replacement cost
3. Optionally apply waiver for fine (not replacement cost)

### Scenario 2: Damaged Book

When a book is damaged:
1. Calculate fine normally
2. Add repair/replacement cost based on damage severity
3. Waiver can be applied to fine portion only

### Scenario 3: System Downtime

If library system was down preventing return:
1. Create full waiver for affected period
2. Document reason: "System downtime on [dates]"
3. Adjust due date or grant waiver

### Scenario 4: Multiple Overdue Books

Calculate fine for each book separately:
- Each book has its own due date
- Each book accrues fine independently
- Max fine cap applies per book, not total
- Total fine = sum of all individual fines

---

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request (validation error) |
| 401 | Unauthorized (missing/invalid token) |
| 403 | Forbidden (insufficient permissions) |
| 404 | Not Found |
| 500 | Internal Server Error |

---

## Audit Logging

All library settings changes and fine waivers are automatically logged:
- Who made the change (updated_by/approved_by)
- When the change was made (timestamp)
- What was changed (old vs new values for settings)
- Why (reason for waivers)

---

## Best Practices

1. **Setting Up Library**:
   - Initialize defaults first
   - Customize based on institutional policy
   - Review settings periodically (annually)

2. **Fine Management**:
   - Set reasonable fine amounts
   - Balance between deterrent and fairness
   - Provide grace periods for faculty/staff
   - Cap maximum fines to prevent excessive debt

3. **Waiver Management**:
   - Document clear waiver policies
   - Require documented reasons
   - Track waiver patterns to identify issues
   - Regular reporting on waiver frequency

4. **Member Type Configuration**:
   - Faculty: Privileged access, extended periods, minimal fines
   - Students: Standard access, moderate periods, standard fines
   - Alumni: Limited access, short periods, higher fines
   - Guest: Restricted access, very short periods, highest fines

---

## Integration with Circulation System

The fine system integrates with the library circulation module:

1. **Borrowing**: When book is issued, due date is calculated based on `borrowing_period_days`
2. **Return**: When book is returned late, fine is automatically calculated
3. **Renewal**: Each renewal extends due date by `borrowing_period_days`
4. **Reservation**: Reserved books are held for `reservation_hold_days`

---

## Support

For API support, contact: library-support@emis.edu

For policy questions, contact: library-admin@emis.edu
