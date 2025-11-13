# EMIS Frontend - Navigation Guide

## Overview
The EMIS frontend is a role-based Streamlit application that provides different interfaces for Students, Faculty, Staff, and Administrators.

## Role-Based Navigation

### Student Portal
Students have access to the following features:

1. **Dashboard** 📊
   - Overview of enrolled courses
   - Attendance percentage
   - Pending assignments
   - CGPA and academic performance

2. **Profile** 👤
   - View and edit personal information
   - Update emergency contacts
   - Change password

3. **My Courses** 📚
   - View enrolled courses
   - Access course materials
   - Check attendance per course
   - Course schedules and instructors

4. **Assignments** 📝
   - View pending assignments
   - Submit assignments
   - Check submitted assignments
   - View graded assignments with feedback

5. **Attendance** 📅
   - Overall attendance summary
   - Course-wise attendance
   - Attendance trends
   - Apply for leave

6. **Exams & Results** 🏆
   - Upcoming exam schedule
   - View results
   - Download hall tickets
   - Download transcripts

7. **Fees & Payments** 💰
   - View fee structure
   - Make online payments
   - Payment history
   - Download receipts

8. **Library** 📖
   - Search books
   - View issued books
   - Reserve books
   - Pay fines

### Faculty Portal
Faculty members have access to:

1. **Dashboard** 📊
   - Courses teaching
   - Total students
   - Pending grading tasks
   - Today's class schedule

2. **Profile** 👤
   - Personal information
   - Qualifications
   - Change password

3. **My Courses** 📚
   - View assigned courses
   - Student lists
   - Upload course materials
   - Course analytics

4. **Mark Attendance** 📅
   - Mark daily attendance
   - Bulk attendance marking
   - Attendance reports
   - Analytics (low attendance students)

5. **Assignments** 📝
   - Create assignments
   - View submissions
   - Grade assignments
   - Provide feedback

6. **Grading** 🏆
   - Enter exam marks
   - Bulk marks upload
   - Gradebook management
   - Student performance analytics

7. **Timetable** 📆
   - View teaching schedule
   - Room assignments
   - Class timings

### Admin/Staff Portal
Administrators and staff have access to:

1. **Dashboard** 📊
   - Key metrics (students, faculty, courses)
   - Enrollment statistics
   - Financial overview
   - Recent activities
   - Pending tasks

2. **Students** 👨‍🎓
   - Student list
   - Add new students
   - Edit student records
   - Search and filter
   - Student analytics

3. **Admissions** 📋
   - Application management
   - Document verification
   - Merit list generation
   - Admission approvals

4. **Academics** 📚
   - Course management
   - Program management
   - Curriculum planning
   - Academic calendar

5. **HR & Payroll** 💼
   - Employee management
   - Leave approvals
   - Payroll processing
   - Performance tracking

6. **Library** 📖
   - Book catalog management
   - Issue/return books
   - Fine management
   - Library reports

7. **Finance** 💰
   - Fee management
   - Payment processing
   - Expense tracking
   - Financial reports

8. **Reports** 📊
   - Academic reports
   - Financial reports
   - Attendance reports
   - Custom report generation

9. **Settings** ⚙️
   - System configuration
   - User management
   - Role management
   - General settings

## Page Structure

```
frontend/
├── app.py                          # Main application entry
├── pages/
│   ├── common/
│   │   └── profile.py             # Common profile page
│   ├── student/
│   │   ├── courses.py             # Student courses
│   │   ├── assignments.py         # Student assignments
│   │   ├── attendance.py          # Student attendance
│   │   ├── exams.py               # Exams and results
│   │   ├── fees.py                # Fees and payments
│   │   └── library.py             # Library access
│   ├── faculty/
│   │   ├── courses.py             # Faculty courses
│   │   └── attendance.py          # Attendance marking
│   ├── dashboard.py               # Role-based dashboard
│   ├── students.py                # Student management (admin)
│   ├── admissions.py              # Admissions (admin)
│   ├── academics.py               # Academics (admin)
│   ├── hr.py                      # HR & Payroll (admin)
│   ├── library.py                 # Library management (admin)
│   ├── finance.py                 # Finance (admin)
│   ├── reports.py                 # Reports (admin)
│   └── settings.py                # Settings (admin)
├── utils/
│   ├── navigation.py              # Navigation utilities
│   ├── helpers.py                 # Helper functions
│   └── api_client.py              # API client
├── components/
│   └── ui_components.py           # Reusable UI components
└── config/
    └── settings.py                # Configuration
```

## Navigation Flow

1. **Login** → User authenticates with credentials
2. **Role Detection** → System identifies user role
3. **Menu Generation** → Navigation menu generated based on role
4. **Page Routing** → Selected menu item routes to appropriate page
5. **Page Display** → Page content displayed with role-specific features

## Inter-Page Links

Pages are linked through:
- **Session state**: `st.session_state.page` for navigation
- **Button clicks**: Quick access buttons on dashboard
- **Menu selection**: Sidebar menu navigation
- **Breadcrumbs**: Contextual navigation (future enhancement)

## Adding New Pages

To add a new page:

1. Create the page file in appropriate directory:
   - `pages/student/` for student pages
   - `pages/faculty/` for faculty pages
   - `pages/common/` for shared pages
   - `pages/` for admin pages

2. Update `utils/navigation.py`:
   - Add menu item to appropriate role
   - Add page title mapping

3. Update `app.py`:
   - Add route in `route_to_page()` function

4. Update module `__init__.py`:
   - Import new page module

## Testing Navigation

Test with different roles:

```python
# Student
st.session_state.user_role = "student"
st.session_state.authenticated = True

# Teacher
st.session_state.user_role = "teacher"
st.session_state.authenticated = True

# Admin
st.session_state.user_role = "admin"
st.session_state.authenticated = True
```

## Common Issues

1. **Page not found**: Check route in `app.py`
2. **Menu not showing**: Check `navigation.py` menu items
3. **Import errors**: Verify `__init__.py` files
4. **Session state cleared**: Re-authenticate after logout

## Best Practices

1. **Consistent naming**: Use descriptive page keys
2. **Error handling**: Graceful fallbacks for API errors
3. **Demo data**: Provide demo data when API fails
4. **Loading states**: Show spinners for async operations
5. **User feedback**: Success/error messages for actions
6. **Navigation state**: Maintain state across pages

## Future Enhancements

- [ ] Breadcrumb navigation
- [ ] Deep linking with URL parameters
- [ ] Back button functionality
- [ ] Page history tracking
- [ ] Favorite pages/bookmarks
- [ ] Search across all pages
- [ ] Keyboard shortcuts
- [ ] Mobile-responsive navigation
