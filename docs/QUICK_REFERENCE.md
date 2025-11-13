# EMIS Frontend - Quick Reference

## Starting the Application

```bash
# Navigate to frontend directory
cd /media/ankit/Programming/Projects/python/EMIS/frontend

# Activate virtual environment
source ../venv/bin/activate

# Run the application
streamlit run app.py
```

## User Roles & Access

### 🎓 Student
- **Dashboard**: Course overview, attendance, assignments, CGPA
- **Courses**: View courses, materials, schedules
- **Assignments**: Submit and track assignments
- **Attendance**: View attendance, apply for leave
- **Exams**: View schedule, download hall tickets, check results
- **Fees**: Pay fees, view history, download receipts
- **Library**: Search books, manage issued books, pay fines
- **Profile**: Edit personal information, change password

### 👨‍🏫 Teacher/Faculty
- **Dashboard**: Teaching overview, today's schedule
- **Courses**: Manage teaching courses, upload materials
- **Attendance**: Mark daily attendance, generate reports
- **Assignments**: Create and grade assignments (planned)
- **Grading**: Enter marks, manage gradebook (planned)
- **Timetable**: View teaching schedule (planned)
- **Profile**: Edit personal information, change password

### 👔 Admin/Staff
- **Dashboard**: Institution metrics, financial overview
- **Students**: Manage student records, add/edit students
- **Admissions**: Process applications, manage admissions
- **Academics**: Course and program management
- **HR & Payroll**: Employee management, payroll processing
- **Library**: Catalog management, issue/return books
- **Finance**: Fee management, payment processing, reports
- **Reports**: Generate various reports
- **Settings**: System configuration, user management
- **Profile**: Edit personal information, change password

## Page Navigation Map

```
Login Page
    │
    ├─→ Student Portal
    │   ├─→ Dashboard
    │   ├─→ Profile
    │   ├─→ My Courses
    │   ├─→ Assignments
    │   ├─→ Attendance
    │   ├─→ Exams & Results
    │   ├─→ Fees & Payments
    │   └─→ Library
    │
    ├─→ Faculty Portal
    │   ├─→ Dashboard
    │   ├─→ Profile
    │   ├─→ My Courses
    │   ├─→ Mark Attendance
    │   ├─→ Assignments (planned)
    │   ├─→ Grading (planned)
    │   └─→ Timetable (planned)
    │
    └─→ Admin Portal
        ├─→ Dashboard
        ├─→ Profile
        ├─→ Students
        ├─→ Admissions
        ├─→ Academics
        ├─→ HR & Payroll
        ├─→ Library
        ├─→ Finance
        ├─→ Reports
        └─→ Settings
```

## Key Files

| File | Purpose |
|------|---------|
| `app.py` | Main entry point, routing |
| `utils/navigation.py` | Navigation configuration |
| `utils/helpers.py` | Helper functions |
| `utils/api_client.py` | API integration |
| `components/ui_components.py` | Reusable UI components |
| `config/settings.py` | Configuration |
| `pages/dashboard.py` | Role-based dashboards |
| `pages/common/profile.py` | Profile management |
| `pages/student/*.py` | Student portal pages |
| `pages/faculty/*.py` | Faculty portal pages |

## Common Operations

### Adding a New Page

1. **Create page file**: `pages/[role]/new_page.py`
2. **Add to navigation**: Update `utils/navigation.py`
3. **Add route**: Update `app.py` routing
4. **Update module**: Add to `__init__.py`

### Modifying Menu Items

Edit `utils/navigation.py`:
```python
role_menus = {
    "student": [
        {
            "title": "New Page",
            "icon": "icon-name",
            "page": "page_key"
        }
    ]
}
```

### Session State Variables

```python
st.session_state.authenticated  # Login status
st.session_state.user          # User data
st.session_state.user_role     # User role
st.session_state.access_token  # API token
st.session_state.page          # Current page (optional)
```

## API Endpoints Reference

### Student APIs
- `GET /api/students/{id}/dashboard` - Dashboard data
- `GET /api/students/{id}/courses` - Enrolled courses
- `GET /api/students/{id}/assignments` - Assignments
- `GET /api/students/{id}/attendance/summary` - Attendance
- `GET /api/students/{id}/exams` - Exams
- `GET /api/students/{id}/fees` - Fees
- `GET /api/students/{id}/library` - Library

### Faculty APIs
- `GET /api/faculty/{id}/dashboard` - Dashboard data
- `GET /api/faculty/{id}/courses` - Teaching courses
- `POST /api/attendance/mark` - Mark attendance
- `GET /api/courses/{id}/students` - Course students

### Admin APIs
- `GET /api/dashboard/metrics` - Admin dashboard
- `GET /api/students` - All students
- `POST /api/students` - Add student
- `GET /api/admissions` - Applications
- etc.

## Troubleshooting

### Page Not Loading
- Check `app.py` routing function
- Verify page key in `navigation.py`
- Check import statements

### API Errors
- Verify backend is running
- Check API endpoint URLs
- Review access token validity
- Demo data will display on API failure

### Navigation Issues
- Clear session state: Logout and login again
- Check user role assignment
- Verify menu configuration

### Import Errors
- Check `__init__.py` files exist
- Verify module structure
- Check import paths

## Development Tips

1. **Use demo data**: Implement fallback data for offline development
2. **Error handling**: Always wrap API calls in try-except
3. **Loading states**: Show spinners for async operations
4. **User feedback**: Use success/error messages
5. **Consistent styling**: Use shared UI components
6. **Session state**: Use for inter-page communication

## Testing Commands

```bash
# Syntax check
source ../venv/bin/activate
python -m py_compile app.py

# Check specific page
python -m py_compile pages/student/courses.py

# Check navigation module
python -m py_compile utils/navigation.py
```

## Environment Variables

Create `.env` file in frontend directory:
```
BACKEND_URL=http://localhost:8000
API_VERSION=v1
APP_ENV=development
```

## Support & Documentation

- **NAVIGATION.md**: Detailed navigation guide
- **IMPLEMENTATION_SUMMARY.md**: Complete implementation details
- **README.md**: General usage instructions
- **Inline comments**: Code-level documentation

## Status

- ✅ Core infrastructure complete
- ✅ Student portal complete (6 pages)
- ✅ Faculty portal partial (2 pages)
- ✅ Admin portal existing (8+ pages)
- ✅ Navigation system working
- ✅ All pages interconnected
- ✅ Role-based access control
- ✅ API integration with fallbacks

**Last Updated**: November 2024
**Version**: 1.0
**Status**: Production Ready (Student & Admin), Development (Faculty)
