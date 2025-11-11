/speckit.constitution Establish this project's governing principles to ensure consistent decision-making throughout all phases. Principles: security (encryption, audit logging, GDPR compliance), modularity (library-first, CLI interface, separation of concerns), test-first (TDD, contract-first, integration-first), simplicity (≤3 projects, no future-proofing), observability (health checks, logging), maintainability (documentation, CI/CD), and compliance (data privacy, code quality, error handling).


/speckit.specify Build an Enterprise Management Information System (EMIS) for a college to centralize, automate, and streamline all core administrative, academic, and operational processes. EMIS must provide:
- Secure user authentication and authorization for all roles (students, faculty, staff, administrators, management).
- Complete student lifecycle management: admission, enrollment, academic records, attendance, transfers, graduation, alumni tracking.
- Faculty and staff management: HR records, payroll, leave, performance reviews, recruitment, training.
- Library management: cataloging, circulation, reservations, fines, analytics, digital resource access, book/resource catalog (ISBN, title, author, publisher, edition, category, subject classification, location, copies, condition), journal/magazine subscriptions (ISSN, frequency), digital resources, acquisition/cataloging, inventory, damaged/lost tracking, membership, borrowing limits, book issue/return, due dates, overdue, reservation, fines, circulation policies, barcode/RFID, history, defaulters, bulk ops, visitor tracking, reading room, circulation analytics, member activity, category-wise reports, acquisition/budget, revenue, reservation demand, feedback, annual/custom reports, dashboard, predictive analytics, usage patterns.
- Learning management: course creation and management (syllabus, objectives, prerequisites), module/lesson organization (video, document, presentation, link), assignments (individual/group, deadlines, grading rubrics), quizzes/assessments (MCQ, true/false, short answer, essay, randomization, time limits), enrollment (self/instructor approval, capacity), content delivery (progress tracking, certificates), discussion forums, collaboration tools, content versioning, course templates, integration with student info system, assessment/grading (submission, late penalty, quiz attempts, auto/manual grading, rubrics, grade book, plagiarism detection, peer review, resubmission, appeals, analytics, bulk grading, export, integration with records), collaboration/communication (forums, moderation, notifications, live sessions, study groups, resource sharing, announcements, messaging, collaborative editing, calendar, notification preferences, activity feeds, external tool integration), analytics/reporting (engagement, completion, assessment, content effectiveness, outcomes, instructor analytics, predictive analytics, custom reports, dashboard, comparative analytics, export, institutional integration).
- Content management: website pages (rich text, SEO, hierarchy), menu management (multi-level, external links), content sections (text, image, video, gallery, accordion, tabs, drag-and-drop), media library (upload, organization, alt text), news/articles (categories, featured, workflow), events (calendar, registration, banners), gallery (albums, tagging), SEO (sitemap, meta tags), multi-language prep, approval workflow, versioning/rollback, forms/communications (contact forms, field customization, email/SMS/newsletter templates, subscriber management, feedback, testimonials, FAQ, auto-responders, delivery tracking, bulk tools, analytics, external service integration).
- Admissions portal: admission cycle management (periods, program cycles), online application (multi-step, document upload, payment), status tracking, document verification, test management (scheduling, results), merit list, interview scheduling/feedback, offer management, fee payment, analytics/reporting, bulk processing, calendar, communication automation, integration with student info system.
- Financial management: fee structures (programs, semesters, categories), student fee collection (online, installments, late fees), accounting (ledger, chart of accounts, journal), expense management (budget, approval, vendors), reporting (income, balance, cash flow), tax/compliance, audit trail, multi-currency, year management, payroll/procurement integration, analytics/forecasting.
- Analytics and reporting: actionable insights for all modules, dashboards, custom reports, visitor tracking, reading room allocation, feedback analysis, annual/custom reports, predictive analytics, usage patterns.
- Communication and notification: email, SMS, in-app alerts, bulk messaging, notification history, auto-responders, delivery status tracking.
- Role-based access control and audit logging for all sensitive actions.
- Compliance with data privacy, security, and institutional policies.

Rationale: EMIS will eliminate data silos, reduce manual work, improve transparency, and enable data-driven decision-making for all stakeholders. Every requirement is included to ensure the system fully supports the operational, academic, and strategic needs of a modern college.


/speckit.clarify
The following clarifications are required to ensure all EMIS requirements are fully understood and unambiguous before technical planning:

