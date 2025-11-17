# Implementation Tasks: EMIS Core Platform

**Feature**: EMIS Core Platform  
**Created**: 2025-11-16  
**Status**: Ready for Implementation  
**Tech Stack**: Python 3.11+, Django 4.2+, Django REST Framework, PostgreSQL 15+, Django ORM, Redis, Celery

---

## Overview

This document provides a complete, dependency-ordered task breakdown organized by user story. Each user story represents an independently testable feature increment. After completing the Setup and Foundational phases, user stories can be implemented in parallel by different developers.

### Execution Strategy

1. **Setup Phase** → Complete project initialization
2. **Foundational Phase** → MUST complete before ANY user story (authentication, database, error handling)
3. **User Story Phases** → Implement in priority order (P1 → P2 → P3 → P4 → P5)
4. **Polish Phase** → Cross-cutting concerns affecting multiple stories

### MVP Scope 🎯

**Minimum Viable Product = User Story 1 (Secure Access & Role Control)**

After completing Setup + Foundational + US1, you have a functional authentication system with RBAC that can be demonstrated and tested independently.

---

## Phase 1: Setup & Project Initialization

**Goal**: Establish project structure, dependencies, and development environment.

- [x] T001 Create Django project structure following plan.md architecture (apps/, config/, tests/) ✅
- [x] T002 Initialize requirements.txt with Python 3.11+ and core dependencies (Django, Django REST Framework, psycopg2, pytest) ✅
- [x] T003 [P] Configure linting tools (flake8, black, isort) in pyproject.toml ✅
- [x] T004 [P] Configure type checking with mypy in pyproject.toml ✅
- [x] T005 [P] Create .env.example file with required environment variables (DATABASE_URL, REDIS_URL, SECRET_KEY) ✅
- [x] T006 [P] Create docker-compose.yml for PostgreSQL 15+ and Redis services ✅
- [x] T007 Create config/settings.py for centralized configuration management ✅
- [x] T008 [P] Setup pytest.ini with test discovery and coverage configuration ✅
- [x] T009 [P] Create GitHub Actions workflow for CI/CD in .github/workflows/ci.yml ✅
- [x] T010 [P] Create README.md with setup instructions and architecture overview ✅
- [x] T011 Initialize Django migrations for all apps ✅
- [x] T012 Create apps/core/__init__.py for shared utilities module ✅

---

## Phase 2: Foundational Infrastructure (MUST complete before user stories)

**Goal**: Build blocking prerequisites required by ALL user stories.

**Independent Test**: Can verify database connection, create test users, and validate error response format.

### Database Foundation

- [x] T020 Create apps/core/database.py with Django database configuration and connection utilities ✅
- [x] T021 Create apps/core/models/base.py with BaseModel including id, created_at, updated_at fields ✅
- [x] T022 [P] Create Django migration for base models ✅

### Error Handling Framework

- [x] T023 Create apps/core/exceptions.py with base EMISException and MODULE_ERROR_CODE support ✅
- [x] T024 Create apps/core/error_codes.py with error code registry (AUTH_001-099, ADMISSIONS_101-199, etc.) ✅
- [x] T025 Create apps/core/middleware/error_handler.py to format all errors with code, message, correlation_id ✅
- [x] T026 [P] Write unit tests for error handler in tests/core/test_error_handler.py ✅

### Authentication & Authorization Framework

- [x] T027 Create apps/authentication/models/user.py with User model (email, hashed_password, status, roles) ✅
- [x] T028 Create apps/authentication/models/role.py with Role model (name, description, permissions) ✅
- [x] T029 Create apps/authentication/models/permission.py with Permission model (resource_group, action) ✅
- [x] T030 Create apps/authentication/models/resource_group.py with ResourceGroup model ✅
- [x] T031 Create apps/authentication/models/audit_log.py with AuditLog model (actor, action, target, timestamp, outcome) ✅
- [x] T032 Create Django migration for authentication models ✅
- [x] T033 Create apps/authentication/security.py with password hashing utilities (bcrypt) ✅
- [x] T034 Create apps/authentication/jwt.py with JWT token generation and validation ✅
- [x] T035 Create apps/core/middleware/auth.py with JWT authentication dependency ✅
- [x] T036 Create apps/core/middleware/rbac.py with permission checking decorator ✅
- [x] T037 Create apps/core/middleware/audit.py with audit logging decorator ✅

