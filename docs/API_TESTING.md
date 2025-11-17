# API Testing Guide

## Using Postman

### 1. Import Environment

Create a new environment in Postman with these variables:

```json
{
  "base_url": "http://localhost:8000",
  "access_token": "",
  "refresh_token": ""
}
```

### 2. Test Authentication Flow

#### A. Register User

```
POST {{base_url}}/api/v1/auth/register/
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "password_confirm": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe"
}
```

#### B. Login

```
POST {{base_url}}/api/v1/auth/login/
Content-Type: application/json

{
  "username": "johndoe",
  "password": "SecurePass123!"
}
```

**Save tokens from response:**
- Copy `access` to `access_token` variable
- Copy `refresh` to `refresh_token` variable

#### C. Get Current User

```
GET {{base_url}}/api/v1/auth/me/
Authorization: Bearer {{access_token}}
```

#### D. Refresh Token

```
POST {{base_url}}/api/v1/auth/refresh/
Content-Type: application/json

{
  "refresh": "{{refresh_token}}"
}
```

### 3. Test User Management (Admin Only)

#### List Users

```
GET {{base_url}}/api/v1/auth/users/?page=1&page_size=20
Authorization: Bearer {{access_token}}
```

#### Get Specific User

```
GET {{base_url}}/api/v1/auth/users/{user_id}/
Authorization: Bearer {{access_token}}
```

#### Update User

```
PUT {{base_url}}/api/v1/auth/users/{user_id}/update/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "first_name": "Updated",
  "last_name": "Name",
  "email": "updated@example.com"
}
```

### 4. Test Role Management

#### List All Roles

```
GET {{base_url}}/api/v1/auth/roles/
Authorization: Bearer {{access_token}}
```

#### Create Role

```
POST {{base_url}}/api/v1/auth/roles/create/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "name": "Custom Role",
  "description": "A custom role for testing"
}
```

#### Assign Role to User

```
POST {{base_url}}/api/v1/auth/users/{user_id}/roles/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "role_id": "{role_id}"
}
```

### 5. Test Audit Logs

#### View Audit Logs

```
GET {{base_url}}/api/v1/auth/audit/logs/?page=1&action=login
Authorization: Bearer {{access_token}}
```

#### Get User Activity

```
GET {{base_url}}/api/v1/auth/audit/users/{user_id}/activity/?days=30
Authorization: Bearer {{access_token}}
```

#### Get Security Events

```
GET {{base_url}}/api/v1/auth/audit/security-events/?hours=24
Authorization: Bearer {{access_token}}
```

## Using cURL

### Quick Test Script

Save as `test_api.sh`:

```bash
#!/bin/bash

BASE_URL="http://localhost:8000"

# Register user
echo "Registering user..."
curl -X POST $BASE_URL/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "first_name": "Test",
    "last_name": "User"
  }'

# Login
echo -e "\n\nLogging in..."
RESPONSE=$(curl -s -X POST $BASE_URL/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "SecurePass123!"
  }')

# Extract token
TOKEN=$(echo $RESPONSE | jq -r '.access')

echo -e "\n\nAccess Token: $TOKEN"

# Get current user
echo -e "\n\nGetting current user..."
curl -X GET $BASE_URL/api/v1/auth/me/ \
  -H "Authorization: Bearer $TOKEN"

echo -e "\n\nDone!"
```

Make it executable:
```bash
chmod +x test_api.sh
./test_api.sh
```

## Using Python Requests

```python
import requests

BASE_URL = "http://localhost:8000"

# Register
response = requests.post(
    f"{BASE_URL}/api/v1/auth/register/",
    json={
        "username": "pythonuser",
        "email": "python@example.com",
        "password": "SecurePass123!",
        "password_confirm": "SecurePass123!",
        "first_name": "Python",
        "last_name": "User"
    }
)
print("Register:", response.json())

# Login
response = requests.post(
    f"{BASE_URL}/api/v1/auth/login/",
    json={
        "username": "pythonuser",
        "password": "SecurePass123!"
    }
)
data = response.json()
access_token = data['access']
print("Login successful, token:", access_token[:20] + "...")

# Get current user
response = requests.get(
    f"{BASE_URL}/api/v1/auth/me/",
    headers={"Authorization": f"Bearer {access_token}"}
)
print("Current user:", response.json())

# List users
response = requests.get(
    f"{BASE_URL}/api/v1/auth/users/",
    headers={"Authorization": f"Bearer {access_token}"}
)
print("Users:", response.json())
```

## Expected Responses

### Successful Login

```json
{
  "user": {
    "id": "uuid-here",
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User",
    "roles": [],
    "is_active": true
  },
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access_expires_in": 1800,
  "refresh_expires_in": 604800
}
```

### Error Response

```json
{
  "error": {
    "code": "AUTH_001",
    "message": "Invalid credentials",
    "correlation_id": "abc123-def456",
    "timestamp": "2024-11-16T12:00:00Z"
  }
}
```

### Paginated Response

```json
{
  "results": [...],
  "page_info": {
    "total": 100,
    "page": 1,
    "page_size": 20,
    "total_pages": 5
  }
}
```

## Error Codes Reference

- `AUTH_001`: Invalid credentials
- `AUTH_003`: Invalid or expired token
- `AUTH_006`: Account inactive
- `AUTH_012`: User not found
- `AUTH_013`: Email already exists
- `AUTH_014`: Username already exists
- `CORE_002`: Resource not found
- `CORE_003`: Validation error

## Rate Limiting

(To be implemented)

## Webhooks

(To be implemented)

## Best Practices

1. Always use HTTPS in production
2. Store tokens securely (not in localStorage)
3. Refresh tokens before they expire
4. Handle 401 errors by refreshing token
5. Implement proper error handling
6. Use pagination for large datasets
7. Log all API errors for debugging
