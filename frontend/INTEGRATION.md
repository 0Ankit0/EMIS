# EMIS Frontend Integration Guide

## Overview

This document describes how the Streamlit frontend integrates with the FastAPI backend.

## Architecture

```
┌─────────────────┐      HTTP/REST API     ┌─────────────────┐
│                 │ ◄──────────────────────► │                 │
│   Streamlit     │                          │   FastAPI       │
│   Frontend      │                          │   Backend       │
│   (Port 8501)   │                          │   (Port 8000)   │
│                 │                          │                 │
└─────────────────┘                          └─────────────────┘
        │                                             │
        │                                             │
        ▼                                             ▼
   Browser UI                                   PostgreSQL DB
```

## API Communication

### Authentication Flow

1. **Login Request**:
```python
# Frontend (utils/api_client.py)
response = api_client.login(username, password)
# Returns: {"access_token": "...", "user": {...}}
```

2. **Token Storage**:
```python
# Stored in Streamlit session state
st.session_state.access_token = response["access_token"]
st.session_state.user = response["user"]
```

3. **Authenticated Requests**:
```python
# Token automatically added to headers
headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
```

### API Endpoints Usage

#### Students Module

**GET /api/students**
```python
# Frontend
students = api_client.get("/api/students", params={"page": 1, "limit": 50})
# Returns: {"items": [...], "total": 100, "page": 1}
```

**POST /api/students**
```python
# Frontend
student_data = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com"
}
result = api_client.post("/api/students", student_data)
```

**GET /api/students/{id}**
```python
# Frontend
student = api_client.get(f"/api/students/{student_id}")
```

**PUT /api/students/{id}**
```python
# Frontend
api_client.put(f"/api/students/{student_id}", updated_data)
```

**DELETE /api/students/{id}**
```python
# Frontend
api_client.delete(f"/api/students/{student_id}")
```

#### Library Module

**GET /api/library/books**
```python
books = api_client.get("/api/library/books")
```

**POST /api/library/issue**
```python
issue_data = {
    "book_id": 123,
    "member_id": 456,
    "issue_date": "2024-01-15"
}
api_client.post("/api/library/issue", issue_data)
```

#### Finance Module

**GET /api/finance/bills**
```python
bills = api_client.get("/api/finance/bills", params={"status": "pending"})
```

**POST /api/finance/bills**
```python
bill_data = {
    "student_id": 123,
    "amount": 50000,
    "items": [...]
}
api_client.post("/api/finance/bills", bill_data)
```

## Data Flow

### Typical Request Flow

1. **User Action** (Frontend)
   - User clicks button or submits form
   - Streamlit captures event

2. **API Request** (Frontend)
   - `api_client` prepares request
   - Adds authentication headers
   - Sends HTTP request

3. **Backend Processing**
   - FastAPI receives request
   - Validates authentication
   - Processes business logic
   - Queries database

4. **Response** (Backend → Frontend)
   - Returns JSON response
   - Frontend handles response
   - Updates UI

5. **UI Update** (Frontend)
   - Display success/error message
   - Refresh data if needed
   - Update components

## Error Handling

### Backend Errors

```python
# Backend returns HTTP status codes
# 200: Success
# 400: Bad Request
# 401: Unauthorized
# 403: Forbidden
# 404: Not Found
# 500: Internal Server Error
```

### Frontend Error Handling

```python
# utils/api_client.py
try:
    response.raise_for_status()
    return response.json()
except requests.exceptions.HTTPError as e:
    if response.status_code == 401:
        # Session expired
        st.session_state.clear()
        st.error("Session expired. Please login again.")
    elif response.status_code == 403:
        st.error("Permission denied")
    else:
        st.error(f"API Error: {e}")
```

## State Management

### Session State Variables

```python
# Authentication
st.session_state.authenticated = True/False
st.session_state.access_token = "jwt_token"
st.session_state.user = {...}
st.session_state.user_role = "admin"/"teacher"/"student"

# Navigation
st.session_state.current_page = "dashboard"

# Temporary Data
st.session_state.selected_student = 123
st.session_state.edit_mode = True
```

## File Uploads

### Frontend

```python
# pages/students.py
uploaded_file = st.file_uploader("Upload Document")
if uploaded_file:
    files = {"file": uploaded_file}
    api_client.post("/api/students/upload", files=files)
```

### Backend Endpoint

```python
# src/routes/students.py
@router.post("/students/upload")
async def upload_document(file: UploadFile):
    # Process file
    return {"filename": file.filename}
```

## Real-time Updates

### Polling Approach

```python
# Dashboard auto-refresh every 30 seconds
import time

while True:
    data = api_client.get("/api/dashboard/metrics")
    st.rerun()
    time.sleep(30)
```

### WebSocket (Future Enhancement)

```python
# Real-time notifications
# To be implemented using Streamlit's experimental features
```

## Performance Optimization

### Caching

```python
# Frontend caching
@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_students():
    return api_client.get("/api/students")
```

### Pagination

```python
# Frontend
page = st.number_input("Page", min_value=1)
students = api_client.get("/api/students", params={
    "page": page,
    "limit": 20
})
```

### Lazy Loading

```python
# Load data only when needed
if st.button("Load More"):
    next_page = api_client.get(f"/api/students?page={page+1}")
```

## Security Considerations

### Token Security

- Tokens stored in session state (memory only)
- Automatically cleared on logout
- Not persisted to disk

### Input Validation

```python
# Frontend validation
if not email or "@" not in email:
    st.error("Invalid email")
    return

# Backend also validates (defense in depth)
```

### CSRF Protection

- FastAPI provides CSRF middleware
- Streamlit handles token automatically

## Development Workflow

### Running Both Services

1. **Terminal 1 - Backend**:
```bash
cd /path/to/EMIS
./start-dev.sh
```

2. **Terminal 2 - Frontend**:
```bash
cd /path/to/EMIS/frontend
./start-frontend.sh
```

### Testing API Integration

```python
# Test script
from utils.api_client import api_client

# Test connection
try:
    response = api_client.get("/health")
    print("✅ Backend connected")
except:
    print("❌ Backend not reachable")
```

## Deployment

### Production Setup

1. **Backend**: Deploy FastAPI with Gunicorn
2. **Frontend**: Deploy Streamlit with reverse proxy
3. **Both**: Use HTTPS
4. **CORS**: Configure properly

### Environment Variables

```bash
# Backend .env
DATABASE_URL=postgresql://...
SECRET_KEY=...

# Frontend .env
API_BASE_URL=https://api.yourschool.com
```

## Troubleshooting

### Common Issues

**Issue**: Connection refused
- **Solution**: Ensure backend is running on correct port

**Issue**: 401 Unauthorized
- **Solution**: Check token validity, re-login if needed

**Issue**: CORS errors
- **Solution**: Configure CORS in backend settings

**Issue**: Slow performance
- **Solution**: Implement caching, pagination

## API Documentation

For complete API documentation, see:
- Backend: http://localhost:8000/docs (Swagger UI)
- Backend: http://localhost:8000/redoc (ReDoc)

## Future Enhancements

- [ ] WebSocket for real-time updates
- [ ] GraphQL integration
- [ ] Offline mode support
- [ ] Progressive Web App (PWA)
- [ ] Mobile-responsive design improvements