### API Infrastructure

- [x] T038 Create apps/core/serializers/base.py with base DRF serializers ✅
- [x] T039 Create apps/core/serializers/error.py with ErrorResponse serializer (code, message, correlation_id) ✅
- [x] T040 Create apps/core/serializers/pagination.py with PaginatedResponse serializer ✅
- [x] T041 Create config/urls.py with Django URL routing and app registration ✅
- [x] T042 [P] Create apps/core/utils/correlation.py for correlation ID generation ✅

### Caching & Background Jobs Setup

- [x] T043 Create apps/core/cache.py with Redis client initialization ✅
- [x] T044 Create apps/core/tasks/__init__.py for Celery app configuration ✅
- [x] T045 [P] Create docker configuration for Celery worker in docker-compose.yml ✅

---

## Phase 3: User Story 1 - Secure Access & Role Control (Priority: P1) 🎯 MVP

**Goal**: Users can authenticate and access only features permitted by their role, with all sensitive actions audit logged.

**Why this priority**: Without secure access and role enforcement, no other module can safely operate.

**Independent Test**: Create users for each role, authenticate, verify permitted/denied actions are enforced and audit events recorded.

**Acceptance Criteria**:
- Valid student login completes in <3 seconds with audit log entry (SC-001)
- Role permission changes propagate to next request (SC-006)
- All error responses include MODULE_ERROR_CODE (SC-007)

### Domain Layer for US1

- [x] T050 [P] [US1] Create apps/authentication/serializers/user.py with UserCreate, UserResponse, UserLogin serializers ✅
- [x] T051 [P] [US1] Create apps/authentication/serializers/role.py with RoleCreate, RoleResponse serializers ✅
- [x] T052 [P] [US1] Create apps/authentication/serializers/permission.py with PermissionCreate, PermissionResponse serializers ✅
- [x] T053 [US1] Create apps/authentication/services/auth_service.py with register, login, logout methods ✅
- [x] T054 [US1] Create apps/authentication/services/user_service.py with CRUD operations for users ✅
- [x] T055 [US1] Create apps/authentication/services/role_service.py with role and permission management ✅
- [x] T056 [US1] Create apps/authentication/services/audit_service.py with audit log creation and querying ✅

### API Layer for US1

- [x] T057 [US1] Create apps/authentication/api/auth.py with POST /auth/register endpoint ✅
- [x] T058 [US1] Implement POST /auth/login endpoint in apps/authentication/api/auth.py ✅
- [x] T059 [US1] Implement POST /auth/logout endpoint in apps/authentication/api/auth.py ✅
- [x] T060 [US1] Implement POST /auth/refresh endpoint for token refresh in apps/authentication/api/auth.py ✅
- [x] T061 [US1] Create apps/authentication/api/users.py with GET /users/ endpoint (paginated, filterable) ✅
- [x] T062 [US1] Implement GET /users/{user_id} endpoint in apps/authentication/api/users.py ✅
- [x] T063 [US1] Implement PUT /users/{user_id} endpoint in apps/authentication/api/users.py ✅
- [x] T064 [US1] Implement DELETE /users/{user_id} endpoint in apps/authentication/api/users.py ✅
- [x] T065 [US1] Create apps/authentication/api/roles.py with role CRUD endpoints ✅
- [x] T066 [US1] Create apps/authentication/api/permissions.py with permission assignment endpoints ✅
- [x] T067 [US1] Create apps/authentication/api/audit.py with GET /audit-logs/ endpoint (admin only) ✅

### Testing for US1

- [x] T068 [P] [US1] Write integration test for registration flow in tests/authentication/test_auth_flow.py ✅
- [x] T069 [P] [US1] Write integration test for login flow with audit logging in tests/authentication/test_auth_flow.py ✅
- [x] T070 [P] [US1] Write test for RBAC enforcement (faculty denied access to admin endpoint) in tests/authentication/test_rbac.py ✅
- [x] T071 [P] [US1] Write test for role permission change propagation in tests/authentication/test_rbac.py ✅
- [x] T072 [P] [US1] Write test for audit log creation on sensitive actions in tests/authentication/test_audit.py ✅
- [x] T073 [P] [US1] Write test for session auto-extension during operations in tests/authentication/test_session.py (N/A for JWT)
- [x] T074 [P] [US1] Write edge case test for simultaneous role permission change in tests/authentication/test_edge_cases.py ✅

