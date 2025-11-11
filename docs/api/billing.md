# Billing API Documentation

## Overview

The Billing API provides comprehensive fee management, bill generation, payment processing, and financial tracking for students and employees.

## Base URL

```
/api/v1/billing
```

## Authentication

All endpoints require authentication and appropriate permissions.

## Endpoints

### Bill Management

#### Create Bill

```http
POST /bills
```

Create a new bill for student or employee.

**Request Body:**

```json
{
  "bill_type": "tuition_fee",
  "student_id": 123,
  "items": [
    {
      "name": "Tuition Fee - Semester 1",
      "quantity": 1.0,
      "unit_price": 50000.00,
      "tax_percentage": 0.0,
      "category": "tuition"
    }
  ],
  "due_date": "2025-12-31",
  "academic_year": "2024-2025",
  "semester": 1,
  "description": "Semester 1 tuition fees"
}
```

**Response:** `201 Created`

```json
{
  "id": 1,
  "bill_number": "TF20251101001",
  "bill_type": "tuition_fee",
  "student_id": 123,
  "bill_date": "2025-11-10",
  "due_date": "2025-12-31",
  "subtotal": 50000.00,
  "tax_amount": 0.0,
  "total_amount": 50000.00,
  "amount_paid": 0.0,
  "amount_due": 50000.00,
  "status": "draft",
  "academic_year": "2024-2025",
  "semester": 1
}
```

#### Get Bill by ID

```http
GET /bills/{bill_id}
```

#### Get Bill by Number

```http
GET /bills/number/{bill_number}
```

#### Get Student Bills

```http
GET /bills/student/{student_id}?status_filter=pending
```

#### Get Overdue Bills

```http
GET /bills/overdue
```

---

### Fee Structure Templates (T207, T214)

#### Create Fee Structure Template

```http
POST /fee-structures
```

Create reusable fee structure template for programs.

**Request Body:**

```json
{
  "program_id": 1,
  "academic_year": "2024-2025",
  "semester": 1,
  "template_name": "B.Tech CSE - Semester 1",
  "items": [
    {"name": "Tuition Fee", "amount": 50000},
    {"name": "Lab Fee", "amount": 5000},
    {"name": "Library Fee", "amount": 2000}
  ]
}
```

**Permissions:** `billing:admin`

#### Apply Fee Structure to Student

```http
POST /fee-structures/{template_id}/apply/{student_id}?due_date=2025-12-31
```

Automatically generates bill from template.

---

### Bulk Bill Generation (T210, T215)

#### Bulk Generate Bills

```http
POST /bills/bulk-generate
```

Generate bills for multiple students at once.

**Request Body:**

```json
{
  "bill_type": "tuition_fee",
  "student_ids": [101, 102, 103, 104],
  "items": [
    {
      "name": "Tuition Fee",
      "quantity": 1.0,
      "unit_price": 50000.00
    }
  ],
  "due_date": "2025-12-31",
  "academic_year": "2024-2025",
  "semester": 1
}
```

**Response:**

```json
{
  "success_count": 4,
  "error_count": 0,
  "bills": [...],
  "errors": []
}
```

**Permissions:** `billing:bulk_create`

---

### Payment Processing (T216)

#### Record Payment

```http
POST /bills/{bill_id}/payment
```

**Request Body:**

```json
{
  "amount": 25000.00,
  "payment_method": "upi",
  "transaction_id": "UPI123456789"
}
```

**Permissions:** `billing:payment`

---

### Late Fee Management (T208)

#### Apply Late Fees

```http
POST /bills/apply-late-fees?grace_days=7&late_fee_percentage=5.0
```

Apply late fees to all overdue bills.

**Response:**

```json
{
  "message": "Applied late fees to 15 bills",
  "count": 15
}
```

**Permissions:** `billing:admin`

---

### Installment Plans (T209)

#### Create Installment Plan

```http
POST /bills/{bill_id}/installments
```

**Request Body:**

```json
{
  "num_installments": 3,
  "first_installment_date": "2025-12-01"
}
```

**Response:**