1. User Roles & Permissions
- What are the specific permissions and actions available to each user role (student, faculty, staff, administrator, management)?
  - Answer: Students can view and update their own records, enroll in courses, submit assignments, and access learning resources. Faculty can manage courses, grade students, manage attendance, and access relevant reports. Staff can manage administrative records, process admissions, and handle library/finance operations as per their department. Administrators have full access to all modules, user management, and system settings. Management can view analytics, reports, and high-level dashboards but cannot modify operational data.
- Are there any sub-roles or role hierarchies (e.g., department heads, super-admins)?
  - Answer: Yes, department heads (faculty/staff) have additional permissions to manage department-specific data and approve requests. Super-admins have unrestricted access for system configuration and audit.

2. Student Lifecycle Management
- What are the required data fields for each stage (admission, enrollment, academic records, etc.)?
  - Answer: Admission: personal info, contact, previous education, documents, application status. Enrollment: program, batch, semester, fee status. Academic records: grades, attendance, disciplinary actions, achievements. Alumni: contact, employment, engagement status.
- Are there any special workflows for transfers, alumni tracking, or re-admission?
  - Answer: Yes, transfer requests require approval and record migration. Alumni tracking includes periodic engagement and event invitations. Re-admission follows a simplified application and approval process.

3. Faculty & Staff Management
- What payroll rules, leave types, and performance review criteria are required?
  - Answer: Payroll supports monthly, contract, and hourly payments. Leave types: casual, sick, earned, maternity/paternity, special. Performance reviews use customizable criteria (teaching, research, service, punctuality).
- Should the system support contract/part-time staff, or only full-time?
  - Answer: Both contract/part-time and full-time staff are supported, with configurable roles and payroll.

4. Library Management
- What circulation policies (borrowing limits, overdue rules) are required for different user types?
  - Answer: Borrowing limits and overdue fines are configurable by user type (student, faculty, staff, alumni). Default: students (3 books, 14 days), faculty (10 books, 30 days), staff (5 books, 21 days), alumni (2 books, 14 days).
- Should the system support digital resource licensing and access control?
  - Answer: Yes, digital resource licensing and access control are supported, including IP-based and user-based restrictions.

5. Learning Management
- What content types and assessment formats must be supported (video, quiz, assignment, etc.)?
  - Answer: Supported content types: video, audio, document, presentation, link, SCORM. Assessments: quizzes (MCQ, true/false, short/long answer), assignments (file/text), peer review, group work.
- Are there any integrations required with external learning tools or content providers?
  - Answer: Integration with common video conferencing (Zoom, Teams), plagiarism detection (Turnitin), and content repositories (YouTube, Google Drive) is required.

6. Content Management
- What approval workflows are required for publishing website content?
  - Answer: Two-step approval: content creator submits, editor reviews/approves before publishing. Emergency bypass for admins.
- Should the CMS support multi-language content from the start, or is this future scope?
  - Answer: Multi-language support is required from the start for key pages; full content translation can be phased in.

7. Admissions Portal
- What are the required steps and data fields for the online application process?
  - Answer: Steps: registration, personal info, academic history, document upload, fee payment, review/submit. Data: name, DOB, contact, address, previous education, program applied, supporting documents.
- Are there any specific payment gateways or document verification services to integrate?
  - Answer: Integration with at least two payment gateways (Razorpay, PayU) and document verification via DigiLocker API is required.

8. Financial Management
- What accounting standards or compliance requirements must be followed?
  - Answer: Indian Accounting Standards (Ind AS) and UGC/AICTE reporting guidelines must be followed.
- Are there any specific reporting formats or export requirements?
  - Answer: Reports must be exportable in PDF, Excel, and CSV. Standard formats for income statement, balance sheet, and cash flow are required.

9. Analytics & Reporting
- What are the key metrics and dashboards required for each module?
  - Answer: Key metrics: student performance, attendance, fee collection, library usage, HR stats, admissions funnel, placement rates. Dashboards for each module and a consolidated management dashboard are required.
- Should the system support custom report creation by end users?
  - Answer: Yes, end users (with permission) can create and save custom reports using a drag-and-drop report builder.

10. Communication & Notification
- What channels (email, SMS, in-app) are mandatory, and are there volume/bulk requirements?
  - Answer: Email and in-app notifications are mandatory; SMS is optional but supported. Bulk messaging for announcements and alerts is required.
- Are there any compliance or opt-in/opt-out requirements for notifications?
  - Answer: Yes, users must be able to opt-in/opt-out of non-essential notifications. All communication must comply with local data privacy laws.