### Data Seeding for US1

- [x] T075 [US1] Create apps/authentication/fixtures/seed_roles.py to create default roles (Student, Faculty, Staff, Admin, Management) ✅
- [x] T076 [US1] Create apps/authentication/fixtures/seed_permissions.py to create resource groups and permissions ✅
- [x] T077 [US1] Create management command to seed authentication data: python manage.py seed-auth ✅

---

## Phase 4: User Story 2 - Admissions Lifecycle (Priority: P2)

**Goal**: Applicants submit applications, staff review documents, generate merit lists, and enroll accepted students.

**Why this priority**: Establishes the initial population of students—critical for downstream academic and financial processes.

**Independent Test**: Simulate application submission → document verification → merit list generation → enrollment; verify each state transition and final student record creation.

**Acceptance Criteria**:
- Admissions staff can process an application in <2 minutes average (SC-002)
- Merit list generation is idempotent with versioning support

**Dependencies**: Requires US1 (authentication) to be complete.

### Models for US2

- [x] T100 [P] [US2] Create apps/admissions/models/application.py with Application model (applicant_data, documents, status, submitted_at) ✅
- [x] T101 [P] [US2] Create apps/admissions/models/merit_list.py with MeritList model (generation_timestamp, criteria, ranked_applications) ✅
- [x] T102 [P] [US2] Create apps/students/models/student.py with Student model extending User ✅
- [x] T103 [P] [US2] Create apps/students/models/enrollment.py with Enrollment model (student, program, batch, status, start_date) ✅
- [x] T104 [US2] Create Django migration for admissions and students models ✅

### Domain Layer for US2

- [x] T105 [P] [US2] Create apps/admissions/serializers/application.py with ApplicationCreate, ApplicationUpdate, ApplicationResponse serializers ✅
- [x] T106 [P] [US2] Create apps/admissions/serializers/merit_list.py with MeritListCreate, MeritListResponse serializers ✅
- [x] T107 [P] [US2] Create apps/students/serializers/enrollment.py with EnrollmentCreate, EnrollmentResponse serializers ✅
- [x] T108 [US2] Create apps/admissions/services/application_service.py with submit, validate, update_status methods ✅
- [x] T109 [US2] Create apps/admissions/services/merit_list_service.py with generate_merit_list, rank_applications methods ✅
- [x] T110 [US2] Create apps/admissions/services/enrollment_service.py with create_enrollment_from_application method ✅
- [x] T111 [US2] Implement application status state machine in apps/admissions/services/application_service.py ✅

### API Layer for US2
  ✅
- [x] T112 [US2] Create apps/admissions/api/applications.py with POST /applications/ endpoint  ✅
- [x] T113 [US2] Implement GET /applications/ endpoint (paginated, filtered by status) in apps/admissions/api/applications.py  ✅
- [x] T114 [US2] Implement GET /applications/{application_id} endpoint in apps/admissions/api/applications.py  ✅
- [x] T115 [US2] Implement PATCH /applications/{application_id}/status endpoint in apps/admissions/api/applications.py  ✅
- [x] T116 [US2] Create apps/admissions/api/merit_lists.py with POST /merit-lists/ endpoint  ✅
- [x] T117 [US2] Implement GET /merit-lists/ endpoint in apps/admissions/api/merit_lists.py  ✅
- [x] T118 [US2] Implement GET /merit-lists/{merit_list_id} endpoint in apps/admissions/api/merit_lists.py  ✅
- [x] T119 [US2] Create apps/students/api/enrollments.py with POST /enrollments/ endpoint  ✅
- [x] T120 [US2] Implement GET /enrollments/ endpoint in apps/students/api/enrollments.py  ✅
  ✅
### Testing for US2

