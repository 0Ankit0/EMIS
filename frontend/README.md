# EMIS Frontend - Streamlit Application

## Overview

This is the Streamlit-based frontend application for the EMIS (Education Management Information System). It provides a user-friendly web interface to interact with the backend API.

## Features

- 🔐 **Authentication**: Secure login and session management
- 👨‍🎓 **Student Management**: View, add, edit, and search students
- 📝 **Admissions**: Manage admission applications and processes
- 📚 **Academics**: Course management, timetables, exams, and results
- 💼 **HR & Payroll**: Employee management and payroll processing
- 📖 **Library**: Book catalog, circulation, and fine management
- 💰 **Finance**: Billing, accounting, and financial reports
- 📊 **Reports**: Analytics, dashboards, and custom reports
- ⚙️ **Settings**: User profile and system preferences

## Installation

### Prerequisites

- Python 3.11 or higher
- Backend API running (default: http://localhost:8000)

### Setup

1. Install dependencies:
```bash
cd frontend
pip install -r requirements.txt
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your API URL and settings
```

3. Run the application:
```bash
streamlit run app.py
```

The application will be available at http://localhost:8501

## Project Structure

```
frontend/
├── app.py                      # Main application entry point
├── config/
│   └── settings.py            # Configuration settings
├── pages/                     # Page modules
│   ├── __init__.py
│   ├── dashboard.py           # Main dashboard
│   ├── students.py            # Student management
│   ├── admissions.py          # Admissions management
│   ├── academics.py           # Academic management
│   ├── hr.py                  # HR & Payroll
│   ├── library.py             # Library management
│   ├── finance.py             # Finance management
│   ├── reports.py             # Reports & Analytics
│   └── settings.py            # User settings
├── components/                # Reusable UI components
│   └── ui_components.py
├── utils/                     # Utility functions
│   ├── api_client.py         # API communication
│   └── helpers.py            # Helper functions
├── assets/                    # Static assets
│   ├── images/
│   └── css/
├── .streamlit/
│   └── config.toml           # Streamlit configuration
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## Usage

### Login

Default credentials (development):
- Username: `admin`
- Password: `admin123`

### Navigation

Use the sidebar menu to navigate between different modules:
- **Dashboard**: Overview and key metrics
- **Students**: Student information and management
- **Admissions**: Application processing
- **Academics**: Course and exam management
- **HR & Payroll**: Employee management
- **Library**: Book catalog and circulation
- **Finance**: Billing and accounting
- **Reports**: Analytics and reports
- **Settings**: User preferences

### Features by Module

#### Dashboard
- Key performance indicators
- Enrollment statistics
- Attendance trends
- Financial overview
- Recent activities

#### Students
- View all students
- Add new students
- Search and filter
- Student analytics
- Edit/delete students

#### Library
- Book catalog
- Issue/return books
- Fine management
- Circulation reports

#### Finance
- Generate bills
- Track payments
- View financial reports
- Budget management

## API Integration

The frontend communicates with the backend API using the `APIClient` class:

```python
from utils.api_client import api_client

# GET request
data = api_client.get("/api/students")

# POST request
result = api_client.post("/api/students", {
    "first_name": "John",
    "last_name": "Doe"
})

# PUT request
api_client.put("/api/students/1", {"status": "active"})

# DELETE request
api_client.delete("/api/students/1")
```

## Configuration

### API Configuration

Edit `frontend/config/settings.py`:

```python
API_BASE_URL = "http://localhost:8000"
API_TIMEOUT = 30
```

### Theme Customization

Edit `frontend/.streamlit/config.toml`:

```toml
[theme]
primaryColor="#0066cc"
backgroundColor="#ffffff"
secondaryBackgroundColor="#f0f2f6"
```

## Development

### Adding New Pages

1. Create a new file in `pages/`:
```python
# pages/my_page.py
import streamlit as st

def show():
    st.title("My Page")
    # Your code here
```

2. Import in `pages/__init__.py`:
```python
from .my_page import show as show_my_page
```

3. Add to navigation in `app.py`

### Creating Components

Add reusable components in `components/ui_components.py`:

```python
def render_my_component(data):
    # Component implementation
    pass
```

## Troubleshooting

### Connection Error

If you see connection errors:
1. Ensure backend API is running
2. Check API_BASE_URL in settings
3. Verify firewall settings

### Authentication Issues

If login fails:
1. Check credentials
2. Verify backend authentication endpoint
3. Clear session state and retry

### Missing Data

If data doesn't load:
1. Check API endpoint availability
2. Verify user permissions
3. Check browser console for errors

## Performance Tips

- Enable caching for frequently accessed data
- Use pagination for large datasets
- Implement lazy loading for images
- Optimize database queries

## Security

- Never commit `.env` file
- Use HTTPS in production
- Implement CSRF protection
- Validate all user inputs
- Use secure session management

## Deployment

### Production Deployment

1. Set production environment:
```bash
export ENVIRONMENT=production
```

2. Update API URL:
```bash
export API_BASE_URL=https://api.yourschool.com
```

3. Run with production settings:
```bash
streamlit run app.py --server.port=80 --server.headless=true
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

Copyright © 2024 EMIS. All rights reserved.

## Support

For issues and questions:
- Email: support@emis.com
- Documentation: https://docs.emis.com
- Issues: https://github.com/yourorg/emis/issues
