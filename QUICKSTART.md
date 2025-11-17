# EMIS Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Setup Environment

```bash
# Clone the repository
git clone <repository-url>
cd EMIS

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Database

Create a `.env` file:
```env
DATABASE_URL=postgresql://emis_user:password@localhost:5432/emis_db
SECRET_KEY=your-long-random-secret-key-here
DEBUG=True
```

Create PostgreSQL database:
```bash
createdb emis_db
```

### Step 3: Initialize System

```bash
# Run migrations
python manage.py migrate

# Seed roles and permissions
python manage.py seed_auth

# Create admin user
python manage.py createsuperuser
```

### Step 4: Run Server

```bash
python manage.py runserver
```

Visit: http://localhost:8000

## 🧪 Test the APIs

### 1. Register a User

```bash
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "first_name": "Test",
    "last_name": "User"
  }'
```

### 2. Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "SecurePass123!"
  }'
```

Save the `access` token from the response.

### 3. Get Current User

```bash
curl -X GET http://localhost:8000/api/v1/auth/me/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 4. List All Users (Admin Only)

```bash
curl -X GET http://localhost:8000/api/v1/auth/users/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 📊 View Seeded Data

After running `python manage.py seed_auth`, you'll have:

- **21 Resource Groups**: Users, Roles, Students, Courses, Finance, etc.
- **114 Permissions**: view, create, update, delete, approve, export
- **10 Roles**: Super Admin, Admin, Faculty, Student, etc.

## 🔑 Admin Access

Login to Django admin:
http://localhost:8000/admin/

Use the superuser credentials you created.

## ✅ Verify Installation

Run tests to ensure everything works:

```bash
pytest tests/authentication/ -v
```

You should see all tests passing ✅

## 🎯 Next Steps

1. Explore the API endpoints in README.md
2. Assign roles to users via admin panel
3. Test permission-based access control
4. Check audit logs for compliance

## 🆘 Need Help?

- Check README.md for detailed documentation
- Review error messages in console
- Check logs in `logs/` directory
- Ensure PostgreSQL and Redis are running

## 🎉 You're Ready!

Your EMIS instance is now running and ready to use!