- [x] T121 [P] [US2] Write integration test for application submission with validation in tests/admissions/test_application_flow.py ✅
- [x] T122 [P] [US2] Write integration test for application status transitions in tests/admissions/test_application_flow.py ✅
- [x] T123 [P] [US2] Write integration test for merit list generation in tests/admissions/test_merit_list.py ✅
- [x] T124 [P] [US2] Write integration test for enrollment creation from accepted application in tests/admissions/test_enrollment.py ✅
- [x] T125 [P] [US2] Write edge case test for application missing required document in tests/admissions/test_edge_cases.py ✅
- [x] T126 [P] [US2] Write edge case test for multiple merit list generations (idempotency) in tests/admissions/test_edge_cases.py ✅
- [x] T127 [P] [US2] Write edge case test for duplicate admission applications in tests/admissions/test_edge_cases.py ✅

---

## Phase 5: User Story 3 - Course Delivery & Assessment (Priority: P3)

**Goal**: Faculty create courses and publish modular learning content; students access lessons, submit assignments, and view grades.

**Why this priority**: Enables academic progression and instructional delivery once students exist.

**Independent Test**: Create a course with modules and assignments; have a student enroll, access content, submit assignment, and receive a grade.

**Acceptance Criteria**:
- 90% of assignment submissions acknowledged in <5 seconds (SC-003)
- Transcript generation accuracy = 100% in audit samples (SC-010)
- Prerequisite validation before course enrollment (FR-015)

**Dependencies**: Requires US1 (authentication) and US2 (student enrollment) to be complete.

### Models for US3

- [x] T150 [P] [US3] Create apps/courses/models/course.py with Course model (title, syllabus, prerequisites, status, created_by)
- [x] T151 [P] [US3] Create apps/courses/models/module.py with Module model (course, title, sequence_order, content)
- [x] T152 [P] [US3] Create apps/courses/models/assignment.py with Assignment model (course, title, due_date, grading_rubric)
- [x] T153 [P] [US3] Create apps/courses/models/submission.py with Submission model (assignment, student, timestamp, grade_status, files)
- [x] T154 [P] [US3] Create apps/courses/models/grade_record.py with GradeRecord model (course, student, grade_value, finalized)
- [x] T155 [P] [US3] Create apps/students/models/attendance.py with AttendanceRecord model (student, course, session_date, status)
- [x] T156 [P] [US3] Create apps/students/models/transcript.py with Transcript model (student, grade_records_snapshot, generated_at)
- [x] T157 [US3] Create Django migration for courses and grading models

### Domain Layer for US3

- [x] T158 [P] [US3] Create apps/courses/serializers/course.py with CourseCreate, CourseUpdate, CourseResponse serializers
- [x] T159 [P] [US3] Create apps/courses/serializers/module.py with ModuleCreate, ModuleResponse serializers
- [x] T160 [P] [US3] Create apps/courses/serializers/assignment.py with AssignmentCreate, AssignmentResponse serializers
- [x] T161 [P] [US3] Create apps/courses/serializers/submission.py with SubmissionCreate, SubmissionResponse serializers
- [x] T162 [P] [US3] Create apps/courses/serializers/grade.py with GradeRecordCreate, GradeRecordResponse serializers
- [x] T163 [US3] Create apps/courses/services/course_service.py with CRUD operations and prerequisite validation
- [x] T164 [US3] Create apps/courses/services/module_service.py with module management operations
- [x] T165 [US3] Create apps/courses/services/assignment_service.py with assignment creation and deadline enforcement
- [x] T166 [US3] Create apps/courses/services/submission_service.py with submission handling and late flag detection
- [x] T167 [US3] Create apps/courses/services/grading_service.py with grade calculation and finalization
- [x] T168 [US3] Create apps/students/services/transcript_service.py with transcript generation (only finalized grades)

### API Layer for US3

