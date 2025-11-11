# Financial Aid API Documentation

## Overview

The Financial Aid API manages scholarships, grants, fee waivers, and other forms of financial assistance for students.

## Base URL

```
/api/v1/financial-aid
```

## Authentication

All endpoints require authentication and appropriate permissions.

## Endpoints

### Scholarship Management

#### Create Scholarship Program

```http
POST /scholarships
```

Create new scholarship/grant program.

**Request Body:**

```json
{
  "scholarship_name": "Merit Scholarship 2024",
  "scholarship_code": "MERIT2024",
  "aid_type": "merit_scholarship",
  "provider": "Institution",
  "amount": 50000.00,
  "eligibility_criteria": "Minimum 85% marks in previous semester",
  "academic_year": "2024-2025",
  "effective_from": "2024-06-01",
  "minimum_percentage": 85.0,
  "family_income_limit": 500000.00,
  "max_students": 50,
  "application_start_date": "2024-06-01",
  "application_end_date": "2024-07-15"
}
```

**Permissions:** `financial_aid:admin`

#### Get Active Scholarships

```http
GET /scholarships?academic_year=2024-2025&aid_type=merit_scholarship
```

#### Get Scholarship Details

```http
GET /scholarships/{scholarship_id}
```

---

### Aid Applications

#### Apply for Scholarship

```http
POST /applications
```

Student submits scholarship application.

**Request Body:**

```json
{
  "scholarship_id": 1,
  "student_id": 123,
  "academic_year": "2024-2025",
  "semester": 1
}
```

**Permissions:** `financial_aid:apply`

#### Submit Application for Review

```http
POST /applications/{aid_id}/submit
```

Submits draft application for official review.

#### Get Aid Application

```http
GET /applications/{aid_id}
```

#### Get Student's Aid Applications

```http
GET /applications/student/{student_id}?status_filter=approved
```

#### Get Pending Applications

```http
GET /applications/pending
```

Get all applications pending review.

**Permissions:** `financial_aid:review`

---

### Eligibility Verification (T223)

#### Verify Student Eligibility

```http
POST /applications/{aid_id}/verify
```

Verify student meets scholarship eligibility criteria.

**Request Body:**

```json
{
  "student_percentage": 87.5,
  "family_income": 350000.00,
  "category": "General"
}
```

**Response:**

```json
{
  "id": 1,
  "application_number": "MERIT202401",
  "scholarship_id": 1,
  "student_id": 123,
  "academic_year": "2024-2025",
  "status": "under_review",
  "requested_amount": 50000.00,
  "is_eligible": true
}
```

**Permissions:** `financial_aid:verify`

**Eligibility Checks:**
- Minimum percentage requirement
- Family income limit
- Category eligibility
- Other criteria defined in scholarship

---

### Approval Workflow

#### Approve Aid Application

```http
POST /applications/{aid_id}/approve
```

**Request Body:**

```json
{
  "approved_amount": 45000.00,
  "comments": "Approved with reduced amount due to budget constraints"
}
```

**Permissions:** `financial_aid:approve`

#### Reject Aid Application

```http
POST /applications/{aid_id}/reject
```

**Request Body:**

```json
{
  "reason": "Does not meet minimum percentage requirement"
}
```

---

### Disbursement (T224)

#### Disburse Financial Aid

```http
POST /applications/{aid_id}/disburse
```

Process disbursement of approved financial aid.

**Request Body:**

```json
{
  "disbursement_method": "bank_transfer",
  "disbursement_reference": "TXN123456789"
}
```

**Disbursement Methods:**
- `bank_transfer` - Direct bank transfer to student
- `adjustment_in_fee` - Adjust in fee bill
- `cheque` - Issue cheque

**Permissions:** `financial_aid:disburse`

---

### Bill Adjustment (T225)

#### Adjust Aid in Student Bill

```http
POST /applications/{aid_id}/adjust-in-bill
```

Apply financial aid as discount in student's fee bill.

**Request Body:**

```json
{
  "bill_id": 456
}
```

**Process:**
1. Verifies aid is approved
2. Verifies bill belongs to the aid recipient
3. Adds negative line item to bill
4. Updates bill totals
5. Marks aid as disbursed via fee adjustment

**Response:**

```json
{
  "id": 1,
  "application_number": "MERIT202401",
  "status": "disbursed",
  "approved_amount": 50000.00,
  "disbursed_amount": 50000.00,
  "disbursement_method": "adjustment_in_fee",
  "adjusted_bill_id": 456,
  "adjustment_amount": 50000.00
}
```

