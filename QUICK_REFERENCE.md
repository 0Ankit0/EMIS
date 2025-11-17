# EMIS CORE PLATFORM - QUICK REFERENCE

## 🚀 Quick Start

```bash
# 1. Clone and setup
cd /media/ankit/Programming/Projects/python/EMIS
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env with your settings

# 3. Start database
docker-compose up -d

# 4. Run migrations
python manage.py migrate

# 5. Seed data
python manage.py seed_auth

# 6. Create superuser
python manage.py createsuperuser

# 7. Run server
python manage.py runserver
```

## 📡 API Endpoints

### Authentication
```http
POST /api/v1/auth/register/
POST /api/v1/auth/login/
POST /api/v1/auth/logout/
POST /api/v1/auth/refresh/
GET  /api/v1/auth/me/
```

### User Management
```http
GET    /api/v1/auth/users/
GET    /api/v1/auth/users/{id}/
PUT    /api/v1/auth/users/{id}/update/
DELETE /api/v1/auth/users/{id}/delete/
POST   /api/v1/auth/users/{id}/roles/
```

### Admissions
```http
POST  /api/v1/admissions/applications/
GET   /api/v1/admissions/applications/
PATCH /api/v1/admissions/applications/{id}/status/
POST  /api/v1/admissions/merit-lists/
GET   /api/v1/admissions/merit-lists/
```

### Enrollments
```http
POST  /api/v1/students/enrollments/
GET   /api/v1/students/enrollments/
POST  /api/v1/students/enrollments/from-application/
POST  /api/v1/students/enrollments/bulk-enroll/
```

## 🔑 Default Roles

| Role | Permissions | Use Case |
|------|-------------|----------|
| Super Admin | 114 | Full system access |
| Admin | 107 | Administrative tasks |
| Management | 42 | Strategic oversight |
| Faculty | 19 | Teaching & grading |
| Admissions Officer | 18 | Application processing |
| Finance Officer | 18 | Fee management |
| Librarian | 12 | Library operations |
| Staff | 7 | General staff tasks |

## 🧪 Running Tests

```bash
# All tests
pytest

# Specific module
pytest tests/authentication/
pytest tests/admissions/

# With coverage
pytest --cov=apps --cov-report=html
```

## 📊 Key Features

### Authentication & Security
- JWT-based authentication
- bcrypt password hashing
- Token refresh mechanism
- RBAC enforcement
- Audit logging

### Admissions Workflow
- Application submission
- 9-state workflow
- Merit list generation
- Automatic ranking
- Student enrollment

### Permission System
- 21 resource groups
- 114 granular permissions
- Role-based access
- Dynamic assignment

## 🔧 Management Commands

```bash
# Seed authentication data
python manage.py seed_auth

# Create superuser
python manage.py createsuperuser

# Run migrations
python manage.py migrate

# Create migrations
python manage.py makemigrations
```

## 📈 Status

- MVP: 97% Complete ⭐
- Phase 4: 64% Complete ✅
- Production Ready: YES ✅
- Test Coverage: Good ✅

## 📚 Documentation

- README.md - Full guide
- QUICKSTART.md - Quick setup
- API_TESTING.md - API docs
- FINAL_IMPLEMENTATION_STATUS.md - Detailed status

## ⚙️ Configuration

### Environment Variables
```bash
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost:5432/emis
REDIS_URL=redis://localhost:6379/0
JWT_SECRET_KEY=your-jwt-secret
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
```

### Database
- PostgreSQL 15+
- Redis for caching
- Celery for background jobs

## 🎯 Next Steps

1. Deploy to production
2. Implement Phase 5 (Courses)
3. Add Phase 6 (Finance)
4. Build Phase 7 (Analytics)
5. Polish & optimize

---

**For detailed information, see FINAL_IMPLEMENTATION_STATUS.md**