- [x] T169 [US3] Create apps/courses/api/courses.py with POST /courses/ endpoint
- [x] T170 [US3] Implement GET /courses/ endpoint (paginated, searchable) in apps/courses/api/courses.py
- [x] T171 [US3] Implement GET /courses/{course_id} endpoint in apps/courses/api/courses.py
- [x] T172 [US3] Implement PUT /courses/{course_id} endpoint in apps/courses/api/courses.py
- [x] T173 [US3] Implement POST /courses/{course_id}/modules endpoint in apps/courses/api/courses.py
- [x] T174 [US3] Create apps/courses/api/assignments.py with POST /assignments/ endpoint
- [x] T175 [US3] Implement GET /assignments/ endpoint (filtered by course) in apps/courses/api/assignments.py
- [x] T176 [US3] Create apps/courses/api/submissions.py with POST /submissions/ endpoint
- [x] T177 [US3] Implement GET /submissions/ endpoint (filtered by assignment/student) in apps/courses/api/submissions.py
- [x] T178 [US3] Create apps/courses/api/grades.py with POST /grades/ endpoint (faculty only)
- [x] T179 [US3] Implement GET /grades/ endpoint (filtered by course/student) in apps/courses/api/grades.py
- [x] T180 [US3] Create apps/students/api/transcripts.py with GET /transcripts/{student_id} endpoint

### Testing for US3

- [x] T181 [P] [US3] Write integration test for course creation with prerequisites in tests/courses/test_course_flow.py
- [x] T182 [P] [US3] Write integration test for assignment submission with timestamp in tests/courses/test_submission_flow.py
- [x] T183 [P] [US3] Write integration test for grading workflow in tests/courses/test_grading_flow.py
- [x] T184 [P] [US3] Write integration test for transcript generation in tests/students/test_transcript.py
- [x] T185 [P] [US3] Write test for prerequisite validation before enrollment in tests/courses/test_prerequisites.py
- [x] T186 [P] [US3] Write edge case test for assignment submission one second past deadline in tests/courses/test_edge_cases.py
- [x] T187 [P] [US3] Write edge case test for transcript request with incomplete grades in tests/courses/test_edge_cases.py
- [x] T188 [P] [US3] Write edge case test for deleted course content access in tests/courses/test_edge_cases.py
- [x] T189 [P] [US3] Write edge case test for course withdrawal impact on grades in tests/courses/test_edge_cases.py

---

## Phase 6: User Story 4 - Fee Collection & Financial Tracking (Priority: P4)

**Goal**: Finance staff configure fee structures, record student payments (including installments and late fees), and view fee collection summaries.

**Why this priority**: Financial processing underpins operational sustainability and must follow compliance rules.

**Independent Test**: Define a fee structure, apply to an enrolled student, record payment (including late scenario), and export a summary report.

**Acceptance Criteria**:
- Fee collection report for 1,000 students generates in <10 seconds (SC-004)
- Late fee calculation is accurate for all payment scenarios
- Partial payment tracking with remaining balance is correct

**Dependencies**: Requires US1 (authentication) and US2 (student enrollment) to be complete.

### Models for US4

- [x] T200 [P] [US4] Create apps/finance/models/fee_structure.py with FeeStructure model (program, components, installment_rules, late_fee_policy)
- [x] T201 [P] [US4] Create apps/finance/models/invoice.py with Invoice model (student, fee_components, amount_due, due_date, status)
- [x] T202 [P] [US4] Create apps/finance/models/payment.py with Payment model (invoice, amount_paid, timestamp, method, late_fee_applied)
- [x] T203 [US4] Create Django migration for finance models

### Domain Layer for US4

- [x] T204 [P] [US4] Create apps/finance/serializers/fee_structure.py with FeeStructureCreate, FeeStructureResponse serializers ✅
- [x] T205 [P] [US4] Create apps/finance/serializers/invoice.py with InvoiceCreate, InvoiceResponse serializers ✅
- [x] T206 [P] [US4] Create apps/finance/serializers/payment.py with PaymentCreate, PaymentResponse serializers ✅
- [x] T207 [US4] Create apps/finance/services/fee_structure_service.py with fee structure management ✅
- [x] T208 [US4] Create apps/finance/services/invoice_service.py with invoice generation and balance tracking ✅
- [x] T209 [US4] Create apps/finance/services/payment_service.py with payment processing and late fee calculation ✅
- [x] T210 [US4] Create apps/finance/services/report_service.py with fee collection summary generation ✅

### API Layer for US4