**Permissions:** `financial_aid:disburse`

---

## Aid Types

- `scholarship` - General scholarship
- `grant` - Grant from external agency
- `fee_waiver` - Fee waiver/concession
- `merit_scholarship` - Merit-based scholarship
- `need_based` - Need-based financial aid
- `sports_scholarship` - Sports achievement scholarship
- `minority_scholarship` - Minority community scholarship
- `sc_st_scholarship` - SC/ST scholarship
- `obc_scholarship` - OBC scholarship
- `government_scholarship` - Government-funded scholarship
- `institutional_scholarship` - Institution-funded scholarship
- `loan` - Educational loan

## Aid Status

- `draft` - Application created but not submitted
- `submitted` - Application submitted for review
- `under_review` - Being reviewed for eligibility
- `approved` - Application approved
- `rejected` - Application rejected
- `disbursed` - Aid amount disbursed
- `cancelled` - Application cancelled

## Permissions

- `financial_aid:read` - View scholarships and applications
- `financial_aid:apply` - Submit aid applications
- `financial_aid:verify` - Verify eligibility
- `financial_aid:review` - Review applications
- `financial_aid:approve` - Approve/reject applications
- `financial_aid:disburse` - Disburse aid
- `financial_aid:admin` - Full administration

## Error Codes

- `404` - Scholarship or application not found
- `400` - Invalid request (e.g., already applied, max beneficiaries reached)
- `403` - Permission denied

## Complete Workflow Example

### 1. Create Scholarship Program

```bash
POST /scholarships
{
  "scholarship_name": "Merit Scholarship 2024",
  "scholarship_code": "MERIT2024",
  "aid_type": "merit_scholarship",
  "provider": "Institution",
  "amount": 50000.00,
  "eligibility_criteria": "Minimum 85% marks",
  "academic_year": "2024-2025",
  "effective_from": "2024-06-01",
  "minimum_percentage": 85.0,
  "max_students": 50
}
```

### 2. Student Applies

```bash
POST /applications
{
  "scholarship_id": 1,
  "student_id": 123,
  "academic_year": "2024-2025"
}
```

### 3. Submit for Review

```bash
POST /applications/1/submit
```

### 4. Verify Eligibility

```bash
POST /applications/1/verify
{
  "student_percentage": 87.5,
  "family_income": 350000.00,
  "category": "General"
}
```

### 5. Approve Application

```bash
POST /applications/1/approve
{
  "approved_amount": 50000.00,
  "comments": "Approved"
}
```

### 6. Adjust in Fee Bill

```bash
POST /applications/1/adjust-in-bill
{
  "bill_id": 456
}
```

**Result:** Student's fee bill reduced by ₹50,000

---

## Integration with Billing

When aid is adjusted in bill:

1. Creates negative line item in bill
2. Updates bill discount_amount
3. Reduces total_amount
4. Recalculates amount_due
5. Links aid to bill for tracking
6. Marks aid as disbursed

**Example Bill After Aid Adjustment:**

```
Original Bill Amount: ₹100,000
Financial Aid Applied: -₹50,000
------------------------------------
Final Amount Due: ₹50,000
```

## Reports

### Scholarship Utilization Report

```http
GET /reports/scholarship-utilization?academic_year=2024-2025
```

Shows:
- Total scholarships available
- Current beneficiaries vs max limit
- Total amount disbursed
- Pending applications

### Student Aid Summary

```http
GET /reports/student-aid-summary/{student_id}
```

Shows all financial aid received by student.

## Notes

- Application numbers are auto-generated: `{SCHOLARSHIP_CODE}{YEAR}{SEQ}`
- Eligibility is verified before approval
- Maximum beneficiary limit is enforced
- Aid can only be disbursed once approved
- Bill adjustment automatically marks aid as disbursed
- Scholarships can be renewable or one-time

## Implementation Status

✅ All endpoints implemented (T219-T227)
- [X] T219 - Scholarship model
- [X] T220 - Financial aid model  
- [X] T221 - Aid application model
- [X] T222 - Financial aid service
- [X] T223 - Eligibility verification
- [X] T224 - Aid disbursement workflow
- [X] T225 - Bill adjustment integration
- [X] T226 - Financial aid endpoints
- [X] T227 - API documentation
