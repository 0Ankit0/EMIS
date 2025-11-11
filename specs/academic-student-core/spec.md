# Academic & Student Core - Specification

## Overview

The Academic & Student Core is the heart of the EMIS system for college management. It encompasses all student-facing and academic operations from admission to graduation.

## Modules

### 1. Student Information System (SIS)
**Purpose**: Manages the core student record, including personal details, demographics, and contact information.

**Features**:
- Student profile management
- Demographics tracking
- Contact information management
- Emergency contacts
- Student ID generation
- Document uploads (photo, signature)

### 2. Admissions & Enrollment
**Purpose**: Manages the entire application lifecycle, from online applications and document verification to acceptance and registration.

**Features**:
- Online application portal
- Document upload and verification
- Application fee payment integration
- Merit list generation
- Admission offer letters
- Acceptance confirmation
- Enrollment process
- Document verification (DigiLocker integration)

### 3. Course & Curriculum Management
**Purpose**: Defines the college's course catalog, including course codes, descriptions, prerequisites, and credit hours.

**Features**:
- Course catalog management
- Curriculum design
- Program/degree management
- Department management
- Subject/course prerequisites
- Credit hour tracking
- Syllabus management
- Course outcomes mapping

### 4. Registration & Timetabling
**Purpose**: Allows students to register for courses, manage class schedules, and handle add/drop requests. Includes administrative tools for creating the master college timetable.

**Features**:
- Course registration
- Class schedule generation
- Room allocation
- Faculty assignment
- Add/drop course requests
- Conflict detection
- Substitution management
- Timetable optimization

### 5. Examination & Grading
**Purpose**: Manages all exam-related activities, from scheduling and hall ticket generation to grade entry, GPA calculation, and publishing transcripts.

**Features**:
- Exam scheduling
- Hall ticket generation
- Internal assessment tracking
- External exam management
- Grade entry and verification
- GPA/CGPA calculation
- Result sheet generation
- Transcript generation
- Marksheet printing

### 6. Attendance Management
**Purpose**: Tracks student attendance, generates reports, and flags students who fall below attendance threshold.

**Features**:
- Daily attendance marking
- Attendance tracking by subject
- Biometric integration support
- Attendance reports
- Low attendance alerts
- Leave management
- Attendance percentage calculation
- Eligibility verification for exams

## Database Models

- Student
- Enrollment
- Course
- CourseRegistration
- AcademicRecord
- Attendance
- Exam
- Marks
- ResultSheet
- ClassSchedule
- Timetable
- TimetableSlot
- Application
- AdmissionTest
- Interview

## API Endpoints

See `tasks.md` for detailed endpoint specifications.

## Integration Points

- **Financial Core**: Student fees, payment tracking
- **Administrative Core**: Faculty assignments, resource allocation
- **Library**: Student library membership
- **Hostel**: Student accommodation
