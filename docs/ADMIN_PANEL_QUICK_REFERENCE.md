# EMIS Admin Panel - Quick Reference

## 🚀 Access the System

### Login
- URL: `http://127.0.0.1:8000/auth/login/`
- **Admin**: username: `admin` | password: `admin123`

### Available Modules

| Module | URL | Description |
|--------|-----|-------------|
| Students | `/students/` | Manage student records, documents, profiles |
| Courses | `/courses/` | Manage academic courses and syllabi |
| Admissions | `/admissions/` | Process applications and admissions |
| Finance | `/finance/` | Manage fees, invoices, payments |
| Faculty | `/faculty/` | Manage faculty members and assignments |
| Exams | `/exams/` | Manage exams and grade entry |
| Library | `/library/` | Manage books and library resources |

## 📋 Features by Module

### **Students Module** `/students/`
- ✅ List all students with filters
- ✅ View student details
- ✅ Create new student
- ✅ Edit student information
- ✅ Delete student
- ✅ Upload profile photo
- ✅ Upload/manage documents
- ✅ Export student data
- ✅ Import bulk students
- ✅ Search & filter
- ✅ Activity log

### **Courses Module** `/courses/`
- ✅ List all courses
- ✅ Create new course
- ✅ Edit course details
- ✅ Delete course
- ✅ Filter by department
- ✅ Search courses

### **Finance Module** `/finance/`
- ✅ Finance dashboard
- ✅ Manage invoices
- ✅ Fee structures
- ✅ Student fee portal

### **Admissions Module** `/admissions/`
- ✅ Application dashboard
- ✅ Review applications
- ✅ Application details

### **Faculty Module** `/faculty/`
- ✅ Faculty list
- ✅ Faculty profiles
- ✅ Faculty dashboard

### **Exams Module** `/exams/`
- ✅ Exam management
- ✅ Grade entry (faculty)
- ✅ Student grades view

### **Library Module** `/library/`
- ✅ Library dashboard
- ✅ Book management
- ✅ Book issuing

## 🎨 UI Components

### Stats Cards
Display key metrics with color coding:
- **Blue**: General stats
- **Green**: Success/Active items
- **Orange**: Pending/Warnings
- **Red**: Critical/Inactive
- **Cyan**: Information

### Tables
- Powered by DataTables
- Search functionality
- Sorting on all columns
- Pagination (25 per page)
- Responsive design

### Forms
- Clean, validated inputs
- File upload with drag & drop
- Date pickers
- Select2 dropdowns
- Inline validation

### File Management
- Upload multiple files
- Drag & drop support
- File preview
- Download/delete options
- Type & size validation

## 🔐 Access Control

### Admin/Staff
Full access to all modules:
- Create, Read, Update, Delete
- View all records
- Export data
- Import data
- Manage system

### Students  
Limited access:
- View own profile
- View own courses
- View own grades
- View own fees
- View own attendance

### Faculty
Teaching-related access:
- View assigned classes
- Enter grades
- Mark attendance
- Upload course materials

## 💡 Tips & Tricks

### Quick Actions
- **View Details**: Click eye icon
- **Edit**: Click edit icon
- **Delete**: Click trash icon (confirmation required)
- **Search**: Use search box in filters
- **Export**: Click CSV or PDF buttons
- **Import**: Click Import button, select file

### Keyboard Shortcuts
- **Ctrl/Cmd + S**: Save form (if supported)
- **Esc**: Close modal
- **Tab**: Navigate form fields

### File Uploads
1. Click upload area OR drag files
2. Select file(s)
3. Preview appears
4. Click Upload button
5. File is saved

### Filters
1. Select filter criteria
2. Click "Filter" button
3. Click "Clear" to reset
4. Results update instantly

## 📱 Responsive Design

### Desktop (> 1024px)
- Full sidebar visible
- 4-column stats
- Full width tables

### Tablet (768px - 1024px)
- Full sidebar visible
- 2-column stats
- Scrollable tables

### Mobile (< 768px)
- Collapsible sidebar
- Single column stats
- Mobile-optimized tables
- Touch-friendly buttons

## 🐛 Troubleshooting

### Can't Login
- Check username/password
- Verify account is active
- Clear browser cache
- Try different browser

### Page Not Loading
- Check URL is correct
- Verify you have permission
- Check if logged in
- Contact administrator

### File Upload Fails
- Check file size (< 5MB documents, < 2MB photos)
- Verify file type is allowed
- Check internet connection
- Try again

### Table Not Loading
- Refresh page
- Clear filters
- Check browser console for errors
- Contact support

## 📊 Data Export

### Export Students
1. Go to Students list
2. Apply filters (optional)
3. Click "Export CSV" or "Export PDF"
4. Download starts automatically

### Export Format
- **CSV**: Spreadsheet format (Excel compatible)
- **PDF**: Printable document format

## 📥 Data Import

### Import Students
1. Click "Import" button
2. Download template (first time)
3. Fill template with data
4. Select filled file
5. Click "Import"
6. Review results
7. Fix errors if any

### Template Format
- First row: Headers
- Required fields marked with *
- Date format: YYYY-MM-DD
- No special characters in names

## 🔔 Notifications

### Bell Icon
- Shows unread count
- Click to view all
- Mark as read
- Clear notifications

### Types
- **System**: Important updates
- **Application**: New applications
- **Payment**: Fee payments
- **Grade**: Grade updates

## ⚙️ Settings

### Profile Settings
- Update personal information
- Change password
- Enable 2FA
- Update photo

### System Settings (Admin Only)
- Configure modules
- Manage permissions
- Set academic year
- Configure fees

## 📞 Support

### Get Help
- **Documentation**: `/docs/`
- **API Docs**: `/api/docs/`
- **Admin Panel**: `/admin/`
- **Email**: support@emis.edu

### Report Issues
1. Note error message
2. Note steps to reproduce
3. Take screenshot
4. Contact support

## 🎯 Best Practices

### Data Entry
- Fill all required fields
- Use consistent formats
- Verify before saving
- Review after saving

### File Management
- Use descriptive names
- Organize by category
- Delete old files
- Keep backups

### Security
- Logout when done
- Don't share password
- Report suspicious activity
- Use strong passwords

### Performance
- Close unused tabs
- Clear cache regularly
- Use latest browser
- Good internet connection

## 🚀 Next Steps

1. **Explore**: Browse all modules
2. **Create**: Add test data
3. **Test**: Try all features
4. **Learn**: Read documentation
5. **Customize**: Configure settings

## 📚 Additional Resources

- [Full Implementation Guide](ADMIN_PANEL_IMPLEMENTATION.md)
- [Role-Based Access Control](RBAC_IMPLEMENTATION.md)
- [Authentication Guide](AUTHENTICATION_GUIDE.md)
- [API Documentation](/api/docs/)

---

**Version**: 1.0.0  
**Last Updated**: November 17, 2025  
**Status**: Production Ready