- [x] T211 [US4] Create apps/finance/api/fee_structures.py with POST /fee-structures/ endpoint ✅
- [x] T212 [US4] Implement GET /fee-structures/ endpoint in apps/finance/api/fee_structures.py ✅
- [x] T213 [US4] Create apps/finance/api/invoices.py with POST /invoices/ endpoint ✅
- [x] T214 [US4] Implement GET /invoices/ endpoint (filtered by student/status) in apps/finance/api/invoices.py ✅
- [x] T215 [US4] Implement GET /invoices/{invoice_id} endpoint in apps/finance/api/invoices.py ✅
- [x] T216 [US4] Create apps/finance/api/payments.py with POST /payments/ endpoint ✅
- [x] T217 [US4] Implement GET /payments/ endpoint (filtered by student/date range) in apps/finance/api/payments.py ✅
- [x] T218 [US4] Create apps/finance/api/reports.py with GET /reports/fee-collection endpoint ✅
- [x] T219 [US4] Implement fee collection report export (PDF, Excel, CSV) in apps/finance/api/reports.py ✅

### Testing for US4

- [x] T220 [P] [US4] Write integration test for fee structure creation in tests/finance/test_fee_structure.py ✅
- [x] T221 [P] [US4] Write integration test for invoice generation in tests/finance/test_invoice_flow.py ✅
- [x] T222 [P] [US4] Write integration test for payment processing with late fee in tests/finance/test_payment_flow.py ✅
- [x] T223 [P] [US4] Write integration test for partial payment handling in tests/finance/test_payment_flow.py ✅
- [x] T224 [P] [US4] Write integration test for fee collection report generation in tests/finance/test_reports.py ✅
- [x] T225 [P] [US4] Write edge case test for fee payment with partial installment and scholarship in tests/finance/test_edge_cases.py ✅
- [x] T226 [P] [US4] Write edge case test for overdue fee payment reversal in tests/finance/test_edge_cases.py ✅

---

## Phase 7: User Story 5 - Management Analytics Dashboard (Priority: P5)

**Goal**: Management users view consolidated metrics (admissions funnel, attendance rates, fee collection status, course completion percentages) on a single dashboard.

**Why this priority**: Enables data-driven oversight and strategic decisions once foundational operations are in place.

**Independent Test**: Populate sample data for each module and load dashboard; verify each metric matches underlying records.

**Acceptance Criteria**:
- Dashboard metrics refresh completes within 60 seconds (SC-005)
- All metrics are accurate vs source data
- Zero-data edge cases display 0 instead of errors

**Dependencies**: Requires US1, US2, US3, US4 to be complete (needs data from all modules).

### Models for US5

- [x] T250 [P] [US5] Create apps/analytics/models/dashboard_metric.py with DashboardMetric model (metric_key, computed_value, last_refreshed)
- [x] T251 [US5] Create Django migration for analytics models

### Domain Layer for US5

- [x] T252 [P] [US5] Create apps/analytics/serializers/dashboard.py with DashboardMetricResponse, DashboardSummary serializers
- [x] T253 [US5] Create apps/analytics/services/admissions_metrics_service.py for admissions funnel calculation
- [x] T254 [US5] Create apps/analytics/services/attendance_metrics_service.py for attendance rate calculation
- [x] T255 [US5] Create apps/analytics/services/fee_metrics_service.py for fee collection calculation
- [x] T256 [US5] Create apps/analytics/services/course_metrics_service.py for course completion calculation
- [x] T257 [US5] Create apps/analytics/services/dashboard_service.py to aggregate all metrics
- [x] T258 [US5] Implement caching strategy for dashboard metrics in apps/analytics/services/dashboard_service.py

### Background Jobs for US5

- [x] T259 [US5] Create apps/analytics/tasks/refresh_dashboard.py Celery task for periodic metric refresh
- [x] T260 [US5] Configure Celery beat schedule for hourly dashboard refresh in config/celery.py

### API Layer for US5

- [x] T261 [US5] Create apps/analytics/api/dashboard.py with GET /dashboard/ endpoint
- [x] T262 [US5] Implement GET /dashboard/admissions endpoint for admissions funnel in apps/analytics/api/dashboard.py
- [x] T263 [US5] Implement GET /dashboard/attendance endpoint for attendance metrics in apps/analytics/api/dashboard.py
- [x] T264 [US5] Implement GET /dashboard/finance endpoint for fee collection in apps/analytics/api/dashboard.py
- [x] T265 [US5] Implement GET /dashboard/courses endpoint for course completion in apps/analytics/api/dashboard.py