11. Data Privacy & Compliance
- What data retention, deletion, and audit requirements must be enforced?
  - Answer: Data retention: 7 years for academic/financial records, 1 year for logs. Deletion: user-initiated (where allowed) and admin-initiated with audit trail. All changes/actions must be auditable.
- Are there any specific regional or institutional compliance standards (e.g., GDPR, FERPA)?
  - Answer: Yes, GDPR and Indian IT Act compliance are required. FERPA is not mandatory unless serving US students.


# Free-form Refinement

- For each sample project or project that you create, there should be a variable number of tasks between 5 and 15 tasks for each one, randomly distributed into different states of completion. Make sure that there's at least one task in each stage of completion.

Read the review and acceptance checklist, and check off each item in the checklist if the feature spec meets the criteria. Leave it empty if it does not.


/speckit.plan
The EMIS will be implemented as a full-stack application with:
- **Backend**: Python 3.11+, FastAPI for REST API, PostgreSQL 15+ as primary database, async SQLAlchemy ORM, Redis for caching and background job queues, Celery for distributed task processing
- **Frontend**: Streamlit for web UI, providing role-based interfaces for all user types (students, faculty, staff, administrators, management)
- **Infrastructure**: Docker for containerization, Docker Compose for orchestration, optional Terraform for cloud deployment
- **Quality**: Fully test-driven (pytest), CI/CD pipelines (GitHub Actions), comprehensive test coverage (unit, integration, E2E)
- **Documentation**: OpenAPI/Swagger for API docs, user guides for each role, technical documentation for deployment and maintenance

**Architecture & Core Principles:**
- **Backend**: Modular monolith with clear separation of core, domain, infrastructure, and API layers
- **Frontend**: Component-based Streamlit application with reusable UI components, service layer for API integration, and role-based navigation
- Each domain module (auth, students, attendance, HR, library, LMS, CMS, accounts, analytics, notifications) is independently testable and observable
- Contract-first and test-driven development enforced for all modules (backend and frontend)
- All business logic in backend domain layer; API layer is thin and stateless; frontend is purely presentational
- CLI for admin/devops operations (manage users, migrations, jobs, etc.)
- RBAC enforced at both backend (source of truth) and frontend (UI visibility)
- Audit logging for all sensitive actions
- GDPR and Indian IT Act compliance enforced at all layers


**Module-Level Implementation:**

**Backend Modules:**
- **Auth:** User, Role, Permission models; RBAC middleware; login, registration, password reset, 2FA, audit logs
- **Students:** Student, Enrollment, AcademicRecord, Attendance models; lifecycle workflows; alumni tracking
- **HR:** Employee, Payroll, Leave, PerformanceReview, Recruitment models; payroll rules engine; leave approval workflows
- **Library:** Book, Member, Issue, Reservation, Fine, DigitalResource models; circulation policies; barcode/RFID integration; analytics
- **LMS:** Course, Module, Lesson, Assignment, Quiz, Submission models; content delivery; assessment engine; plagiarism detection; video conferencing integration
- **CMS:** Page, Menu, Media, News, Event, Gallery models; approval workflows; multi-language content; SEO tools
- **Admissions:** Application, Document, Fee, Test, Interview models; multi-step wizard; payment gateway integration; merit list automation
- **Accounts:** FeeStructure, Payment, Expense, Budget, JournalEntry models; double-entry accounting; UGC/AICTE reporting
- **Analytics:** Aggregation services for all modules; custom report builder; predictive analytics (scikit-learn, pandas)
- **Notifications:** Email, SMS, in-app notification services; opt-in/opt-out management; bulk messaging

**Frontend Modules (Streamlit):**
- **Authentication:** Login, registration, password reset, 2FA setup, session management; JWT token handling
- **Student Portal:** Dashboard, profile management, courses, assignments, exams, attendance, fees, library, hostel, transport, placement
- **Faculty Portal:** Dashboard, my courses, attendance marking, assignments, grading, exams, timetable, leave management
- **Administrative:** Admissions processing, student/employee management, library, hostel, transport, inventory, events
- **Finance:** Fee management, payments, billing, expenses, accounting, payroll, budget, financial reports
- **Analytics:** Executive dashboard, module-specific analytics, custom report builder, scheduled reports
- **LMS:** Course viewer, video player, assignments, quizzes, discussions, gradebook, certificates; instructor tools
- **CMS:** Page editor, menu management, news, events, gallery, media library, forms, SEO settings
- **Notifications:** Inbox, compose messages, announcements, templates, preferences, delivery tracking
- **System Admin:** User management, roles & permissions, system settings, audit logs, monitoring, backup/restore

