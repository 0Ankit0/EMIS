# Library API Documentation

## Overview

The Library Management System provides comprehensive functionality for managing library operations, including book cataloging, circulation, fine management, and lost book handling.

## Base URL

```
/api/v1/library
```

## Features

### 1. Book Management
- Add, update, and delete books
- Search and browse catalog
- Track book availability
- Manage book categories

### 2. Circulation Management
- Issue books to students and faculty
- Return books with fine calculation
- Renew books
- Reserve books
- Track borrowing history

### 3. Fine Management
- Automatic fine calculation for overdue books
- Configurable fine rules per member type
- Fine payment tracking
- Fine waivers with approval

### 4. Lost Book Management
- Report lost books
- Automatic fine calculation based on book price
- Investigation workflow
- Payment tracking
- Replacement options

## Endpoints

### Book Management

#### Add Book
```http
POST /books
Authorization: Bearer <token>
Permissions: library:create

{
  "isbn": "978-0-123456-78-9",
  "title": "Introduction to Computer Science",
  "author": "John Doe",
  "publisher": "Tech Publications",
  "publication_year": 2023,
  "category": "Computer Science",
  "quantity": 5,
  "available_quantity": 5
}
```

#### Get Book
```http
GET /books/{book_id}
Authorization: Bearer <token>
Permissions: library:read
```

#### Search Books
```http
GET /books/search?query=computer&category=science
Authorization: Bearer <token>
Permissions: library:read
```

### Circulation

#### Issue Book
```http
POST /books/issue
Authorization: Bearer <token>
Permissions: library:issue

{
  "member_id": "uuid",
  "book_id": "uuid",
  "issue_date": "2024-01-15",
  "due_date": "2024-01-29"
}
```

#### Return Book
```http
POST /books/return
Authorization: Bearer <token>
Permissions: library:return

{
  "transaction_id": "uuid",
  "return_date": "2024-01-29",
  "condition": "good"
}
```

### Lost Book Management

#### Report Lost Book
```http
POST /books/lost
Authorization: Bearer <token>
Permissions: library:manage

{
  "issue_id": 123,
  "member_id": 456,
  "book_id": 789,
  "book_title": "Advanced Physics",
  "book_isbn": "978-0-123456-78-9",
  "book_price": 850.00,
  "loss_date": "2024-01-15",
  "notes": "Book reported lost by student"
}

Response:
{
  "id": 1,
  "member_id": 456,
  "book_title": "Advanced Physics",
  "book_price": 850.00,
  "processing_fine": 170.00,
  "total_fine": 1020.00,
  "amount_paid": 0.00,
  "is_paid": false,
  "status": "reported",
  "reported_date": "2024-01-15"
}
```

**Fine Calculation**:
- Processing Fine = Book Price × (Processing Fine % / 100)
- Processing Fine is capped between minimum and maximum limits
- Total Fine = Book Price + Processing Fine

**Default Settings**:
- Processing Fine Percentage: 20%
- Minimum Processing Fine: ₹50
- Maximum Processing Fine: ₹500

#### Get Lost Book Details
```http
GET /books/lost/{loss_id}
Authorization: Bearer <token>
Permissions: library:read
```

#### Get Member Lost Books
```http
GET /books/lost/member/{member_id}?status=confirmed
Authorization: Bearer <token>
Permissions: library:read
```

**Status Values**: `reported`, `under_investigation`, `confirmed`, `resolved`, `waived`

#### Investigate Lost Book
```http
POST /books/lost/{loss_id}/investigate
Authorization: Bearer <token>
Permissions: library:manage

{
  "notes": "Initiated investigation, checking library records"
}

Response:
{
  "message": "Lost book marked as under investigation",
  "loss_id": 1,
  "status": "under_investigation"
}
```

#### Confirm Lost Book
```http
POST /books/lost/{loss_id}/confirm
Authorization: Bearer <token>
Permissions: library:manage

{
  "resolution_notes": "Investigation complete, book confirmed as lost"
}

Response:
{
  "message": "Book loss confirmed",
  "loss_id": 1,
  "total_fine": 1020.00,
  "status": "confirmed"
}
```

#### Record Lost Book Payment
```http
POST /books/lost/{loss_id}/payment
Authorization: Bearer <token>
Permissions: library:manage, finance:manage

{
  "amount": 500.00
}

Response:
{
  "id": 1,
  "member_id": 456,
  "total_fine": 1020.00,
  "amount_paid": 500.00,
  "is_paid": false,
  "status": "confirmed"
}
```

