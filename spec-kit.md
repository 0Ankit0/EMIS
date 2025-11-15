# SpecKit Documentation - EMIS Project

This document contains the complete specification workflow for the Enterprise Management Information System (EMIS) project. Each section corresponds to a `/speckit.*` command that guides the feature specification, planning, and implementation process.

---

## Table of Contents

1. [Constitution](#constitution) - `/speckit.constitution`
2. [Specify](#specify) - `/speckit.specify`
3. [Clarify](#clarify) - `/speckit.clarify`
4. [Plan](#plan) - `/speckit.plan`
5. [Analyze](#analyze) - `/speckit.analyze`
6. [Checklist](#checklist) - `/speckit.checklist`
7. [Tasks](#tasks) - `/speckit.tasks`
8. [Implement](#implement) - `/speckit.implement`

---

## Constitution

**Command**: `/speckit.constitution`

**Purpose**: Establish this project's governing principles to ensure consistent decision-making throughout all phases.

### Project Principles

The EMIS project is governed by the following core principles:

#### 1. Security
- **Encryption**: All data must be encrypted in transit (HTTPS/TLS) and at rest (database, file storage)
- **Audit Logging**: All sensitive actions must be logged with user, timestamp, and action details
- **GDPR Compliance**: Data privacy, consent management, right to deletion, data portability
- **Indian IT Act Compliance**: Local regulatory requirements for educational institutions

#### 2. Modularity
- **Library-First**: Core business logic in domain layer, reusable across interfaces
- **CLI Interface**: Admin operations accessible via command-line for automation
- **Separation of Concerns**: Clear boundaries between API, domain, and infrastructure layers
- **Domain Module Independence**: Each module (auth, students, HR, library, etc.) is independently testable

#### 3. Test-First Development
- **TDD (Test-Driven Development)**: Write tests before implementation
- **Contract-First**: API contracts defined and validated before implementation
- **Integration-First**: Test user journeys and cross-module interactions early

#### 4. Simplicity
- **≤3 Projects**: Avoid unnecessary project proliferation (monorepo preferred)
- **No Future-Proofing**: Implement only what's needed now, refactor when needed
- **YAGNI (You Aren't Gonna Need It)**: Resist speculative features

#### 5. Observability
- **Health Checks**: All services expose health/readiness endpoints
- **Structured Logging**: Consistent, searchable log format across all modules
- **Metrics**: Track performance, usage, and errors

#### 6. Maintainability
- **Documentation**: Auto-generated API docs, ADRs, user guides
- **CI/CD**: Automated testing, linting, building, and deployment
- **Code Quality**: Enforced via linting (flake8, black, isort) and type checking (mypy)

#### 7. Compliance
- **Data Privacy**: GDPR, Indian IT Act, institutional policies
- **Code Quality**: Minimum coverage, linting, type safety
- **Error Handling**: Graceful degradation, user-friendly errors, no sensitive data exposure

### Constitution Version

- **Version**: 1.0.0
- **Ratified**: 2025-11-15
- **Last Amended**: 2025-11-15

---

## Specify

**Command**: `/speckit.specify [feature description]`

**Purpose**: Create or update the feature specification from a natural language feature description.

### Feature Description

Build an Enterprise Management Information System (EMIS) for a college to centralize, automate, and streamline all core administrative, academic, and operational processes.

### Core Requirements

EMIS must provide:

#### 1. Authentication & Authorization
- Secure user authentication and authorization for all roles (students, faculty, staff, administrators, management)
- Role-based access control (RBAC) and audit logging for all sensitive actions

#### 2. Student Lifecycle Management
- **Admissions**: Application, enrollment, document verification, merit lists
- **Academic Records**: Grades, attendance, achievements, disciplinary actions
- **Transfers**: Approval workflows and record migration
- **Graduation**: Degree conferral and transcript generation
- **Alumni Tracking**: Contact management, engagement, event invitations

#### 3. Faculty & Staff Management (HR)
- **Employee Records**: Personal info, employment history, contracts
- **Payroll**: Monthly, contract, and hourly payment processing
- **Leave Management**: Casual, sick, earned, maternity/paternity, special leave
- **Performance Reviews**: Customizable criteria (teaching, research, service, punctuality)
- **Recruitment**: Job postings, applications, interview scheduling
- **Training**: Professional development tracking

#### 4. Library Management
- **Cataloging**: Book/resource catalog (ISBN, title, author, publisher, edition, category, subject classification, location, copies, condition)
- **Journal/Magazine Management**: ISSN, frequency, subscriptions
- **Digital Resources**: Licensing, IP-based and user-based access control
- **Circulation**: Book issue/return, due dates, overdue tracking, reservations, fines
- **Membership**: Borrowing limits by user type (student: 3 books/14 days, faculty: 10 books/30 days, staff: 5 books/21 days, alumni: 2 books/14 days)
- **Inventory Management**: Acquisition, cataloging, damaged/lost tracking
- **Analytics**: Circulation reports, member activity, category-wise usage, acquisition/budget, revenue, reservation demand, predictive analytics

#### 5. Learning Management System (LMS)
- **Course Management**: Creation, syllabus, objectives, prerequisites
- **Content Delivery**: Modules/lessons (video, audio, document, presentation, link, SCORM)
- **Assignments**: Individual/group, deadlines, grading rubrics, submission tracking, late penalties
- **Quizzes/Assessments**: MCQ, true/false, short/long answer, essay, randomization, time limits, auto/manual grading
- **Grading**: Grade book, rubrics, plagiarism detection (Turnitin integration), peer review, resubmission, appeals
- **Collaboration**: Discussion forums, live sessions (Zoom, Teams), study groups, messaging, collaborative editing
- **Analytics**: Engagement, completion rates, assessment performance, content effectiveness, instructor analytics, predictive analytics

#### 6. Content Management System (CMS)
- **Pages**: Rich text editor, SEO optimization, hierarchical structure
- **Menus**: Multi-level navigation, external links
- **Media Library**: Upload, organization, alt text, galleries
- **News/Articles**: Categories, featured content, approval workflow
- **Events**: Calendar, registration, banners
- **Multi-language**: Support from start for key pages, phased rollout for full content
- **Approval Workflow**: Two-step (creator submits, editor approves), emergency bypass for admins
- **SEO Tools**: Sitemap generation, meta tags

#### 7. Admissions Portal
- **Admission Cycles**: Period management, program-specific cycles
- **Online Application**: Multi-step wizard (registration, personal info, academic history, document upload, fee payment, review/submit)
- **Document Verification**: DigiLocker API integration
- **Test Management**: Scheduling, result processing
- **Merit Lists**: Automated generation based on criteria
- **Interview Management**: Scheduling, feedback collection
- **Offer Management**: Generation, acceptance tracking
- **Payment Integration**: Razorpay, PayU gateways
- **Analytics**: Admissions funnel, program-wise statistics

#### 8. Financial Management
- **Fee Management**: Structures by program/semester/category, online collection, installments, late fees
- **Accounting**: Double-entry ledger, chart of accounts, journal entries
- **Expense Management**: Budget tracking, approval workflows, vendor management
- **Compliance**: Indian Accounting Standards (Ind AS), UGC/AICTE reporting
- **Reporting**: Income statement, balance sheet, cash flow (exportable in PDF, Excel, CSV)
- **Audit Trail**: Complete transaction history
- **Multi-currency**: Support for international transactions
- **Payroll Integration**: Seamless connection with HR payroll

#### 9. Analytics & Reporting
- **Dashboards**: Module-specific and consolidated management dashboards
- **Custom Reports**: Drag-and-drop report builder for end users (with permissions)
- **Key Metrics**: Student performance, attendance, fee collection, library usage, HR statistics, admissions funnel, placement rates
- **Predictive Analytics**: Scikit-learn and pandas for data analysis
- **Export**: PDF, Excel, CSV formats

#### 10. Communication & Notification
- **Channels**: Email (mandatory), SMS (optional), in-app alerts (mandatory)
- **Bulk Messaging**: Announcements, alerts, campaigns
- **Notification History**: Complete audit trail
- **Auto-responders**: Automated acknowledgments
- **Delivery Tracking**: Status monitoring
- **Opt-in/Opt-out**: User preference management for non-essential notifications
- **Compliance**: Local data privacy laws

#### 11. Data Privacy & Compliance
- **Data Retention**: 7 years for academic/financial records, 1 year for logs
- **Data Deletion**: User-initiated (where allowed) and admin-initiated with audit trail
- **Audit Requirements**: All changes/actions must be auditable
- **GDPR Compliance**: Required for EU users
- **Indian IT Act**: Mandatory compliance
- **FERPA**: Optional (only if serving US students)

#### 12. Timetable & Scheduling
- **Academic Calendar**: Semester/term dates, holidays, exam schedules
- **Course Timetabling**: Classroom allocation, faculty assignment, conflict detection
- **Exam Scheduling**: Exam hall allocation, invigilator assignment, seating arrangements
- **Room Booking**: Classroom and facility booking for events and activities
- **Conflict Resolution**: Detection and resolution of scheduling conflicts (faculty, room, student)
- **Calendar Integration**: iCal export, Google Calendar sync

#### 13. Hostel Management
- **Room Allocation**: Room assignment based on availability, preferences, and policies
- **Occupancy Tracking**: Current occupancy status, vacancy management
- **Visitor Management**: Guest registration, entry/exit logs, security
- **Complaint Management**: Maintenance requests, issue tracking, resolution
- **Fee Management**: Hostel fee structures, payment tracking, mess charges
- **Attendance**: Hostel attendance tracking (check-in/check-out)
- **Warden Dashboard**: Overview of occupancy, complaints, attendance

#### 14. Transport Management
- **Route Management**: Bus routes, stops, timings
- **Vehicle Management**: Fleet tracking, maintenance schedules, fuel logs
- **Driver Management**: Driver assignments, attendance, performance
- **Student Transport Allocation**: Route assignment based on location
- **Fee Management**: Transport fee structures, payment tracking
- **GPS Tracking**: Real-time vehicle location (if integrated)
- **Attendance**: Transport usage tracking
- **Parent Notifications**: Bus arrival/departure alerts

#### 15. Exam Management (Extended)
- **Question Bank**: Question repository with difficulty levels, topics, bloom's taxonomy
- **Exam Paper Generation**: Automated paper generation based on syllabus and difficulty distribution
- **Online Examinations**: Browser-based exam platform with proctoring support
- **Answer Sheet Management**: Digital answer sheet upload, distribution to evaluators
- **Evaluation Management**: Evaluator assignment, blind evaluation, moderation
- **Grade Processing**: Marks entry, grade calculation, result compilation
- **Revaluation/Rechecking**: Revaluation requests, processing, fee management
- **Result Publishing**: Result declaration, mark sheets, rank lists
- **Transcript Generation**: Official transcripts with verification codes

#### 16. Placement & Career Services
- **Company Management**: Company profiles, contacts, placement history
- **Job Postings**: Job/internship listings, eligibility criteria
- **Student Applications**: Application tracking, shortlisting, interview scheduling
- **Placement Drives**: Drive scheduling, company coordination, logistics
- **Student Profile**: Resume management, skills, certifications, projects
- **Placement Statistics**: Placement reports, company-wise, branch-wise analytics
- **Alumni Placement Network**: Alumni job postings and referrals

#### 17. Research Management
- **Project Management**: Research project tracking, funding, milestones
- **Publication Management**: Journal/conference publication records
- **Patent Management**: Patent applications, status tracking
- **Grant Management**: Research grant applications, fund utilization tracking
- **Ethics & Compliance**: IRB approvals, ethics committee submissions
- **Collaboration Tracking**: External collaborations, MoUs, joint projects

#### 18. Visitor & Gate Management
- **Visitor Registration**: Pre-registration, walk-in registration
- **Entry/Exit Logs**: Gate pass generation, security logs
- **Appointment Management**: Faculty/staff appointment scheduling
- **Vehicle Entry**: Vehicle registration and tracking
- **Security Alerts**: Blacklist management, suspicious activity alerts

#### 19. Integration & API Requirements
- **REST API**: RESTful API for all modules with OpenAPI documentation
- **Webhook Support**: Event-based webhooks for real-time integrations
- **Single Sign-On (SSO)**: SAML 2.0 and OAuth 2.0 support for external identity providers
- **Third-Party Integrations**:
  - Payment Gateways: Razorpay, PayU, Stripe
  - SMS Gateways: Twilio, MSG91
  - Email Service: SendGrid, AWS SES
  - Cloud Storage: AWS S3, Google Cloud Storage
  - Video Conferencing: Zoom, Microsoft Teams APIs
  - Biometric Systems: Integration for attendance
  - ERP Systems: Data sync with existing institutional ERP
- **API Security**: API keys, OAuth 2.0, rate limiting, request signing
- **Data Export/Import**: Bulk data export/import in CSV, Excel, JSON formats
- **Webhooks for Events**: Student enrollment, fee payment, exam results, library fines

#### 20. Mobile App Requirements
- **Mobile Platform**: Native apps for iOS and Android, or Progressive Web App (PWA)
- **Student App Features**:
  - Dashboard with upcoming classes, assignments, exams
  - Attendance tracking and reports
  - Course materials access
  - Assignment submission
  - Grade viewing
  - Fee payment
  - Library account management
  - Push notifications for announcements
- **Faculty App Features**:
  - Attendance marking
  - Grade entry
  - Course material upload
  - Student queries/messages
  - Timetable and schedule
- **Parent App Features** (Optional):
  - Child's attendance and performance
  - Fee payment
  - Communication with teachers
  - Transport tracking
- **Offline Capabilities**: Key features accessible offline with sync when online

#### 21. Workflow & Approval Management
- **Configurable Workflows**: Multi-step approval workflows for various processes
- **Leave Approvals**: Faculty/staff leave request workflows
- **Expense Approvals**: Budget approval chains
- **Course Approvals**: New course proposal approvals
- **Document Approvals**: Certificate requests, NOCs, bonafide certificates
- **Admission Approvals**: Application review and approval workflows
- **Workflow Builder**: Admin interface to create and modify approval workflows
- **Escalation Rules**: Auto-escalation if approval pending beyond threshold
- **Delegate Support**: Temporary delegation of approval authority

#### 22. Document Management
- **Document Templates**: Pre-defined templates for certificates, letters, forms
- **Digital Signatures**: E-signature support for authorized personnel
- **Document Versioning**: Version control for important documents
- **Document Search**: Full-text search across uploaded documents
- **Document Expiry**: Tracking of document expiration (IDs, certificates)
- **QR Code Verification**: QR codes on certificates for authenticity verification
- **Bulk Document Generation**: Mass generation of certificates, transcripts, ID cards

#### 23. Survey & Feedback Management
- **Survey Builder**: Create custom surveys and feedback forms
- **Question Types**: Multiple choice, rating scales, text responses, matrix questions
- **Target Audience**: Send surveys to specific user groups
- **Response Collection**: Anonymous and attributed responses
- **Analytics**: Survey response analytics, charts, sentiment analysis
- **Course Feedback**: End-of-semester course and faculty feedback
- **Exit Surveys**: Alumni exit surveys, employee exit interviews
- **Campus Climate Surveys**: Student satisfaction, safety surveys

### Rationale

EMIS will eliminate data silos, reduce manual work, improve transparency, and enable data-driven decision-making for all stakeholders. Every requirement is included to ensure the system fully supports the operational, academic, and strategic needs of a modern college.

### Edge Cases & Non-Functional Requirements

#### System-Wide Edge Cases

1. **Concurrent Operations**
   - What happens when two users try to update the same record simultaneously?
   - How to handle concurrent enrollment in courses with limited capacity?
   - Race conditions in library book reservations when multiple users reserve the last available copy

2. **Data Integrity**
   - Handling of orphaned records when parent entities are deleted (cascading deletes vs soft deletes)
   - What happens when a student is deleted but has active library loans or pending fee payments?
   - Data consistency when transactions span multiple modules (e.g., admission → enrollment → fee generation)

3. **Network & Service Failures**
   - Behavior when payment gateway is unreachable during fee payment
   - Handling of failed email/SMS delivery (retry mechanism, queue management)
   - Video conferencing integration failures during live sessions
   - DigiLocker API unavailability during document verification

4. **Performance & Scalability**
   - System behavior under peak load (admission season, exam result day, enrollment periods)
   - Handling of bulk operations (bulk student import, mass email campaigns)
   - Large file uploads (student documents, video content for LMS)
   - Report generation for large datasets (10,000+ students, multi-year data)

5. **Authentication & Session Management**
   - Session timeout handling and auto-logout after inactivity
   - Concurrent login from multiple devices/locations
   - Password reset when user has no access to registered email
   - Account lockout after multiple failed login attempts
   - Token expiry during long-running operations

6. **Data Migration & Imports**
   - Handling of duplicate records during bulk imports
   - Invalid or malformed data in CSV/Excel imports
   - Character encoding issues (special characters, non-English names)
   - Date format inconsistencies across different locales

7. **File Management**
   - Maximum file size limits for uploads
   - Unsupported file formats
   - Virus/malware scanning for uploaded documents
   - Storage quota management per user/module
   - Handling of corrupted files

8. **Timezone & Localization**
   - Handling multiple timezones (international students, online courses)
   - Date/time display consistency across different user locations
   - Academic calendar across different campuses in different timezones
   - Deadline management for global users

#### Module-Specific Edge Cases

**Authentication & Authorization:**
- First-time login flow and mandatory password change
- Password complexity validation and user-friendly error messages
- Two-factor authentication failure or device loss
- Role change propagation (user promoted to admin mid-session)
- Deactivated user attempting to login

**Student Lifecycle:**
- Student withdrawal mid-semester (fee refund, grade handling)
- Course dropout and re-enrollment rules
- Maximum credits per semester enforcement
- Prerequisites not met when enrolling in advanced courses
- Duplicate admission applications from same applicant
- Transcript requests for students with pending dues

**HR Module:**
- Overlapping leave requests handling
- Leave balance going negative
- Payroll calculation when employee joins/leaves mid-month
- Performance review cycle conflicts with employee transitions
- Contract renewal reminders and auto-expiry

**Library Management:**
- Book return after due date with fine calculation
- Lost book handling and replacement cost
- Multiple simultaneous reservations for same book
- Digital resource access from unauthorized IP addresses
- Book condition downgrade after return

**Learning Management System:**
- Assignment submission after deadline
- Quiz timeout and auto-submission
- Plagiarism detection false positives
- Grade dispute and appeal workflows
- Course withdrawal impact on grades (W, WF, etc.)
- Group assignment when member drops the course
- Large video upload timeout

**Content Management System:**
- Content approval rejection and revision workflow
- Page deletion with active references from other pages
- Media file deletion used in multiple pages
- URL slug conflicts
- SEO meta tag limits and validation

**Admissions Portal:**
- Application submission after deadline
- Incomplete applications (missing documents, payment pending)
- Merit list tie-breaking rules
- Offer acceptance deadline enforcement
- Payment gateway transaction failures and reconciliation
- Document verification failures

**Financial Management:**
- Partial payment handling
- Refund processing workflows
- Fee waiver and scholarship application
- Late fee calculation and compounding rules
- Payment reversal/chargeback handling
- Currency conversion for international payments
- Financial year-end closing procedures

**Analytics & Reporting:**
- Report generation timeout for very large datasets
- Data export size limits
- Custom report with invalid query parameters
- Scheduled report delivery failures
- Dashboard loading with incomplete data

**Communication & Notification:**
- Bulk email rate limiting to prevent spam blacklisting
- Notification delivery failure handling
- Email bounce-back processing
- Opt-out link in all bulk communications
- Notification priority and queuing during high volume

#### Non-Functional Requirements

1. **Performance Requirements**
   - API response time: <500ms for 95th percentile
   - Page load time: <2 seconds for initial load
   - Database query optimization for reports: <5 seconds
   - Concurrent user support: Minimum 1,000 simultaneous users
   - Background job processing: High-priority jobs <1 minute

2. **Availability & Reliability**
   - System uptime: 99.5% (excluding scheduled maintenance)
   - Scheduled maintenance windows: Off-peak hours only
   - Database backup: Daily automated backups with point-in-time recovery
   - Disaster recovery: RTO (Recovery Time Objective) <4 hours, RPO (Recovery Point Objective) <1 hour

3. **Scalability**
   - Support for up to 50,000 students
   - Support for up to 5,000 concurrent users
   - Storage: Minimum 1TB for documents and media
   - Horizontal scaling capability for API and worker nodes

4. **Security Requirements**
   - Password policy: Minimum 8 characters, complexity requirements, rotation every 90 days
   - Session timeout: 30 minutes of inactivity
   - Failed login attempts: Lock account after 5 consecutive failures
   - API rate limiting: 100 requests per minute per user, 1000 per minute per IP
   - Data encryption: AES-256 for data at rest, TLS 1.3 for data in transit
   - Vulnerability scanning: Weekly automated scans
   - Penetration testing: Annual third-party security audit

5. **Usability Requirements**
   - Mobile responsive design for all user interfaces
   - Accessibility: WCAG 2.1 Level AA compliance
   - Browser support: Latest 2 versions of Chrome, Firefox, Safari, Edge
   - Keyboard navigation support for all critical workflows
   - Screen reader compatibility
   - Multi-language UI support (English, Hindi, and one regional language minimum)

6. **Data Backup & Recovery**
   - Automated daily backups with 30-day retention
   - Weekly full backups with 1-year retention
   - Point-in-time recovery capability for database
   - Backup verification and restore testing quarterly
   - Offsite backup storage

7. **Monitoring & Alerting**
   - Real-time error tracking and alerting
   - Performance monitoring with anomaly detection
   - Uptime monitoring with 5-minute check intervals
   - Alert escalation for critical issues
   - Monthly SLA reports

8. **Browser & Device Compatibility**
   - Desktop: Windows, macOS, Linux
   - Mobile: iOS 14+, Android 10+
   - Tablet: iPad, Android tablets
   - Progressive Web App (PWA) support for offline access to critical features

### Expected Output

When `/speckit.specify` is executed, it should:

1. Create a feature branch (e.g., `001-emis-core`)
2. Generate `specs/001-emis-core/spec.md` with:
   - User scenarios organized by priority (P1, P2, P3...)
   - Each scenario independently testable
   - Functional requirements (FR-001, FR-002...)
   - Non-functional requirements
   - Key entities
   - Success criteria
   - Edge cases
3. Generate initial checklist at `specs/001-emis-core/checklists/requirements.md`

---

## Clarify

**Command**: `/speckit.clarify`

**Purpose**: Identify underspecified areas in the current feature spec by asking targeted clarification questions and encoding answers back into the spec.

### Clarifications Completed


The following clarifications were obtained to ensure all EMIS requirements are fully understood and unambiguous:

#### 1. User Roles & Permissions

**Q: What are the specific permissions and actions available to each user role?**

- **Students**: View and update own records, enroll in courses, submit assignments, access learning resources
- **Faculty**: Manage courses, grade students, manage attendance, access relevant reports
- **Staff**: Manage administrative records, process admissions, handle library/finance operations per department
- **Administrators**: Full access to all modules, user management, system settings
- **Management**: View analytics, reports, high-level dashboards (read-only, cannot modify operational data)

**Q: Are there sub-roles or role hierarchies?**

- **Department Heads** (faculty/staff): Additional permissions to manage department-specific data and approve requests
- **Super-admins**: Unrestricted access for system configuration and audit

#### 2. Student Lifecycle Management

**Q: Required data fields for each stage?**

- **Admission**: Personal info, contact, previous education, documents, application status
- **Enrollment**: Program, batch, semester, fee status
- **Academic Records**: Grades, attendance, disciplinary actions, achievements
- **Alumni**: Contact, employment, engagement status

**Q: Special workflows?**

- **Transfers**: Require approval and record migration
- **Alumni Tracking**: Periodic engagement and event invitations
- **Re-admission**: Simplified application and approval process

#### 3. Faculty & Staff Management

**Q: Payroll rules, leave types, performance review criteria?**

- **Payroll**: Monthly, contract, and hourly payments
- **Leave Types**: Casual, sick, earned, maternity/paternity, special
- **Performance Reviews**: Customizable criteria (teaching, research, service, punctuality)

**Q: Contract/part-time staff support?**

- Both contract/part-time and full-time staff supported with configurable roles and payroll

#### 4. Library Management

**Q: Circulation policies for different user types?**

Borrowing limits and overdue fines configurable by user type:
- **Students**: 3 books, 14 days
- **Faculty**: 10 books, 30 days
- **Staff**: 5 books, 21 days
- **Alumni**: 2 books, 14 days

**Q: Digital resource licensing and access control?**

- Yes, including IP-based and user-based restrictions

#### 5. Learning Management

**Q: Content types and assessment formats?**

- **Content Types**: Video, audio, document, presentation, link, SCORM
- **Assessments**: Quizzes (MCQ, true/false, short/long answer), assignments (file/text), peer review, group work

**Q: External integrations?**

- **Video Conferencing**: Zoom, Teams
- **Plagiarism Detection**: Turnitin
- **Content Repositories**: YouTube, Google Drive

#### 6. Content Management

**Q: Approval workflows for publishing?**

- Two-step approval: Content creator submits, editor reviews/approves before publishing
- Emergency bypass for admins

**Q: Multi-language support timing?**

- Required from start for key pages; full content translation can be phased in

#### 7. Admissions Portal

**Q: Application process steps and data fields?**

- **Steps**: Registration, personal info, academic history, document upload, fee payment, review/submit
- **Data**: Name, DOB, contact, address, previous education, program applied, supporting documents

**Q: Payment gateways and document verification?**

- **Payment Gateways**: Razorpay, PayU (at least two)
- **Document Verification**: DigiLocker API

#### 8. Financial Management

**Q: Accounting standards and compliance?**

- Indian Accounting Standards (Ind AS)
- UGC/AICTE reporting guidelines

**Q: Reporting formats and exports?**

- **Formats**: PDF, Excel, CSV
- **Standard Reports**: Income statement, balance sheet, cash flow

#### 9. Analytics & Reporting

**Q: Key metrics and dashboards?**

- **Metrics**: Student performance, attendance, fee collection, library usage, HR stats, admissions funnel, placement rates
- **Dashboards**: Module-specific and consolidated management dashboard

**Q: Custom report creation by end users?**

- Yes, via drag-and-drop report builder (with permissions)

#### 10. Communication & Notification

**Q: Mandatory channels and bulk requirements?**

- **Mandatory**: Email, in-app notifications
- **Optional**: SMS
- **Bulk Messaging**: Required for announcements and alerts

**Q: Compliance and opt-in/opt-out?**

- Users must be able to opt-in/opt-out of non-essential notifications
- All communication must comply with local data privacy laws

#### 11. Data Privacy & Compliance

**Q: Data retention, deletion, and audit requirements?**

- **Retention**: 7 years for academic/financial records, 1 year for logs
- **Deletion**: User-initiated (where allowed) and admin-initiated with audit trail
- **Audit**: All changes/actions must be auditable

**Q: Regional/institutional compliance standards?**

- **Required**: GDPR, Indian IT Act
- **Optional**: FERPA (only if serving US students)

### Additional Refinements

- For sample projects, create 5-15 tasks per project with random distribution across completion states
- Ensure at least one task in each completion stage
- Review and acceptance checklist should be checked off for items meeting criteria

---

## Plan

**Command**: `/speckit.plan`

**Purpose**: Create a comprehensive technical implementation plan based on the feature specification and clarifications.

### Technical Stack

The EMIS will be implemented as a **modular monolith** with the following technology stack:

- **Language**: Python 3.11+
- **API Framework**: FastAPI
- **Database**: PostgreSQL 15+
- **ORM**: Async SQLAlchemy
- **Caching**: Redis
- **Background Jobs**: Celery with Redis as message broker
- **Containerization**: Docker and Docker Compose
- **API Documentation**: OpenAPI/Swagger (auto-generated)
- **Testing**: pytest (unit, integration, contract tests)
- **CI/CD**: GitHub Actions
- **Infrastructure-as-Code**: Docker Compose (local), optional Terraform (cloud)
- **Monitoring**: Prometheus, Grafana, Sentry
- **Analytics**: Scikit-learn, pandas

### Architecture & Core Principles

#### Modular Monolith Architecture
- Clear separation of core, domain, infrastructure, and API layers
- Each domain module independently testable and observable
- Shared infrastructure (auth, db, cache) across modules

#### Layer Structure
- **API Layer**: Thin, stateless, handles HTTP concerns only
- **Domain Layer**: All business logic, rules, workflows
- **Infrastructure Layer**: Database, external services, file storage
- **Core Layer**: Shared utilities, config, middleware

#### Development Principles
- **Contract-First**: API contracts defined before implementation
- **Test-Driven Development**: Tests written before code
- **CLI for Admin**: All admin operations scriptable
- **RBAC Everywhere**: Role-based access control enforced at API layer
- **Audit Everything**: Full audit trail for sensitive operations
- **Compliance by Design**: GDPR and Indian IT Act requirements built-in

### Module-Level Implementation

#### Authentication Module
- **Models**: User, Role, Permission, AuditLog
- **Services**: Authentication, authorization, password management, 2FA
- **APIs**: Login, registration, password reset, token refresh
- **Middleware**: RBAC enforcement, request logging

#### Students Module
- **Models**: Student, Enrollment, AcademicRecord, Attendance, Transfer, Alumni
- **Services**: Student lifecycle, enrollment management, attendance tracking, alumni relations
- **APIs**: Student CRUD, enrollment operations, attendance marking, transcript generation
- **Workflows**: Admission → Enrollment → Active → Transfer/Graduate → Alumni

#### HR Module
- **Models**: Employee, Payroll, Leave, PerformanceReview, Recruitment, Training
- **Services**: Employee management, payroll processing, leave approval, performance evaluation
- **APIs**: Employee CRUD, payroll operations, leave requests, review management
- **Rules Engine**: Configurable payroll rules, leave policies

#### Library Module
- **Models**: Book, Member, Issue, Reservation, Fine, DigitalResource, Journal
- **Services**: Cataloging, circulation, reservation management, fine calculation, analytics
- **APIs**: Catalog search, issue/return, reservation, fine payment, reports
- **Integrations**: Barcode/RFID scanners, IP-based access control
- **Analytics**: Usage patterns, member activity, circulation statistics

#### Learning Management System (LMS)
- **Models**: Course, Module, Lesson, Assignment, Quiz, Submission, Grade, Forum, LiveSession
- **Services**: Course management, content delivery, assessment engine, grading, collaboration
- **APIs**: Course CRUD, content access, assignment submission, quiz taking, grading, forum posts
- **Integrations**: Video conferencing (Zoom, Teams), plagiarism detection (Turnitin), content repos (YouTube, Google Drive)
- **Analytics**: Engagement, completion rates, assessment performance, content effectiveness

#### Content Management System (CMS)
- **Models**: Page, Menu, Media, News, Event, Gallery, SEO
- **Services**: Content creation, approval workflow, media management, SEO optimization
- **APIs**: Page CRUD, media upload, news/events management, menu configuration
- **Features**: Rich text editor, multi-language support, versioning/rollback
- **Workflow**: Creator submits → Editor approves → Published (with admin bypass)

#### Admissions Module
- **Models**: Application, Document, Fee, Test, Interview, MeritList, Offer
- **Services**: Application processing, document verification, test management, merit list generation, offer management
- **APIs**: Application submission, status tracking, document upload, fee payment, interview scheduling
- **Integrations**: Payment gateways (Razorpay, PayU), DigiLocker API
- **Analytics**: Admissions funnel, program-wise statistics

#### Financial Management (Accounts)
- **Models**: FeeStructure, Payment, Expense, Budget, JournalEntry, ChartOfAccounts, Ledger
- **Services**: Fee management, double-entry accounting, expense tracking, budget management, reporting
- **APIs**: Fee CRUD, payment processing, expense approval, budget tracking, financial reports
- **Compliance**: Indian Accounting Standards (Ind AS), UGC/AICTE reporting
- **Reports**: Income statement, balance sheet, cash flow (PDF, Excel, CSV export)
- **Integration**: Payroll module integration

#### Analytics Module
- **Services**: Aggregation across all modules, custom report builder, predictive analytics
- **APIs**: Dashboard data, custom report creation, metric queries, data export
- **Features**: Module-specific dashboards, management dashboard, drag-and-drop report builder
- **Analytics**: Scikit-learn for predictive models, pandas for data processing
- **Metrics**: Student performance, attendance, fee collection, library usage, HR stats, admissions, placements

#### Notifications Module
- **Models**: Notification, NotificationTemplate, NotificationLog, UserPreference
- **Services**: Email service, SMS service (optional), in-app notifications, bulk messaging, preference management
- **APIs**: Send notification, bulk send, notification history, preference management
- **Features**: Auto-responders, delivery tracking, opt-in/opt-out management
- **Compliance**: Data privacy laws, consent management

### DevOps & Operations

#### Development Environment
- Docker Compose for local development
- Environment variables via `.env` files
- Automated database migrations (Alembic)
- Seed scripts for test data

#### CI/CD Pipeline (GitHub Actions)
- **Linting**: flake8, black, isort
- **Type Checking**: mypy
- **Testing**: pytest (unit, integration, contract)
- **Coverage**: Minimum threshold enforcement
- **Build**: Docker image creation
- **Deploy**: Automated deployment to staging/production

#### Infrastructure
- Docker Compose for local/staging
- Optional Terraform for cloud deployment (AWS/GCP/Azure)
- Secrets management (environment-based)
- Database migrations automation
- Health checks for all services

#### Monitoring & Logging
- **Centralized Logging**: Structured JSON logs
- **Metrics**: Prometheus for collection
- **Dashboards**: Grafana for visualization
- **Error Tracking**: Sentry for exceptions
- **Health Checks**: Readiness and liveness endpoints

### Testing & Quality

#### Test Strategy
- **Unit Tests**: All domain logic (100% coverage goal)
- **Integration Tests**: Cross-module workflows
- **Contract Tests**: OpenAPI schema validation
- **End-to-End Tests**: Critical user journeys
- **Manual Testing**: Accessibility and usability

#### Quality Gates
- Linting (flake8, black, isort) must pass
- Type checking (mypy) must pass
- Minimum test coverage threshold
- No high-severity security vulnerabilities
- All contract tests pass

### Security & Compliance

#### Security Measures
- **Encryption in Transit**: HTTPS/TLS for all communications
- **Encryption at Rest**: Database and file storage encryption
- **Authentication**: JWT tokens with refresh mechanism
- **Authorization**: RBAC enforced at API layer
- **Audit Logging**: All sensitive actions logged with user, timestamp, action details
- **Input Validation**: Comprehensive validation on all inputs
- **Rate Limiting**: API rate limiting to prevent abuse
- **Vulnerability Scanning**: Regular dependency and code scans

#### Compliance
- **GDPR**: Data privacy, consent, right to deletion, data portability
- **Indian IT Act**: Local regulatory requirements
- **Data Retention**: 7 years for academic/financial records, 1 year for logs
- **Data Deletion**: User and admin-initiated with audit trail
- **Audit Trail**: Complete history of all changes and actions

### Documentation

#### API Documentation
- Auto-generated from OpenAPI/Swagger
- Interactive API explorer
- Authentication documentation
- Example requests/responses
- Error code reference

#### User Documentation
- User manuals (role-specific)
- Admin guides
- Onboarding tutorials
- FAQ and troubleshooting

#### Technical Documentation
- Architecture Decision Records (ADRs)
- Change logs
- Deployment guides
- Development setup guide
- Contributing guidelines

### Implementation Notes

This plan ensures a robust, scalable, and maintainable EMIS platform that:
- Meets all functional requirements
- Adheres to technical best practices
- Ensures compliance with all regulations
- Provides excellent observability and maintainability
- Supports incremental development and deployment

### Expected Output

When `/speckit.plan` is executed, it should:

1. Generate `specs/[###-feature]/plan.md` with:
   - Technical context and stack decisions
   - Constitution compliance check
   - Project structure (documentation and source code)
   - Module-level architecture
   - Data models overview
   - API contracts outline
   - Testing strategy
   - DevOps approach
2. Generate `specs/[###-feature]/research.md` (Phase 0 research)
3. Generate `specs/[###-feature]/data-model.md` (Phase 1 data models)
4. Generate `specs/[###-feature]/contracts/` (Phase 1 API contracts)
5. Generate `specs/[###-feature]/quickstart.md` (Phase 1 quickstart guide)

---

## Analyze

**Command**: `/speckit.analyze`

**Purpose**: Perform a non-destructive cross-artifact consistency and quality analysis across spec.md, plan.md, and tasks.md.

### Analysis Performed

Analyzed the EMIS specification for inconsistencies, gaps, and alignment with constitution principles.

### Key Findings

#### Alignment with Constitution
- ✅ **Security**: All requirements align with encryption, audit logging, GDPR compliance principles
- ✅ **Modularity**: Library-first approach, CLI interface, clear separation of concerns maintained
- ✅ **Test-First**: TDD, contract-first, integration-first development enforced
- ✅ **Simplicity**: Modular monolith approach (1 project) adheres to ≤3 projects principle
- ✅ **Observability**: Health checks, structured logging, metrics defined
- ✅ **Maintainability**: Documentation, CI/CD, code quality standards specified
- ✅ **Compliance**: Data privacy, code quality, error handling requirements included

#### Coverage Analysis
- **Total Requirements**: 100% of specified features mapped to implementation tasks
- **Module Coverage**: All 10 modules (Auth, Students, HR, Library, LMS, CMS, Admissions, Accounts, Analytics, Notifications) have complete specifications

#### Gaps Identified

The following areas need further definition before implementation:

1. **API Contracts** (HIGH PRIORITY)
   - Detailed endpoint specifications for each module
   - Request/response schemas
   - Error response formats
   - Status codes and error codes
   - Rate limiting specifications

2. **Error Handling Specifications** (HIGH PRIORITY)
   - Error categorization and codes
   - User-facing error messages
   - Logging levels and formats
   - Error recovery strategies
   - Fallback behaviors

3. **Integration Testing Requirements** (MEDIUM PRIORITY)
   - Cross-module test scenarios
   - End-to-end user journeys
   - Performance benchmarks
   - Load testing requirements
   - Security testing scenarios

4. **Data Migration Strategy** (MEDIUM PRIORITY)
   - Schema versioning approach
   - Data migration scripts structure
   - Rollback procedures
   - Zero-downtime migration strategy

5. **Scalability Specifications** (LOW PRIORITY)
   - Horizontal scaling strategy
   - Database sharding/partitioning approach
   - Caching strategies per module
   - Background job queuing priorities

### Inconsistencies Detected

No major inconsistencies detected. Minor clarifications needed:

1. **Terminology Consistency**: "Accounts" vs "Financial Management" - use consistently throughout
2. **Module Dependencies**: Document explicit dependencies between modules (e.g., Admissions → Students)
3. **User Role Mapping**: Ensure all modules respect the same role hierarchy

### Recommendations

1. **Before `/speckit.tasks`**:
   - Complete API contract definitions in `contracts/` directory
   - Define error handling standards
   - Document cross-module dependencies

2. **During Implementation**:
   - Start with foundational modules (Auth, Core)
   - Implement modules in dependency order
   - Maintain strict API contract compliance

3. **Testing Strategy**:
   - Write contract tests first for all endpoints
   - Integration tests for cross-module workflows
   - End-to-end tests for complete user journeys

### Expected Output

When `/speckit.analyze` is executed, it generates a Markdown report with:

- Cross-artifact consistency analysis
- Constitution alignment validation
- Coverage gaps identification
- Inconsistency detection
- Ambiguity highlighting
- Recommendations for remediation
- Severity-categorized findings (CRITICAL, HIGH, MEDIUM, LOW)

---

## Checklist

**Command**: `/speckit.checklist [domain/aspect]`

**Purpose**: Generate custom quality checklists to validate requirements before implementation. Checklists serve as "unit tests for English" - validating requirement quality, not implementation.

### Checklists Generated

#### API Requirements Checklist

Generated at: `specs/001-emis-core/checklists/api.md` (45 items)

**Focus Areas**:
- Requirement completeness (are all necessary API requirements documented?)
- Requirement clarity (are endpoints, methods, and responses unambiguous?)
- Requirement consistency (do API patterns align across modules?)
- Acceptance criteria quality (are API success criteria measurable?)
- Scenario coverage (are all API flows and edge cases addressed?)
- Error handling (are all error scenarios defined?)
- Authentication/authorization (are security requirements clear?)
- Rate limiting (are throttling policies specified?)
- Versioning (is API versioning strategy defined?)
- Documentation (are all APIs documented with examples?)

#### Security Requirements Checklist

Generated at: `specs/001-emis-core/checklists/security.md` (50 items)

**Focus Areas**:
- Authentication requirements (are auth mechanisms fully specified?)
- Authorization requirements (is RBAC completely defined?)
- Data encryption (are encryption requirements clear for transit and rest?)
- Audit logging (are all auditable actions identified?)
- GDPR compliance (are all GDPR requirements addressed?)
- Indian IT Act compliance (are local regulations covered?)
- Input validation (are validation rules defined?)
- SQL injection prevention (are countermeasures specified?)
- XSS prevention (are sanitization requirements clear?)
- CSRF protection (are token requirements defined?)
- Session management (are session policies clear?)
- Password policies (are strength and rotation rules specified?)
- Data retention (are retention periods clear for all data types?)
- Data deletion (are deletion workflows defined?)
- Access control (are permission boundaries clear?)

### Checklist Principles

Checklists validate **requirement quality**, NOT implementation:

❌ **WRONG** (Testing implementation):
- "Verify the login endpoint returns JWT token"
- "Test that password hashing uses bcrypt"
- "Confirm RBAC middleware blocks unauthorized users"

✅ **CORRECT** (Testing requirements quality):
- "Are authentication token types and expiry specified? [Completeness]"
- "Is password hashing algorithm requirement clearly stated? [Clarity]"
- "Are RBAC enforcement points identified for all endpoints? [Coverage]"
- "Is the fallback behavior defined when auth service is unavailable? [Edge Cases]"
- "Are rate limiting thresholds specified for login attempts? [Completeness]"

### Expected Output

When `/speckit.checklist` is executed with a domain (e.g., `api`, `security`, `ux`), it should:

1. Ask 2-5 clarifying questions to understand scope and focus
2. Load feature context from `spec.md`, `plan.md`, `tasks.md`
3. Generate domain-specific checklist at `specs/[###-feature]/checklists/[domain].md`
4. Include 30-60 items organized by requirement quality dimensions:
   - Requirement Completeness
   - Requirement Clarity
   - Requirement Consistency
   - Acceptance Criteria Quality
   - Scenario Coverage
   - Edge Case Coverage
   - Non-Functional Requirements
   - Dependencies & Assumptions
   - Ambiguities & Conflicts
5. Each item formatted as: `- [ ] CHK### [Dimension] Question about requirement quality [Spec §X.Y or Gap]`

---

## Tasks

**Command**: `/speckit.tasks`

**Purpose**: Generate an actionable, dependency-ordered task breakdown for feature implementation based on user stories and design artifacts.

### Task Organization Principles

#### User Story-Centric Organization
Tasks MUST be organized by user story to enable:
- Independent implementation of each story
- Independent testing of each story
- Incremental delivery (MVP = User Story 1)
- Parallel development across stories

#### Task Format (REQUIRED)

Every task MUST follow this format:

```markdown
- [ ] [TaskID] [P?] [Story?] Description with file path
```

**Components**:
1. **Checkbox**: `- [ ]` (markdown checkbox)
2. **Task ID**: Sequential (T001, T002, T003...)
3. **[P] marker**: Include ONLY if parallelizable
4. **[Story] label**: [US1], [US2], [US3] for user story tasks
5. **Description**: Clear action with exact file path

**Examples**:
- ✅ `- [ ] T001 Create project structure per implementation plan`
- ✅ `- [ ] T005 [P] Implement authentication middleware in src/middleware/auth.py`
- ✅ `- [ ] T012 [P] [US1] Create User model in src/models/user.py`
- ❌ `- [ ] Create User model` (missing ID and path)

#### Phase Structure

1. **Phase 1: Setup** - Project initialization and basic structure
2. **Phase 2: Foundational** - Blocking prerequisites for ALL user stories
3. **Phase 3+: User Stories** - One phase per user story (in priority order: P1, P2, P3...)
4. **Final Phase: Polish** - Cross-cutting concerns affecting multiple stories

Within each user story phase:
- Tests (if requested) → Models → Services → Endpoints → Integration

#### Dependencies & Execution Order

- Setup → Foundational → User Stories (parallel or sequential) → Polish
- Each user story is independently testable after Foundational phase completes
- Tasks within a story follow: Tests → Models → Services → Endpoints
- Parallel opportunities marked with [P] within each phase

### Example Task Breakdown Structure

```markdown
## Phase 1: Setup
- [ ] T001 Create project structure
- [ ] T002 Initialize Python project with FastAPI
- [ ] T003 [P] Configure linting (flake8, black, isort)

## Phase 2: Foundational (MUST complete before ANY user story)
- [ ] T004 Setup database and migrations
- [ ] T005 [P] Implement auth framework
- [ ] T006 [P] Setup API routing structure

## Phase 3: User Story 1 - User Authentication (P1) 🎯 MVP
**Goal**: Users can register, login, and manage their accounts
**Independent Test**: Can fully test by registering user, logging in, resetting password

### Tests for US1 (if requested)
- [ ] T010 [P] [US1] Contract test for /auth/register endpoint
- [ ] T011 [P] [US1] Integration test for login flow

### Implementation for US1
- [ ] T012 [P] [US1] Create User model in src/models/user.py
- [ ] T013 [US1] Implement AuthService in src/services/auth_service.py
- [ ] T014 [US1] Implement /auth/register endpoint in src/api/auth.py
- [ ] T015 [US1] Implement /auth/login endpoint in src/api/auth.py

## Phase 4: User Story 2 - Course Management (P2)
[Similar structure for next priority...]
```

### Expected Output

When `/speckit.tasks` is executed, it should:

1. Load design documents from `specs/[###-feature]/`:
   - `plan.md` (REQUIRED) - tech stack, structure
   - `spec.md` (REQUIRED) - user stories with priorities
   - `data-model.md` (optional) - entities
   - `contracts/` (optional) - API endpoints
   - `research.md` (optional) - decisions
2. Generate `specs/[###-feature]/tasks.md` with:
   - Complete task breakdown organized by user story
   - All tasks in checklist format with IDs, [P] markers, [Story] labels
   - Clear phases (Setup, Foundational, User Stories, Polish)
   - Dependency graph showing execution order
   - Parallel execution opportunities
   - Independent test criteria for each user story
3. Report:
   - Total task count
   - Tasks per user story
   - Parallel opportunities
   - Suggested MVP scope (typically User Story 1)

**Note**: Tests are OPTIONAL - only include if explicitly requested in feature specification or if TDD approach is specified.

---

## Implement

**Command**: `/speckit.implement`

**Purpose**: Execute the tasks defined in `tasks.md` to implement the feature.

### Implementation Workflow

#### Prerequisites
- `spec.md` must exist and be complete
- `plan.md` must exist with technical details
- `tasks.md` must exist with complete task breakdown
- All checklists should be reviewed and addressed

#### Execution Process

1. **Load Task List**: Read `specs/[###-feature]/tasks.md`
2. **Validate Prerequisites**: Ensure foundational tasks are complete
3. **Execute Tasks Sequentially**: Process tasks in dependency order
   - Setup tasks first
   - Foundational tasks second
   - User story tasks (MVP first, then by priority)
   - Polish tasks last
4. **Test After Each Task**: Verify each task completion before moving to next
5. **Update Task Status**: Mark completed tasks with `[x]`
6. **Handle Errors**: Log errors, mark problematic tasks, continue or stop as appropriate
7. **Generate Summary**: Report on completion status, tests passed/failed, next steps

#### Implementation Principles

- **One Task at a Time**: Complete and verify before moving to next
- **Test Immediately**: Run tests after each implementation task
- **Incremental Commits**: Commit after each logical unit of work
- **Follow Patterns**: Use established patterns from plan.md
- **Respect Dependencies**: Never skip foundational tasks
- **Document Decisions**: Update ADRs for significant technical choices

#### Error Handling

If a task fails:
1. Log the error with full context
2. Mark task as blocked
3. Identify dependencies affected
4. Suggest remediation steps
5. Ask user whether to continue or stop

#### Success Criteria

Implementation is complete when:
- All tasks marked as `[x]` complete
- All tests passing
- All checklists validated
- Documentation updated
- Ready for code review/deployment

### Expected Output

When `/speckit.implement` is executed, it should:

1. Check prerequisites (spec, plan, tasks exist)
2. Execute tasks in dependency order
3. Run tests after each task
4. Update task status in `tasks.md`
5. Generate implementation log
6. Report completion status:
   - Tasks completed
   - Tests passed/failed
   - Files created/modified
   - Blockers encountered
   - Next steps

**Note**: This command assumes complete task breakdown exists in `tasks.md`. If tasks are incomplete or missing, run `/speckit.tasks` first.

---

## Summary

This SpecKit documentation provides a complete workflow for specifying, planning, and implementing features in the EMIS project:

1. **Constitution** - Establish governing principles
2. **Specify** - Define feature requirements and user stories
3. **Clarify** - Resolve ambiguities and underspecified areas
4. **Plan** - Create technical implementation plan
5. **Analyze** - Validate consistency and completeness
6. **Checklist** - Generate quality validation checklists
7. **Tasks** - Break down into actionable, dependency-ordered tasks
8. **Implement** - Execute tasks and deliver feature

Each command builds on the previous ones, creating a robust specification and implementation workflow that ensures quality, completeness, and alignment with project principles.

---

## File Structure

When following the SpecKit workflow, the following structure will be created:

```
specs/
└── [###-feature-name]/
    ├── spec.md                    # Feature specification (/speckit.specify)
    ├── plan.md                    # Technical plan (/speckit.plan)
    ├── research.md                # Research findings (/speckit.plan Phase 0)
    ├── data-model.md              # Data models (/speckit.plan Phase 1)
    ├── quickstart.md              # Quickstart guide (/speckit.plan Phase 1)
    ├── tasks.md                   # Task breakdown (/speckit.tasks)
    ├── contracts/                 # API contracts (/speckit.plan Phase 1)
    │   ├── auth.yaml
    │   ├── students.yaml
    │   └── ...
    └── checklists/                # Quality checklists (/speckit.checklist)
        ├── requirements.md
        ├── api.md
        ├── security.md
        └── ...
```

---

## References

- Constitution: `.specify/memory/constitution.md`
- Templates: `.specify/templates/`
- Scripts: `.specify/scripts/bash/`
- Prompts: `.github/prompts/speckit.*.prompt.md`
