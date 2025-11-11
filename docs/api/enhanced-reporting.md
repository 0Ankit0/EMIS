# Enhanced Reporting API - Quick Reference

## Teacher Hierarchy API

### Base URL: `/hr/hierarchy`

#### Create/Update Teacher Hierarchy
```http
POST /hr/hierarchy/teachers
Content-Type: application/json

{
  "teacher_id": 123,
  "designation": "Head of Department",
  "department_id": 5,
  "reports_to": null,
  "is_department_head": true,
  "is_program_coordinator": false,
  "program_id": null,
  "subject_coordinator_ids": [10, 11],
  "effective_from": "2024-04-01"
}
```

#### Get Teacher Hierarchy
```http
GET /hr/hierarchy/teachers/{teacher_id}
```

#### Get Organization Chart
```http
GET /hr/hierarchy/org-chart
```

#### Get Department Hierarchy
```http
GET /hr/hierarchy/departments/{department_id}
```

#### Get Subordinates
```http
GET /hr/hierarchy/teachers/{teacher_id}/subordinates
```

#### Get Teachers by Designation
```http
GET /hr/hierarchy/designation/Professor
```

#### Get All Department Heads
```http
GET /hr/hierarchy/department-heads
```

---

## Annual Reports API

### Base URL: `/reports/annual`

#### Generate Annual Report
```http
POST /reports/annual?financial_year=2024-2025
```

**Response:**
```json
{
  "id": 1,
  "report_number": "AR20242025",
  "financial_year": "2024-2025",
  "total_annual_revenue": 5000000.00,
  "total_annual_expenses": 4200000.00,
  "net_annual_profit_loss": 800000.00,
  "annual_profit_margin": 16.0,
  "status": "completed"
}
```

#### List Annual Reports
```http
GET /reports/annual
GET /reports/annual?financial_year=2024-2025
```

#### Get Annual Report Details
```http
GET /reports/annual/{report_id}
```

**Response includes:**
- Executive summary
- Quarterly breakdown (Q1-Q4)
- Monthly breakdown (Jan-Dec)
- Salary analysis
- Department performance
- Student metrics
- Faculty metrics
- Balance sheet
- Cash flow
- Financial ratios
- Comparative analysis

#### Download Annual Report PDF
```http
# Download as attachment
GET /reports/annual/{report_id}/pdf?download=true

# View inline (for browser viewing)
GET /reports/annual/{report_id}/pdf?download=false
```

#### Download Annual Report Excel
```http
GET /reports/annual/{report_id}/excel
```

#### Print Annual Report
```http
GET /reports/annual/{report_id}/print
```
*Opens in browser with print dialog*

#### Approve Annual Report
```http
POST /reports/annual/{report_id}/approve
```

---

## Enhanced Quarterly Reports

### Quarterly Report with Print/Save

#### Download Quarterly Report PDF
```http
# Download
GET /reports/quarterly/{report_id}/pdf?download=true

# View inline
GET /reports/quarterly/{report_id}/pdf?download=false
```

#### Print Quarterly Report
```http
GET /reports/quarterly/{report_id}/print
```

#### Download Quarterly Report Excel
```http
GET /reports/quarterly/{report_id}/excel
```

---

## Bills with Print/Save

### Bill PDF and Print

#### Download Bill PDF
```http
# Download
GET /billing/bills/{bill_id}/pdf?download=true

# View inline
GET /billing/bills/{bill_id}/pdf?download=false
```

#### Print Bill
```http
GET /billing/bills/{bill_id}/print
```

---

## Response Examples

### Annual Report Detail Response
```json
{
  "id": 1,
  "report_number": "AR20242025",
  "financial_year": "2024-2025",
  "start_date": "2024-04-01",
  "end_date": "2025-03-31",
  
  "total_annual_revenue": 5000000.00,
  "total_annual_expenses": 4200000.00,
  "net_annual_profit_loss": 800000.00,
  "annual_profit_margin": 16.0,
  
  "q1_income": 1200000.00,
  "q2_income": 1300000.00,
  "q3_income": 1250000.00,
  "q4_income": 1250000.00,
  
  "q1_expenses": 1050000.00,
  "q2_expenses": 1050000.00,
  "q3_expenses": 1050000.00,
  "q4_expenses": 1050000.00,
  
  "monthly_income_breakdown": {
    "4": 400000.00,
    "5": 400000.00,
    "6": 400000.00,
    ...
  },
  
  "total_salary_expenses": 2500000.00,
  "faculty_salary_total": 1750000.00,
  "staff_salary_total": 750000.00,
  
  "annual_fees_collected": 3500000.00,
  "annual_fees_outstanding": 500000.00,
  "collection_rate": 87.5,
  
  "total_assets": 10000000.00,
  "total_liabilities": 3000000.00,
  "total_equity": 7000000.00,
  
  "current_ratio": 2.5,
  "return_on_assets": 8.0,
  "operating_margin": 16.0,
  "debt_to_equity": 0.43,
  
  "status": "completed",
  "generated_at": "2025-04-15T10:30:00Z"
}
```

