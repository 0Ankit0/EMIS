# Authentication & Authorization Guide

## Overview

EMIS uses a comprehensive authentication and authorization system based on:

- **JWT (JSON Web Tokens)** for stateless authentication
- **Role-Based Access Control (RBAC)** for authorization
- **Audit Logging** for security tracking

## Authentication Flow

### 1. User Registration

```python
POST /api/v1/auth/register

{
  "username": "john.doe",
  "email": "john.doe@example.com",
  "password": "SecurePassword123!",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response:**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "username": "john.doe",
  "email": "john.doe@example.com",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z"
}
```

### 2. User Login

```python
POST /api/v1/auth/login

{
  "username": "john.doe@example.com",
  "password": "SecurePassword123!"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "username": "john.doe",
    "email": "john.doe@example.com",
    "roles": ["student"]
  }
}
```

### 3. Using Access Tokens

Include the access token in API requests:

```python
import requests

headers = {
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGc...'
}

response = requests.get(
    'http://localhost:8000/api/v1/users/',
    headers=headers
)
```

### 4. Token Refresh

Access tokens expire after 30 minutes. Use the refresh token to get a new access token:

```python
POST /api/v1/auth/refresh

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 5. Logout

```python
POST /api/v1/auth/logout

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

## Role-Based Access Control (RBAC)

### Built-in Roles

EMIS provides 5 default roles with different permission levels:

1. **Student**: Basic access to courses, assignments, grades
2. **Faculty**: Manage courses, grades, assignments
3. **Staff**: Administrative tasks, admissions processing
4. **Admin**: Full system access, user management
5. **Management**: Analytics, reports, dashboard access

### Permission Model

Permissions are organized by:
- **Resource Group**: e.g., users, courses, admissions
- **Action**: create, read, update, delete

Example permissions:
- `users:create` - Create new users
- `courses:read` - View courses
- `admissions:update` - Update applications
- `finance:delete` - Delete invoices

### Checking Permissions

#### In Views (Decorator)

```python
from apps.core.middleware.rbac import require_permission

@require_permission('courses:create')
def create_course(request):
    # Only users with 'courses:create' permission can access
    pass
```

#### In Code

```python
from apps.authentication.services.role_service import RoleService

# Check if user has permission
has_permission = RoleService.user_has_permission(
    user=request.user,
    resource_group='courses',
    action='create'
)
```

### Assigning Roles

#### Via API

```python
POST /api/v1/roles/{role_id}/assign

{
  "user_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

#### Programmatically

```python
from apps.authentication.services.role_service import RoleService

RoleService.assign_role_to_user(
    user_id=user.id,
    role_id=role.id
)
```

## Audit Logging

All sensitive actions are automatically logged:

### Viewing Audit Logs

```python
GET /api/v1/audit-logs/

# Filter by user
GET /api/v1/audit-logs/?actor_id={user_id}

# Filter by action
GET /api/v1/audit-logs/?action=login

# Filter by date range
GET /api/v1/audit-logs/?start_date=2024-01-01&end_date=2024-01-31
```

### Audit Log Entry

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "actor": {
    "id": "user-id",
    "username": "john.doe"
  },
  "action": "update",
  "target_model": "Application",
  "target_id": "app-id",
  "timestamp": "2024-01-15T10:30:00Z",
  "outcome": "success",
  "details": {
    "status_change": "submitted -> accepted"
  }
}
```

## Security Best Practices

### 1. Password Requirements

- Minimum 8 characters
- Must include uppercase, lowercase, numbers
- Cannot be common password

### 2. Token Management

- Store tokens securely (never in localStorage if possible)
- Refresh tokens before expiry
- Clear tokens on logout

### 3. Rate Limiting

Authentication endpoints are rate-limited:
- Login: 5 attempts per 5 minutes
- Registration: 3 attempts per 10 minutes

### 4. Session Management

- Access tokens expire after 30 minutes
- Refresh tokens expire after 7 days
- Tokens are rotated on refresh

## Common Use Cases

### 1. Student Access

```python
# Student logs in
POST /api/v1/auth/login
{
  "username": "student@example.com",
  "password": "password"
}

# Student views their courses
GET /api/v1/courses/?student_id=me
Headers: Authorization: Bearer {access_token}

# Student submits assignment
POST /api/v1/submissions/
Headers: Authorization: Bearer {access_token}
{
  "assignment_id": "assignment-id",
  "content": "..."
}
```

### 2. Faculty Access

```python
# Faculty logs in
POST /api/v1/auth/login

# Faculty creates course
POST /api/v1/courses/
Headers: Authorization: Bearer {access_token}
{
  "title": "Introduction to Python",
  "code": "CS101"
}

# Faculty grades assignment
POST /api/v1/grades/
Headers: Authorization: Bearer {access_token}
{
  "submission_id": "submission-id",
  "grade": 85,
  "feedback": "Good work!"
}
```

### 3. Admin Access

```python
# Admin creates new user
POST /api/v1/users/
Headers: Authorization: Bearer {access_token}
{
  "username": "new.faculty",
  "email": "faculty@example.com",
  "role": "faculty"
}

# Admin assigns permissions
POST /api/v1/permissions/assign
Headers: Authorization: Bearer {access_token}
{
  "user_id": "user-id",
  "permissions": ["courses:create", "courses:update"]
}
```

## Troubleshooting

### Invalid Credentials

```json
{
  "code": "AUTH_001",
  "message": "Invalid credentials"
}
```

**Solution**: Verify username and password are correct

### Token Expired

```json
{
  "code": "AUTH_002",
  "message": "Token has expired"
}
```

**Solution**: Use refresh token to get new access token

### Permission Denied

```json
{
  "code": "CORE_003",
  "message": "Permission denied"
}
```

**Solution**: Verify user has required role/permission

## API Reference

For complete API documentation, see:
- [API Documentation](../api/README.md)
- [Swagger UI](http://localhost:8000/api/docs/)
