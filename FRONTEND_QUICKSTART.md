# EMIS Frontend + Backend Quick Start Guide

## 🚀 Quick Start (5 Minutes)

This guide will get both backend and frontend running in under 5 minutes.

### Prerequisites

- Python 3.11+
- PostgreSQL (or use Docker)
- 2 terminal windows

### Step 1: Clone and Setup (2 minutes)

```bash
# If not already cloned
git clone <repository-url>
cd EMIS

# Checkout frontend branch
git checkout frontend-streamlit
```

### Step 2: Start Backend (1 minute)

**Terminal 1:**
```bash
# Quick setup and start
./setup.sh
./start-dev.sh
```

This will:
- Create virtual environment
- Install dependencies
- Start PostgreSQL (via Docker)
- Run database migrations
- Start FastAPI server on http://localhost:8000

### Step 3: Start Frontend (1 minute)

**Terminal 2:**
```bash
# Navigate to frontend
cd frontend

# Quick start
./start-frontend.sh
```

This will:
- Install Streamlit dependencies
- Start frontend on http://localhost:8501

### Step 4: Access Application (30 seconds)

Open your browser:
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000/docs

**Default Login:**
- Username: `admin`
- Password: `admin123`

---

## 🎯 What You Can Do

Once logged in, you can:

### ✅ Dashboard
- View key metrics
- See enrollment statistics
- Check financial overview
- Monitor recent activities

### ✅ Student Management
- Add new students
- View student list
- Search students
- Edit/delete records

### ✅ Library
- Browse book catalog
- Issue/return books
- Manage fines
- View circulation reports

### ✅ Finance
- Generate bills
- Track payments
- View financial reports

### ✅ Reports
- Generate custom reports
- View analytics
- Export data

---

## 🔧 Configuration

### Backend Configuration

Edit `.env`:
```bash
DATABASE_URL=postgresql://emis:emis@localhost:5432/emis
SECRET_KEY=your-secret-key
```

### Frontend Configuration

Edit `frontend/.env`:
```bash
API_BASE_URL=http://localhost:8000
API_TIMEOUT=30
```

---

## 🧪 Testing Integration

Run the integration test:

```bash
./test-integration.sh
```

This checks:
- Backend availability
- API endpoints
- Frontend dependencies
- Configuration files

---

## 📚 Common Tasks

### Add a New Student

1. Go to **Students** page
2. Click **Add Student** tab
3. Fill in details
4. Click **Add Student** button

### Issue a Library Book

1. Go to **Library** page
2. Click **Circulation** tab
3. Select book and member
4. Click **Issue Book**

### Generate Financial Report

1. Go to **Reports** page
2. Select report type
3. Choose date range
4. Click **Generate**

---

## 🐛 Troubleshooting

### Backend Not Starting

```bash
# Check if PostgreSQL is running
docker ps

# Restart backend
./start-dev.sh
```

### Frontend Connection Error

```bash
# Verify backend is running
curl http://localhost:8000/health

# Check frontend config
cat frontend/.env
```

### Database Issues

```bash
# Reset database
docker-compose down -v
docker-compose up -d postgres

# Run migrations
alembic upgrade head
```

### Port Already in Use

```bash
# Backend (8000)
lsof -ti:8000 | xargs kill -9

# Frontend (8501)
lsof -ti:8501 | xargs kill -9
```

---

## 📖 More Information

- **Full Documentation**: See `README.md`
- **API Documentation**: http://localhost:8000/docs
- **Frontend Guide**: See `frontend/README.md`
- **Integration Guide**: See `frontend/INTEGRATION.md`

---

## 🎓 Sample Data

### Creating Test Users

```bash
# Backend terminal
python -m src.cli.user_commands create-user \
  --username teacher1 \
  --password teacher123 \
  --role teacher
```

### Adding Sample Students

Use the frontend "Add Student" form or API:

```bash
curl -X POST http://localhost:8000/api/students \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "program": "B.Tech"
  }'
```

---

## 🔐 Security Notes

**Development:**
- Default credentials are for development only
- HTTPS not required locally
- CORS is permissive

**Production:**
- Change all default passwords
- Use HTTPS
- Configure proper CORS
- Use environment variables for secrets
- Enable authentication middleware

---

## 🚀 Production Deployment

### Backend

```bash
# Build Docker image
docker build -t emis-backend .

# Run with production settings
docker run -p 8000:8000 --env-file .env.production emis-backend
```

### Frontend

```bash
# Install production dependencies
pip install -r frontend/requirements.txt

# Run with production config
streamlit run frontend/app.py --server.port=80 --server.headless=true
```

---

## 💡 Tips

1. **Use Multiple Tabs**: Open different modules in browser tabs
2. **Keyboard Shortcuts**: Streamlit supports `Ctrl+R` to refresh
3. **Data Export**: Most tables have download CSV option
4. **Search**: Use search boxes for quick filtering
5. **Real-time Updates**: Dashboard auto-refreshes

---

## 🤝 Getting Help

- Check logs in terminal windows
- View API docs at http://localhost:8000/docs
- Check browser console for frontend errors
- Run integration tests: `./test-integration.sh`

---

## ✨ Features Overview

| Module | Features |
|--------|----------|
| Dashboard | KPIs, Charts, Recent Activities |
| Students | CRUD, Search, Analytics |
| Admissions | Applications, Approvals, Merit Lists |
| Academics | Courses, Exams, Timetables, Results |
| HR | Employees, Payroll, Leave, Performance |
| Library | Books, Circulation, Fines, Reports |
| Finance | Billing, Payments, Accounting, Reports |
| Reports | Custom Reports, Analytics, Export |

---

## 🎉 You're Ready!

Both backend and frontend should now be running. Start exploring the EMIS system!

Happy coding! 🚀