### Testing for US5

- [x] T266 [P] [US5] Write integration test for admissions funnel metric accuracy in tests/analytics/test_admissions_metrics.py
- [x] T267 [P] [US5] Write integration test for attendance metric accuracy in tests/analytics/test_attendance_metrics.py
- [x] T268 [P] [US5] Write integration test for fee collection metric accuracy in tests/analytics/test_fee_metrics.py
- [x] T269 [P] [US5] Write integration test for course completion metric accuracy in tests/analytics/test_course_metrics.py
- [x] T270 [P] [US5] Write integration test for dashboard aggregation in tests/analytics/test_dashboard.py
- [x] T271 [P] [US5] Write edge case test for dashboard with zero data in tests/analytics/test_edge_cases.py
- [x] T272 [P] [US5] Write performance test for dashboard refresh time (<60 seconds) in tests/analytics/test_performance.py

---

## Phase 8: Polish & Cross-Cutting Concerns

**Goal**: Implement features that span multiple user stories and enhance overall system quality.

### Search & Pagination

- [x] T300 [P] Implement full-text search for users using PostgreSQL tsvector in apps/authentication/services/user_service.py
- [x] T301 [P] Implement search for courses using PostgreSQL tsvector in apps/courses/services/course_service.py
- [x] T302 [P] Implement search for applications in apps/admissions/services/application_service.py
- [x] T303 Ensure all list endpoints support pagination with offset/limit in apps/core/serializers/pagination.py

### Internationalization (i18n)

- [x] T304 Create apps/core/i18n/ directory for translation infrastructure
- [x] T305 Create apps/core/i18n/en.json with English UI strings
- [x] T306 Implement translation helper in apps/core/i18n/translator.py
- [x] T307 Update all API responses to use translation keys (deferred: actual translations for other languages)

### Performance Optimization

- [x] T308 [P] Add database indexes for frequently queried fields (email, status, created_at) in migrations/
- [x] T309 [P] Implement Redis caching for frequently accessed data (roles, permissions) in apps/core/cache.py
- [x] T310 [P] Add query optimization for dashboard metrics (avoid N+1 queries)
- [x] T311 Configure connection pooling for PostgreSQL in apps/core/database.py

### Monitoring & Observability

- [x] T312 [P] Create apps/core/api/health.py with GET /health endpoint
- [x] T313 [P] Implement GET /readiness endpoint checking database and Redis connectivity in apps/core/api/health.py
- [x] T314 [P] Configure structured logging with correlation IDs in apps/core/logging.py
- [x] T315 [P] Add Prometheus metrics endpoints in apps/core/api/metrics.py

### Security Hardening

- [x] T316 [P] Implement rate limiting for authentication endpoints using Redis
- [x] T317 [P] Add CORS middleware configuration in config/settings.py
- [x] T318 [P] Implement security headers (HSTS, CSP, X-Content-Type-Options) in middleware
- [x] T319 Perform security audit of all endpoints for RBAC coverage

### Documentation

- [x] T320 [P] Generate OpenAPI/Swagger documentation automatically using drf-spectacular
- [x] T321 [P] Create API documentation examples for all endpoints in docs/api/
- [x] T322 [P] Create user guide for authentication and authorization in docs/guides/auth.md
- [x] T323 [P] Create deployment guide in docs/deployment.md
- [x] T324 Update README.md with complete setup and usage instructions

### Testing & Quality Assurance

- [ ] T325 [P] Achieve minimum 80% code coverage across all modules
- [x] T326 [P] Run mypy type checking and fix all type errors
- [x] T327 [P] Run flake8, black, isort and ensure all code passes linting
- [ ] T328 Write end-to-end integration test covering full user journey (register → login → submit application → enroll → submit assignment → pay fees)

---

## Dependencies & Execution Order

### Phase Dependencies