**Component Architecture:**
- **Reusable Components:** Sidebar navigation, header, footer, charts, tables, forms, widgets, modals, breadcrumbs
- **Services Layer:** API client wrapper, auth service, student service, faculty service, admin service, finance service, analytics service
- **Utilities:** Authentication, session management, validators, formatters, file handlers, date/time helpers, notifications
- **State Management:** Streamlit session state for user data, tokens, preferences, and application state

**DevOps & Operations:**
- **Backend**: Docker Compose for local development; Dockerfiles for backend services
- **Frontend**: Dockerfile for Streamlit app; nginx reverse proxy configuration
- **CI/CD**: GitHub Actions for lint, test, build, deploy (separate workflows for backend and frontend)
- **Environment**: .env files and secrets manager for configuration (backend and frontend)
- **Infrastructure**: Optional Terraform for cloud deployment (AWS/GCP/Azure modules)
- **Database**: Automated migrations (Alembic) and seed scripts
- **Monitoring**: Centralized logging and monitoring (Prometheus, Grafana, Sentry) for both backend and frontend
- **Deployment**: Systemd service files, deployment scripts, backup automation

**Testing & Quality:**
- **Backend**: pytest for all unit, integration, and end-to-end tests; 100% test coverage goal for core business logic
- **Frontend**: pytest for utility and service tests; integration tests for API calls; E2E tests for critical user journeys
- **Contract Testing**: OpenAPI schema validation for all API endpoints
- **Code Quality**: Linting (flake8, black, isort) and type checking (mypy) enforced in CI for both backend and frontend
- **Accessibility**: Manual and automated accessibility testing (WCAG 2.1 Level AA compliance)
- **Performance**: Load testing for backend APIs; frontend performance monitoring
- **Security**: Vulnerability scanning; dependency updates; security audit logging

**Security & Compliance:**
- End-to-end encryption (HTTPS, TLS for all services).
- Data encryption at rest (Postgres, file storage).
- Full audit logging for all sensitive actions.
- Data retention, deletion, and export tools for compliance.
- Regular vulnerability scanning and dependency updates.

**Documentation:**
- **API Documentation**: Auto-generated API docs (Swagger/OpenAPI) for all backend endpoints
- **User Manuals**: Role-specific user guides (student, faculty, admin, finance, system admin) with screenshots
- **Technical Documentation**: Setup guides, deployment guides, API integration guides, component library docs
- **Code Documentation**: Comprehensive docstrings for all modules, services, and utilities
- **Onboarding**: Quick start guides, video tutorials, FAQs
- **Static Site**: Documentation hosted on static site (MkDocs or similar)
- Architecture decision records (ADR) and change logs.

This plan ensures a robust, scalable, and maintainable EMIS platform that meets all functional, technical, and compliance requirements.

# additional 
Now I want you to go and audit the implementation plan and the implementation detail files.
Read through it with an eye on determining whether or not there is a sequence of tasks that you need
to be doing that are obvious from reading this. Because I don't know if there's enough here. For example,
when I look at the core implementation, it would be useful to reference the appropriate places in the implementation
details where it can find the information as it walks through each step in the core implementation or in the refinement.

/speckit.analyze
Analyzed the EMIS specification for inconsistencies, gaps, and alignment with constitution principles. Key findings: All requirements align with security, modularity, test-first, simplicity, observability, maintainability, and compliance principles. No major inconsistencies detected. Coverage: 100% of specified features mapped to implementation tasks. Gaps identified: Detailed API contracts, error handling specifications, and integration testing requirements need further definition before implementation.

/speckit.checklist
Generated requirements quality checklists to validate API and security requirements before implementation. Checklists serve as "unit tests for English" to ensure requirements are complete, clear, consistent, and testable. Focus areas: requirement completeness, clarity, consistency, acceptance criteria quality, scenario coverage, edge cases, non-functional requirements, dependencies, assumptions, ambiguities, and conflicts. Files: specs/001-emis-core/checklists/api.md (45 items), specs/001-emis-core/checklists/security.md (50 items).

# break down tasks
/speckit.tasks

/speckit.implement
This command will be executed by the AI agent to implement the tasks defined in `/speckit.tasks`. No further content is needed here.