# API Documentation

## Overview

The EMIS API provides RESTful endpoints for managing all aspects of an educational institution, including:

- Authentication & User Management
- Admissions & Applications
- Course Management & Delivery
- Student Enrollment & Records
- Finance & Fee Management
- Analytics & Reporting

## Base URL

```
http://localhost:8000/api/v1/
```

## Authentication

All API endpoints require authentication using JWT (JSON Web Tokens).

### Login

**Endpoint:** `POST /auth/login`

**Request:**
```json
{
  "username": "student@example.com",
  "password": "your_password"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "username": "student@example.com",
    "email": "student@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "roles": ["student"]
  }
}
```

### Using Access Token

Include the access token in the Authorization header:

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### Refresh Token

**Endpoint:** `POST /auth/refresh`

**Request:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

## Pagination

List endpoints support pagination with the following query parameters:

- `page`: Page number (default: 1)
- `page_size`: Number of items per page (default: 20, max: 100)

**Example:**
```
GET /api/v1/users?page=2&page_size=50
```

**Response:**
```json
{
  "results": [...],
  "page_info": {
    "count": 150,
    "next": "http://localhost:8000/api/v1/users?page=3&page_size=50",
    "previous": "http://localhost:8000/api/v1/users?page=1&page_size=50",
    "page": 2,
    "page_size": 50,
    "total_pages": 3
  }
}
```

## Filtering & Search

List endpoints support filtering and full-text search:

- `search`: Full-text search query
- Custom filters vary by endpoint (e.g., `status`, `program`, `date_range`)

**Example:**
```
GET /api/v1/courses?search=mathematics&status=active
```

## Error Responses

All errors follow a consistent format:

```json
{
  "code": "AUTH_001",
  "message": "Invalid credentials",
  "correlation_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

### Common Error Codes

- `AUTH_001`: Invalid credentials
- `AUTH_002`: Token expired
- `CORE_001`: Validation error
- `CORE_002`: Resource not found
- `CORE_003`: Permission denied

## Rate Limiting

API endpoints are rate limited to prevent abuse:

- **Authentication endpoints**: 5 requests per 5 minutes
- **Other endpoints**: 100 requests per minute

Rate limit exceeded response:
```json
{
  "error": "Rate limit exceeded",
  "code": "RATE_LIMIT_EXCEEDED",
  "message": "Too many requests. Please try again in 300 seconds.",
  "retry_after": 300
}
```

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login and get tokens |
| POST | `/auth/logout` | Logout (invalidate token) |
| POST | `/auth/refresh` | Refresh access token |

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users/` | List all users |
| GET | `/users/{id}` | Get user details |
| PUT | `/users/{id}` | Update user |
| DELETE | `/users/{id}` | Delete user |

### Admissions

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/admissions/applications/` | Submit application |
| GET | `/admissions/applications/` | List applications |
| GET | `/admissions/applications/{id}` | Get application details |
| PATCH | `/admissions/applications/{id}/status` | Update application status |
| POST | `/admissions/merit-lists/` | Generate merit list |
| GET | `/admissions/merit-lists/` | List merit lists |

### Courses

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/courses/` | Create course |
| GET | `/courses/` | List courses |
| GET | `/courses/{id}` | Get course details |
| PUT | `/courses/{id}` | Update course |
| POST | `/courses/{id}/modules` | Add module to course |
| POST | `/assignments/` | Create assignment |
| POST | `/submissions/` | Submit assignment |
| POST | `/grades/` | Record grade |

### Finance

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/finance/fee-structures/` | Create fee structure |
| GET | `/finance/fee-structures/` | List fee structures |
| POST | `/finance/invoices/` | Generate invoice |
| GET | `/finance/invoices/` | List invoices |
| POST | `/finance/payments/` | Record payment |
| GET | `/finance/reports/fee-collection` | Generate fee collection report |

### Analytics

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/dashboard/` | Get dashboard metrics |
| GET | `/dashboard/admissions` | Get admissions metrics |
| GET | `/dashboard/attendance` | Get attendance metrics |
| GET | `/dashboard/finance` | Get finance metrics |
| GET | `/dashboard/courses` | Get course metrics |

### Health & Monitoring

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health/` | Basic health check |
| GET | `/readiness/` | Readiness check (DB + Redis) |
| GET | `/liveness/` | Liveness check |
| GET | `/metrics/` | Prometheus metrics |

## Interactive Documentation

For interactive API documentation with request/response examples:

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

## Support

For API support or questions, contact: support@emis.example.com