```
Setup (Phase 1)
  ↓
Foundational (Phase 2) ← MUST complete before ANY user story
  ↓
  ├─→ User Story 1 (P1) 🎯 MVP
  ↓
  ├─→ User Story 2 (P2) [depends on US1]
  ↓
  ├─→ User Story 3 (P3) [depends on US1, US2]
  ├─→ User Story 4 (P4) [depends on US1, US2]
  ↓
  └─→ User Story 5 (P5) [depends on US1, US2, US3, US4]
  ↓
Polish (Phase 8) [depends on all user stories]
```

### User Story Completion Order

1. **US1 (P1)**: Complete first - blocks all other stories
2. **US2 (P2)**: Complete second - provides student data for US3 and US4
3. **US3 (P3) & US4 (P4)**: Can be developed in parallel after US2
4. **US5 (P5)**: Complete last - requires data from all previous stories

### Parallel Execution Opportunities

Within **Setup Phase**: T003, T004, T005, T008, T009, T010 can run in parallel

Within **Foundational Phase**: T022, T026, T042, T045 can run in parallel after their dependencies

Within **US1**: T050-T052 (schemas) can run in parallel; T068-T074 (tests) can run in parallel

Within **US2**: T100-T103 (models) can run in parallel; T105-T107 (schemas) can run in parallel; T121-T127 (tests) can run in parallel

Within **US3**: T150-T157 (models) can run in parallel; T158-T162 (schemas) can run in parallel; T181-T189 (tests) can run in parallel

Within **US4**: T200-T202 (models) can run in parallel; T204-T206 (schemas) can run in parallel; T220-T226 (tests) can run in parallel

Within **US5**: T266-T272 (tests) can run in parallel

Within **Polish Phase**: Most tasks marked [P] can run in parallel

---

## Success Criteria Validation

After completing all tasks, validate the following success criteria:

- [ ] **SC-001**: 95% of valid login attempts complete in <3 seconds
- [ ] **SC-002**: Admissions staff can process an application in <2 minutes average
- [ ] **SC-003**: 90% of assignment submissions acknowledged in <5 seconds
- [ ] **SC-004**: Fee collection report for 1,000 students generates in <10 seconds
- [ ] **SC-005**: Dashboard metrics refresh completes within 60 seconds
- [ ] **SC-006**: Role permission change propagates to next request
- [ ] **SC-007**: Error responses include MODULE_ERROR_CODE for 100% of failure cases
- [ ] **SC-008**: 95% of users can locate primary dashboard actions without guidance (UX testing)
- [ ] **SC-009**: English UI strings show no missing translation placeholders
- [ ] **SC-010**: Transcript generation accuracy = 100% in audit samples
- [ ] **SC-011**: System maintains stable performance with 5,000 concurrent users (load testing)
- [ ] **SC-012**: Active user sessions auto-extend during operations

---

## Task Summary

- **Total Tasks**: 328
- **Setup Phase**: 12 tasks
- **Foundational Phase**: 26 tasks
- **User Story 1 (P1)**: 28 tasks (MVP)
- **User Story 2 (P2)**: 28 tasks
- **User Story 3 (P3)**: 40 tasks
- **User Story 4 (P4)**: 27 tasks
- **User Story 5 (P5)**: 23 tasks
- **Polish Phase**: 29 tasks
- **Success Criteria Validation**: 12 checks
- **Parallelizable Tasks**: ~120 tasks marked with [P]

### Independent Testing Capability

Each user story can be tested independently after its completion:

- **US1**: Authentication and RBAC system fully functional
- **US2**: Complete admissions-to-enrollment workflow operational
- **US3**: Course creation, assignment submission, and grading functional
- **US4**: Fee structures, invoicing, and payment processing working
- **US5**: Analytics dashboard displaying metrics from all modules

### Incremental Delivery Milestones

- **Milestone 1 (MVP)**: Setup + Foundational + US1 = Functional authentication system
- **Milestone 2**: + US2 = Admissions workflow complete
- **Milestone 3**: + US3 = Academic delivery operational
- **Milestone 4**: + US4 = Financial management functional
- **Milestone 5 (Full Core)**: + US5 = Complete core platform with analytics

---

**Next Steps**: Begin with Phase 1 (Setup) tasks and proceed through phases sequentially. User stories can be distributed across team members after Foundational phase is complete.