### Organization Chart Response
```json
{
  "organization": [
    {
      "id": 1,
      "designation": "Dean",
      "department_id": 1,
      "level": 1,
      "is_hod": false,
      "subordinates": [
        {
          "id": 5,
          "designation": "HOD",
          "department_id": 2,
          "level": 2,
          "is_hod": true,
          "subordinates": [
            {
              "id": 10,
              "designation": "Professor",
              "level": 3,
              "subordinates": []
            }
          ]
        }
      ]
    }
  ],
  "total_teachers": 45
}
```

---

## Permissions Required

| Endpoint | Permission |
|----------|-----------|
| POST /hr/hierarchy/* | `hr:admin` |
| GET /hr/hierarchy/* | `hr:read` |
| POST /reports/annual | `reports:generate` |
| GET /reports/annual/* | `reports:read` |
| POST /reports/annual/*/approve | `reports:approve` |
| GET /billing/bills/*/pdf | `billing:read` |
| GET /reports/quarterly/*/pdf | `reports:read` |

---

## Financial Ratios Reference

### Current Ratio
```
Current Ratio = Current Assets / Current Liabilities

Interpretation:
  > 2.0  = Excellent
  1.5-2.0 = Good
  1.0-1.5 = Average
  < 1.0  = Poor (liquidity issues)
```

### Return on Assets (ROA)
```
ROA = (Net Profit / Total Assets) × 100

Interpretation:
  > 15% = Excellent
  10-15% = Good
  5-10% = Average
  < 5% = Poor
```

### Operating Margin
```
Operating Margin = (Net Profit / Revenue) × 100

Interpretation:
  > 20% = Excellent
  15-20% = Good
  10-15% = Average
  < 10% = Poor
```

### Debt to Equity
```
Debt to Equity = Total Liabilities / Total Equity

Interpretation:
  < 0.5 = Very Low Risk
  0.5-1.0 = Low Risk
  1.0-2.0 = Moderate Risk
  > 2.0 = High Risk
```

---

## Common Use Cases

### 1. Set Up Teacher Hierarchy

```bash
# Set HOD
curl -X POST http://localhost:8000/hr/hierarchy/teachers \
  -H "Content-Type: application/json" \
  -d '{
    "teacher_id": 5,
    "designation": "Head of Department",
    "department_id": 2,
    "is_department_head": true
  }'

# Set Professor reporting to HOD
curl -X POST http://localhost:8000/hr/hierarchy/teachers \
  -H "Content-Type: application/json" \
  -d '{
    "teacher_id": 10,
    "designation": "Professor",
    "department_id": 2,
    "reports_to": 5
  }'
```

### 2. Generate and Download Annual Report

```bash
# Generate
curl -X POST http://localhost:8000/reports/annual?financial_year=2024-2025

# Download PDF
curl http://localhost:8000/reports/annual/1/pdf?download=true \
  -o Annual_Report_2024-2025.pdf

# Download Excel
curl http://localhost:8000/reports/annual/1/excel \
  -o Annual_Report_2024-2025.xlsx
```

### 3. Print Reports

```html
<!-- In HTML/Frontend -->
<button onclick="window.open('/reports/annual/1/print', '_blank')">
  Print Annual Report
</button>

<button onclick="window.open('/reports/quarterly/1/print', '_blank')">
  Print Quarterly Report
</button>

<button onclick="window.open('/billing/bills/1/print', '_blank')">
  Print Bill
</button>
```

---

## Error Responses

### 404 Not Found
```json
{
  "detail": "Annual report 999 not found"
}
```

### 400 Bad Request
```json
{
  "detail": "Quarter must be between 1 and 4"
}
```

### 403 Forbidden
```json
{
  "detail": "Insufficient permissions"
}
```

---

## Notes

- All financial amounts are in the institution's base currency
- Dates are in ISO 8601 format (YYYY-MM-DD)
- Financial year format: "YYYY-YYYY" (e.g., "2024-2025")
- PDF files are generated on-demand and cached in /tmp
- Excel exports include multiple sheets with detailed breakdowns
- Print endpoints return PDF with inline disposition for browser printing
- All endpoints require authentication via JWT token
- Permissions are enforced via RBAC middleware