```json
{
  "installments": [
    {
      "installment_number": 1,
      "amount": 16666.67,
      "due_date": "2025-12-01",
      "status": "pending"
    },
    {
      "installment_number": 2,
      "amount": 16666.67,
      "due_date": "2025-01-01",
      "status": "pending"
    },
    {
      "installment_number": 3,
      "amount": 16666.66,
      "due_date": "2025-02-01",
      "status": "pending"
    }
  ]
}
```

#### Pay Specific Installment

```http
POST /bills/{bill_id}/installments/{installment_number}/pay
```

**Request Body:**

```json
{
  "amount": 16666.67,
  "payment_method": "upi"
}
```

---

### Bill Printing & PDF (T217)

#### Download Bill PDF

```http
GET /bills/{bill_id}/pdf?download=true
```

Download bill as PDF file.

#### Print Bill

```http
GET /bills/{bill_id}/print
```

Get print-optimized PDF (opens in browser).

**Features:**
- QR code for payment
- Institution letterhead
- Professional formatting
- Print-friendly layout

---

### Email Bills (T213)

#### Email Bill to Recipient

```http
POST /bills/{bill_id}/email
```

**Request Body:**

```json
{
  "recipient_email": "parent@example.com",
  "include_pdf": true
}
```

**Response:**

```json
{
  "message": "Bill emailed successfully"
}
```

**Permissions:** `billing:send`

---

### Bill Cancellation

#### Cancel Bill

```http
POST /bills/{bill_id}/cancel?reason=Duplicate
```

---

## Bill Types

- `tuition_fee`
- `admission_fee`
- `exam_fee`
- `library_fee`
- `laboratory_fee`
- `sports_fee`
- `maintenance_fee`
- `transport_fee`
- `hostel_fee`
- `event_fee`
- `fine`
- And more... (see BillType enum)

## Bill Status

- `draft` - Created but not finalized
- `generated` - Finalized and ready to send
- `sent` - Sent to student/parent
- `partially_paid` - Partial payment received
- `paid` - Fully paid
- `overdue` - Past due date
- `cancelled` - Cancelled
- `refunded` - Payment refunded

## Payment Methods

- `cash`
- `cheque`
- `bank_transfer`
- `upi`
- `credit_card`
- `debit_card`
- `net_banking`
- `online_gateway`

## Permissions

- `billing:read` - View bills
- `billing:create` - Create bills
- `billing:bulk_create` - Bulk generate bills
- `billing:payment` - Record payments
- `billing:send` - Email bills
- `billing:cancel` - Cancel bills
- `billing:admin` - Full billing administration

## Error Codes

- `404` - Bill not found
- `400` - Invalid request (e.g., cannot cancel paid bill)
- `403` - Permission denied
- `500` - Server error

## Examples

### Complete Student Fee Flow

1. **Create fee structure template:**
```bash
POST /fee-structures
```

2. **Apply to all new students:**
```bash
POST /fee-structures/1/apply/101
POST /fee-structures/1/apply/102
# Or use bulk generate
```

3. **Student pays:**
```bash
POST /bills/1/payment
```

4. **Email receipt:**
```bash
POST /bills/1/email
```

### Late Fee Management

Run nightly job:
```bash
POST /bills/apply-late-fees?grace_days=7&late_fee_percentage=5.0
```

### Installment Payment Plan

```bash
# Create plan
POST /bills/1/installments
{
  "num_installments": 3,
  "first_installment_date": "2025-12-01"
}

# Pay first installment
POST /bills/1/installments/1/pay
{
  "amount": 16666.67,
  "payment_method": "upi"
}
```

## Webhooks

Payment gateway webhooks for automatic payment updates:

```http
POST /billing/webhook/payment
```

## Notes

- All amounts are in INR (₹)
- Dates are in ISO 8601 format (YYYY-MM-DD)
- Bills are automatically numbered with type prefix
- PDF generation includes QR codes for payment
- Email functionality requires SMTP configuration
- Late fees are capped at 20% of original amount
- Installment plans split amount evenly with rounding adjustment on last installment

## Implementation Status

✅ All endpoints implemented (T207, T208, T209, T210, T213, T214, T215, T216, T217, T218)
