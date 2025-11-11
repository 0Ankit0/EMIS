# Administrative & Operational Core - Specification

## Overview

The Administrative & Operational Core manages all faculty, staff, and operational aspects of the college including HR, library, hostel, and resource management.

## Modules

### 1. Faculty & Staff Management (HR)
**Purpose**: Manages all faculty and staff profiles, including qualifications, subjects taught, payroll information, and leave management.

**Features**:
- Employee profile management
- Qualification tracking
- Subject assignment for faculty
- Workload management
- Attendance tracking
- Leave management
- Performance reviews
- Recruitment and onboarding
- Payroll processing
- Teacher hierarchy management

### 2. Library Management
**Purpose**: Integrates with the college library to manage book catalogs, circulation (check-in/check-out), and late fees.

**Features**:
- Book catalog management
- ISBN and barcode support
- Book circulation (issue/return)
- Student and faculty borrowing
- Reservation system
- Fine calculation and collection
- Lost book management
- Digital resource management
- Library membership management
- Overdue notifications

### 3. Hostel / Dormitory Management
**Purpose**: Manages room allocation, inventory, and hostel fees for on-campus student housing.

**Features**:
- Hostel profile management
- Room allocation
- Bed management
- Student check-in/check-out
- Mess menu management
- Visitor tracking
- Complaint management
- Hostel fee integration
- Room maintenance tracking
- Hostel attendance

### 4. Resource Management
**Purpose**: Tracks the college's physical assets, such as classrooms, labs, and equipment, to help with scheduling and maintenance.

**Features**:
- Classroom management
- Laboratory management
- Equipment tracking
- Asset inventory
- Maintenance scheduling
- Resource booking
- Utilization reports
- Vendor management
- Purchase orders
- Stock tracking

## Additional Modules

### 5. Transport Management
**Purpose**: Manages college transportation including buses, routes, and student transport allocation.

**Features**:
- Vehicle management
- Route planning
- Stop management
- Student transport allocation
- Driver and conductor management
- Maintenance tracking
- Fuel tracking
- Transport fee integration

### 6. Event Management
**Purpose**: Manages college events, conferences, workshops, and cultural activities.

**Features**:
- Event creation and scheduling
- Registration management
- Budget tracking
- Attendance tracking
- Certificate generation
- Event fee collection
- Resource allocation for events

### 7. Placement Management
**Purpose**: Manages campus placements, company visits, and student placement tracking.

**Features**:
- Company registration
- Job posting management
- Student applications
- Interview scheduling
- Offer management
- Placement statistics
- Alumni employment tracking

## Database Models

- Employee
- TeacherHierarchy
- Payroll
- Leave
- PerformanceReview
- Book
- LibraryMember
- Issue
- Reservation
- Fine
- BookLoss
- Hostel
- Room
- RoomAllocation
- MessMenu
- HostelVisitor
- HostelComplaint
- Vehicle
- Route
- RouteStop
- StudentTransport
- VehicleMaintenance
- Event
- EventRegistration
- EventBudget
- Company
- JobPosting
- PlacementApplication
- PlacementOffer
- InventoryItem
- PurchaseOrder
- Vendor

## API Endpoints

See `tasks.md` for detailed endpoint specifications.

## Integration Points

- **Academic Core**: Faculty assignments, student enrollments
- **Financial Core**: HR payroll, library fines, hostel fees, transport fees
- **Communication**: Event notifications, placement updates