**Notes**:
- Partial payments are supported
- When total amount is paid, status automatically changes to "resolved"
- Payment creates a journal entry in the accounting system

#### Waive Lost Book Fine
```http
POST /books/lost/{loss_id}/waive
Authorization: Bearer <token>
Permissions: library:admin

{
  "reason": "Student is from economically disadvantaged background"
}

Response:
{
  "message": "Lost book fine waived",
  "loss_id": 1,
  "status": "waived"
}
```

**Notes**:
- Requires admin permission
- Creates an audit log entry
- Waiver reason is mandatory

#### Get Unpaid Lost Books
```http
GET /books/lost/unpaid
Authorization: Bearer <token>
Permissions: library:read, finance:read

Response:
{
  "count": 15,
  "total_unpaid_amount": 12450.00,
  "losses": [...]
}
```

### Lost Book Settings

#### Get Settings
```http
GET /settings/lost-books
Authorization: Bearer <token>
Permissions: library:read

Response:
{
  "id": 1,
  "processing_fine_percentage": 20.0,
  "minimum_processing_fine": 50.0,
  "maximum_processing_fine": 500.0,
  "grace_period_days": 7,
  "allow_waiver": true,
  "waiver_requires_approval": true,
  "is_active": true
}
```

#### Update Settings
```http
PUT /settings/lost-books
Authorization: Bearer <token>
Permissions: library:admin, settings:manage

{
  "processing_fine_percentage": 25.0,
  "minimum_processing_fine": 100.0,
  "maximum_processing_fine": 750.0,
  "grace_period_days": 5
}

Response:
{
  "message": "Lost book settings updated successfully",
  "settings": {...}
}
```

## Faculty Borrowing

Faculty members can borrow books with different rules than students:

**Default Faculty Settings**:
- Maximum Books: 10 (vs 3 for students)
- Borrowing Period: 30 days (vs 14 for students)
- Fine Per Day: ₹0 (vs ₹5 for students) - configurable
- Renewals: Unlimited (vs 2 for students)

The library service automatically applies the correct settings based on member type (student/faculty/staff/alumni).

## Member Types

- **STUDENT**: Regular students
- **FACULTY**: Teaching staff
- **STAFF**: Non-teaching staff
- **ALUMNI**: Former students
- **GUEST**: External members

Each member type has configurable borrowing limits, periods, and fine rules in the `library_settings` table.

## Lost Book Workflow

1. **Report** - Librarian reports book as lost
   - System calculates fine automatically
   - Status: `reported`

2. **Investigate** - Investigation initiated
   - Librarian adds investigation notes
   - Status: `under_investigation`

3. **Confirm** - Loss confirmed after investigation
   - Resolution notes added
   - Status: `confirmed`
   - Member is notified of fine

4. **Payment** - Member pays fine
   - Can be paid in installments
   - Status: `resolved` when fully paid

5. **Alternative: Waive** - Admin waives fine
   - Requires valid reason
   - Creates audit log
   - Status: `waived`

## Error Codes

- `400 Bad Request` - Invalid input data
- `401 Unauthorized` - Missing or invalid authentication
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `409 Conflict` - Business rule violation (e.g., book not available)
- `500 Internal Server Error` - Server error

## Rate Limiting

- 100 requests per minute for read operations
- 30 requests per minute for write operations

## Pagination

List endpoints support pagination:

```
GET /books?page=1&limit=20
```

## Examples

### Complete Lost Book Scenario

```bash
# 1. Report lost book
curl -X POST https://api.example.com/api/v1/library/books/lost \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "issue_id": 123,
    "member_id": 456,
    "book_id": 789,
    "book_title": "Advanced Physics",
    "book_isbn": "978-0-123456-78-9",
    "book_price": 850.00
  }'

# 2. Investigate
curl -X POST https://api.example.com/api/v1/library/books/lost/1/investigate \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"notes": "Checking all library records"}'

# 3. Confirm loss
curl -X POST https://api.example.com/api/v1/library/books/lost/1/confirm \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"resolution_notes": "Book not found, loss confirmed"}'

# 4. Record payment
curl -X POST https://api.example.com/api/v1/library/books/lost/1/payment \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"amount": 1020.00}'
```

## Notes

- All monetary amounts are in INR (₹)
- All dates are in ISO 8601 format (YYYY-MM-DD)
- All timestamps include timezone information
- Audit logs are created for all sensitive operations
- Email/SMS notifications are sent for important events
