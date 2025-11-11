# Placement API Documentation

## Base URL
`/api/placement`

## Overview
The Placement API manages campus placements, job postings, applications, interviews, and offers.

## Authentication
All endpoints require authentication.

---

## Endpoints

### Company Management

#### Create Company
```http
POST /api/placement/companies
```

**Request Body:**
```json
{
  "name": "TechCorp India",
  "industry": "Information Technology",
  "website": "https://techcorp.com",
  "description": "Leading IT services company",
  "contact_person": "HR Manager",
  "contact_email": "hr@techcorp.com",
  "contact_phone": "+91-9876543210"
}
```

#### Get All Companies
```http
GET /api/placement/companies?is_active=true
```

#### Get Company Details
```http
GET /api/placement/companies/{company_id}
```

### Job Posting Management

#### Create Job Posting
```http
POST /api/placement/jobs
```

**Request Body:**
```json
{
  "company_id": 1,
  "job_title": "Software Engineer",
  "job_description": "Develop web applications",
  "job_type": "Full-time",
  "location": "Bangalore",
  "salary_min": 600000.00,
  "salary_max": 1200000.00,
  "required_skills": "Java, Spring Boot, React",
  "min_cgpa": 7.0,
  "eligible_programs": "B.Tech CSE, MCA",
  "vacancies": 10,
  "application_deadline": "2024-02-28"
}
```

#### Get Job Postings
```http
GET /api/placement/jobs?company_id=1&is_active=true
```

**Response:**
```json
[
  {
    "id": 1,
    "company_name": "TechCorp India",
    "job_title": "Software Engineer",
    "location": "Bangalore",
    "salary_min": 600000.00,
    "salary_max": 1200000.00,
    "application_deadline": "2024-02-28",
    "applications_count": 150,
    "is_active": true
  }
]
```

#### Get Job Details
```http
GET /api/placement/jobs/{job_id}
```

### Application Management

#### Apply for Job
```http
POST /api/placement/jobs/{job_id}/apply
```

**Request Body:**
```json
{
  "resume_url": "https://storage.example.com/resume.pdf",
  "cover_letter": "I am interested in this position...",
  "additional_documents": "https://storage.example.com/certificates.pdf"
}
```

**Response:**
```json
{
  "message": "Application submitted successfully",
  "application_id": 123
}
```

#### Get Student Applications
```http
GET /api/placement/students/{student_id}/applications?status=submitted
```

**Response:**
```json
[
  {
    "id": 123,
    "job_title": "Software Engineer",
    "company_name": "TechCorp India",
    "status": "submitted",
    "applied_date": "2024-01-15T10:00:00"
  }
]
```

#### Get Job Applications
```http
GET /api/placement/jobs/{job_id}/applications?status=shortlisted
```

#### Update Application Status
```http
PUT /api/placement/applications/{application_id}/status?status=shortlisted
```

### Interview Management

#### Schedule Interview
```http
POST /api/placement/interviews
```

**Request Body:**
```json
{
  "application_id": 123,
  "scheduled_date": "2024-02-15T10:00:00",
  "interview_type": "Technical",
  "venue": "Room 301",
  "interviewer_name": "Mr. Kumar",
  "notes": "Focus on DSA and system design"
}
```

#### Update Interview
```http
PUT /api/placement/interviews/{interview_id}
```

**Request Body:**
```json
{
  "status": "completed",
  "feedback": "Good technical skills",
  "rating": 8
}
```

#### Get Student Interviews
```http
GET /api/placement/students/{student_id}/interviews
```

**Response:**
```json
[
  {
    "id": 1,
    "job_title": "Software Engineer",
    "company_name": "TechCorp India",
    "scheduled_date": "2024-02-15T10:00:00",
    "interview_type": "Technical",
    "status": "scheduled",
    "venue": "Room 301"
  }
]
```

### Placement Offer Management

#### Create Offer
```http
POST /api/placement/offers
```

**Request Body:**
```json
{
  "application_id": 123,
  "offer_date": "2024-03-01",
  "joining_date": "2024-07-01",
  "package_amount": 800000.00,
  "designation": "Software Engineer",
  "location": "Bangalore",
  "offer_letter_url": "https://storage.example.com/offer.pdf"
}
```

#### Accept Offer
```http
POST /api/placement/offers/{offer_id}/accept
```

**Response:**
```json
{
  "message": "Offer accepted successfully",
  "offer_id": 1
}
```

#### Get Student Offers
```http
GET /api/placement/students/{student_id}/offers
```

**Response:**
```json
[
  {
    "id": 1,
    "company_name": "TechCorp India",
    "designation": "Software Engineer",
    "package_amount": 800000.00,
    "offer_date": "2024-03-01",
    "joining_date": "2024-07-01",
    "is_accepted": true
  }
]
```

### Statistics & Reports

#### Get Placement Statistics
```http
GET /api/placement/statistics?academic_year_id=1
```

**Response:**
```json
{
  "total_applications": 500,
  "placed_students": 350,
  "placement_rate": 70.0,
  "total_offers": 380,
  "accepted_offers": 350,
  "average_package": 750000.00,
  "highest_package": 2500000.00,
  "companies_participated": 45
}
```

#### Get Company Report
```http
GET /api/placement/companies/{company_id}/report
```

**Response:**
```json
{
  "company": {
    "id": 1,
    "name": "TechCorp India",
    "industry": "Information Technology"
  },
  "job_postings": 5,
  "total_applications": 150,
  "total_offers": 12,
  "placed_students": 10
}
```

---

## Data Models

### Company
```json
{
  "id": 1,
  "name": "TechCorp India",
  "industry": "Information Technology",
  "website": "https://techcorp.com",
  "contact_person": "HR Manager",
  "is_active": true
}
```

### Job Posting
```json
{
  "id": 1,
  "company_id": 1,
  "job_title": "Software Engineer",
  "job_type": "Full-time",
  "location": "Bangalore",
  "salary_min": 600000.00,
  "salary_max": 1200000.00,
  "min_cgpa": 7.0,
  "application_deadline": "2024-02-28",
  "is_active": true
}
```

### Placement Application
```json
{
  "id": 123,
  "student_id": 1001,
  "job_posting_id": 1,
  "status": "submitted",
  "applied_date": "2024-01-15T10:00:00"
}
```

### Interview
```json
{
  "id": 1,
  "application_id": 123,
  "scheduled_date": "2024-02-15T10:00:00",
  "interview_type": "Technical",
  "status": "scheduled",
  "venue": "Room 301"
}
```

### Placement Offer
```json
{
  "id": 1,
  "application_id": 123,
  "offer_date": "2024-03-01",
  "joining_date": "2024-07-01",
  "package_amount": 800000.00,
  "designation": "Software Engineer",
  "is_accepted": true
}
```

---

## Application Status

- `submitted` - Application submitted
- `under_review` - Under review
- `shortlisted` - Shortlisted for interview
- `rejected` - Application rejected
- `offered` - Offer made
- `placed` - Student placed

## Interview Status

- `scheduled` - Interview scheduled
- `completed` - Interview completed
- `cancelled` - Interview cancelled
- `no_show` - Candidate didn't show up
