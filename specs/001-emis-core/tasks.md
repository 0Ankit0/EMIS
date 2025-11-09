# Tasks: EMIS Core System

**Input**: Design documents from `/specs/001-emis-core/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: Test tasks included per constitution requirement (Test-First: TDD, contract-first, integration-first)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- All paths are absolute from `/media/ankit/Programming/Projects/python/EMIS/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per plan.md (src/, tests/, cli/, lib/) in /media/ankit/Programming/Projects/python/EMIS/
- [ ] T002 Initialize Python 3.11+ project with pyproject.toml and requirements.txt in /media/ankit/Programming/Projects/python/EMIS/
- [ ] T003 Install core dependencies (FastAPI, async SQLAlchemy, Celery, Redis, Alembic, Pydantic, pytest) in /media/ankit/Programming/Projects/python/EMIS/
- [ ] T004 Configure Docker Compose for PostgreSQL, Redis, Celery in /media/ankit/Programming/Projects/python/EMIS/docker-compose.yml
- [ ] T005 Set up .env file with required environment variables in /media/ankit/Programming/Projects/python/EMIS/.env
- [ ] T006 [P] Initialize GitHub Actions CI/CD pipeline in /media/ankit/Programming/Projects/python/EMIS/.github/workflows/ci.yml
- [ ] T007 [P] Configure linting (flake8, black, isort) and type checking (mypy) in /media/ankit/Programming/Projects/python/EMIS/pyproject.toml

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete
**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T008 Setup PostgreSQL database schema and Alembic migrations framework in /media/ankit/Programming/Projects/python/EMIS/alembic/
- [ ] T009 Define base User, Role, Permission models in /media/ankit/Programming/Projects/python/EMIS/src/models/auth.py
- [ ] T010 [P] Implement RBAC middleware in /media/ankit/Programming/Projects/python/EMIS/src/middleware/rbac.py
- [ ] T011 [P] Setup pytest configuration and test fixtures in /media/ankit/Programming/Projects/python/EMIS/tests/conftest.py
- [ ] T012 [P] Implement centralized logging infrastructure in /media/ankit/Programming/Projects/python/EMIS/src/lib/logging.py
- [ ] T013 [P] Setup FastAPI application factory and routing structure in /media/ankit/Programming/Projects/python/EMIS/src/app.py
- [ ] T014 [P] Configure error handling and exception middleware in /media/ankit/Programming/Projects/python/EMIS/src/middleware/errors.py
- [ ] T015 Implement audit logging infrastructure in /media/ankit/Programming/Projects/python/EMIS/src/lib/audit.py
- [ ] T016 [P] Setup health check endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/health.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Student Lifecycle Management (Priority: P1) 🎯 MVP

**Goal**: Enable students to apply for admission, enroll in courses, track academic records/attendance/progress, and access alumni services

**Independent Test**: Onboard a new student, progress through admission → enrollment → semester completion → graduation → alumni, verify records at each stage

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T017 [P] [US1] Contract test for student admission endpoints in /media/ankit/Programming/Projects/python/EMIS/tests/contract/test_student_admission.py
- [ ] T018 [P] [US1] Contract test for enrollment endpoints in /media/ankit/Programming/Projects/python/EMIS/tests/contract/test_student_enrollment.py
- [ ] T019 [P] [US1] Integration test for complete student lifecycle journey in /media/ankit/Programming/Projects/python/EMIS/tests/integration/test_student_lifecycle.py

### Implementation for User Story 1

- [ ] T020 [P] [US1] Create Student model in /media/ankit/Programming/Projects/python/EMIS/src/models/student.py
- [ ] T021 [P] [US1] Create Enrollment model in /media/ankit/Programming/Projects/python/EMIS/src/models/enrollment.py
- [ ] T022 [P] [US1] Create AcademicRecord model in /media/ankit/Programming/Projects/python/EMIS/src/models/academic_record.py
- [ ] T023 [P] [US1] Create Attendance model in /media/ankit/Programming/Projects/python/EMIS/src/models/attendance.py
- [ ] T024 [US1] Implement StudentService with lifecycle methods in /media/ankit/Programming/Projects/python/EMIS/src/services/student_service.py
- [ ] T025 [US1] Implement admission workflow logic in /media/ankit/Programming/Projects/python/EMIS/src/services/student_workflow.py
- [ ] T026 [US1] Implement enrollment workflow logic in /media/ankit/Programming/Projects/python/EMIS/src/services/student_workflow.py
- [ ] T027 [US1] Implement graduation workflow logic in /media/ankit/Programming/Projects/python/EMIS/src/services/student_workflow.py
- [ ] T028 [US1] Implement alumni tracking logic in /media/ankit/Programming/Projects/python/EMIS/src/services/student_workflow.py
- [ ] T029 [US1] Create student API endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/students.py
- [ ] T030 [US1] Add validation and error handling for student operations in /media/ankit/Programming/Projects/python/EMIS/src/routes/students.py
- [ ] T031 [US1] Add audit logging for student lifecycle events in /media/ankit/Programming/Projects/python/EMIS/src/services/student_service.py
- [ ] T032 [US1] Document student API in /media/ankit/Programming/Projects/python/EMIS/docs/api/students.md

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Faculty & Staff Management (Priority: P2)

**Goal**: Enable faculty/staff to manage HR records, payroll, leave requests, and performance reviews

**Independent Test**: Onboard a new staff member, process payroll cycle, request and approve leave, record performance review

### Tests for User Story 2

- [ ] T033 [P] [US2] Contract test for HR endpoints in /media/ankit/Programming/Projects/python/EMIS/tests/contract/test_hr.py
- [ ] T034 [P] [US2] Contract test for payroll endpoints in /media/ankit/Programming/Projects/python/EMIS/tests/contract/test_payroll.py
- [ ] T035 [P] [US2] Integration test for HR lifecycle journey in /media/ankit/Programming/Projects/python/EMIS/tests/integration/test_hr_lifecycle.py

### Implementation for User Story 2

- [ ] T036 [P] [US2] Create Employee model in /media/ankit/Programming/Projects/python/EMIS/src/models/employee.py
- [ ] T037 [P] [US2] Create Payroll model in /media/ankit/Programming/Projects/python/EMIS/src/models/payroll.py
- [ ] T038 [P] [US2] Create Leave model in /media/ankit/Programming/Projects/python/EMIS/src/models/leave.py
- [ ] T039 [P] [US2] Create PerformanceReview model in /media/ankit/Programming/Projects/python/EMIS/src/models/performance.py
- [ ] T040 [P] [US2] Create Recruitment model in /media/ankit/Programming/Projects/python/EMIS/src/models/recruitment.py
- [ ] T041 [US2] Implement HRService in /media/ankit/Programming/Projects/python/EMIS/src/services/hr_service.py
- [ ] T042 [US2] Implement payroll rules engine in /media/ankit/Programming/Projects/python/EMIS/src/services/payroll_engine.py
- [ ] T043 [US2] Implement leave approval workflow in /media/ankit/Programming/Projects/python/EMIS/src/services/leave_workflow.py
- [ ] T044 [US2] Create HR API endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/hr.py
- [ ] T045 [US2] Add validation and error handling for HR operations in /media/ankit/Programming/Projects/python/EMIS/src/routes/hr.py
- [ ] T046 [US2] Add audit logging for HR events in /media/ankit/Programming/Projects/python/EMIS/src/services/hr_service.py
- [ ] T047 [US2] Document HR API in /media/ankit/Programming/Projects/python/EMIS/docs/api/hr.md

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Library & Learning Management (Priority: P3)

**Goal**: Enable users to search/borrow/return library resources, access digital content, participate in courses, complete assignments and assessments

**Independent Test**: Search and borrow a book, return it late and verify fine, enroll in a course, complete assignment, take quiz, receive grade

### Tests for User Story 3

- [ ] T048 [P] [US3] Contract test for library endpoints in /media/ankit/Programming/Projects/python/EMIS/tests/contract/test_library.py
- [ ] T049 [P] [US3] Contract test for LMS endpoints in /media/ankit/Programming/Projects/python/EMIS/tests/contract/test_lms.py
- [ ] T050 [P] [US3] Integration test for library circulation journey in /media/ankit/Programming/Projects/python/EMIS/tests/integration/test_library_circulation.py
- [ ] T051 [P] [US3] Integration test for course completion journey in /media/ankit/Programming/Projects/python/EMIS/tests/integration/test_course_completion.py

### Implementation for User Story 3

- [ ] T052 [P] [US3] Create Book model in /media/ankit/Programming/Projects/python/EMIS/src/models/book.py
- [ ] T053 [P] [US3] Create LibraryMember model in /media/ankit/Programming/Projects/python/EMIS/src/models/library_member.py
- [ ] T054 [P] [US3] Create Issue, Reservation, Fine models in /media/ankit/Programming/Projects/python/EMIS/src/models/circulation.py
- [ ] T055 [P] [US3] Create DigitalResource model in /media/ankit/Programming/Projects/python/EMIS/src/models/digital_resource.py
- [ ] T056 [P] [US3] Create Course model in /media/ankit/Programming/Projects/python/EMIS/src/models/course.py
- [ ] T057 [P] [US3] Create Module, Lesson models in /media/ankit/Programming/Projects/python/EMIS/src/models/course_content.py
- [ ] T058 [P] [US3] Create Assignment, Quiz, Submission models in /media/ankit/Programming/Projects/python/EMIS/src/models/assessment.py
- [ ] T059 [US3] Implement LibraryService with circulation logic in /media/ankit/Programming/Projects/python/EMIS/src/services/library_service.py
- [ ] T060 [US3] Implement barcode/RFID integration in /media/ankit/Programming/Projects/python/EMIS/src/lib/barcode.py
- [ ] T061 [US3] Implement LMSService with course management in /media/ankit/Programming/Projects/python/EMIS/src/services/lms_service.py
- [ ] T062 [US3] Implement content delivery engine in /media/ankit/Programming/Projects/python/EMIS/src/services/content_delivery.py
- [ ] T063 [US3] Implement assessment/grading engine in /media/ankit/Programming/Projects/python/EMIS/src/services/assessment_engine.py
- [ ] T064 [US3] Integrate plagiarism detection (external API) in /media/ankit/Programming/Projects/python/EMIS/src/lib/plagiarism.py
- [ ] T065 [US3] Integrate video conferencing (Zoom/Teams API) in /media/ankit/Programming/Projects/python/EMIS/src/lib/video_conferencing.py
- [ ] T066 [US3] Create library API endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/library.py
- [ ] T067 [US3] Create LMS API endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/lms.py
- [ ] T068 [US3] Add validation and error handling in /media/ankit/Programming/Projects/python/EMIS/src/routes/library.py and /media/ankit/Programming/Projects/python/EMIS/src/routes/lms.py
- [ ] T069 [US3] Add audit logging for library/LMS events in /media/ankit/Programming/Projects/python/EMIS/src/services/library_service.py and /media/ankit/Programming/Projects/python/EMIS/src/services/lms_service.py
- [ ] T070 [US3] Document library/LMS API in /media/ankit/Programming/Projects/python/EMIS/docs/api/library_lms.md

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - Admissions & Financial Management (Priority: P4)

**Goal**: Enable applicants to complete online applications with document upload and payment, track admission status; enable financial management and reporting

**Independent Test**: Submit application with documents and payment, track status through verification and merit list; record fee payment, generate financial reports

### Tests for User Story 4

- [ ] T071 [P] [US4] Contract test for admissions endpoints in /media/ankit/Programming/Projects/python/EMIS/tests/contract/test_admissions.py
- [ ] T072 [P] [US4] Contract test for financial endpoints in /media/ankit/Programming/Projects/python/EMIS/tests/contract/test_finance.py
- [ ] T073 [P] [US4] Integration test for admission application journey in /media/ankit/Programming/Projects/python/EMIS/tests/integration/test_admission_journey.py
- [ ] T074 [P] [US4] Integration test for fee payment and accounting in /media/ankit/Programming/Projects/python/EMIS/tests/integration/test_financial_flow.py

### Implementation for User Story 4

- [ ] T075 [P] [US4] Create Application model in /media/ankit/Programming/Projects/python/EMIS/src/models/application.py
- [ ] T076 [P] [US4] Create Document model in /media/ankit/Programming/Projects/python/EMIS/src/models/document.py
- [ ] T077 [P] [US4] Create Test, Interview models in /media/ankit/Programming/Projects/python/EMIS/src/models/admission_process.py
- [ ] T078 [P] [US4] Create FeeStructure, Payment models in /media/ankit/Programming/Projects/python/EMIS/src/models/fee.py
- [ ] T079 [P] [US4] Create Expense, Budget, JournalEntry models in /media/ankit/Programming/Projects/python/EMIS/src/models/accounting.py
- [ ] T080 [US4] Implement AdmissionsService in /media/ankit/Programming/Projects/python/EMIS/src/services/admissions_service.py
- [ ] T081 [US4] Implement multi-step application wizard logic in /media/ankit/Programming/Projects/python/EMIS/src/services/application_workflow.py
- [ ] T082 [US4] Integrate payment gateway (Razorpay/PayU) in /media/ankit/Programming/Projects/python/EMIS/src/lib/payment_gateway.py
- [ ] T083 [US4] Integrate document verification (DigiLocker API) in /media/ankit/Programming/Projects/python/EMIS/src/lib/document_verification.py
- [ ] T084 [US4] Implement merit list automation in /media/ankit/Programming/Projects/python/EMIS/src/services/merit_list.py
- [ ] T085 [US4] Implement AccountsService with double-entry accounting in /media/ankit/Programming/Projects/python/EMIS/src/services/accounts_service.py
- [ ] T086 [US4] Implement UGC/AICTE reporting logic in /media/ankit/Programming/Projects/python/EMIS/src/services/compliance_reporting.py
- [ ] T087 [US4] Create admissions API endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/admissions.py
- [ ] T088 [US4] Create finance API endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/finance.py
- [ ] T089 [US4] Add validation and error handling in /media/ankit/Programming/Projects/python/EMIS/src/routes/admissions.py and /media/ankit/Programming/Projects/python/EMIS/src/routes/finance.py
- [ ] T090 [US4] Add audit logging for admissions/finance events in /media/ankit/Programming/Projects/python/EMIS/src/services/admissions_service.py and /media/ankit/Programming/Projects/python/EMIS/src/services/accounts_service.py
- [ ] T091 [US4] Document admissions/finance API in /media/ankit/Programming/Projects/python/EMIS/docs/api/admissions_finance.md

**Checkpoint**: At this point, User Stories 1-4 should all work independently

---

## Phase 7: User Story 5 - Analytics, Reporting & Notifications (Priority: P5)

**Goal**: Enable administrators to view dashboards, generate custom reports, and send notifications to stakeholders

**Independent Test**: Generate custom report with filters, view dashboard with live metrics, send bulk notifications and track delivery

### Tests for User Story 5

- [ ] T092 [P] [US5] Contract test for analytics endpoints in /media/ankit/Programming/Projects/python/EMIS/tests/contract/test_analytics.py
- [ ] T093 [P] [US5] Contract test for notification endpoints in /media/ankit/Programming/Projects/python/EMIS/tests/contract/test_notifications.py
- [ ] T094 [P] [US5] Integration test for report generation in /media/ankit/Programming/Projects/python/EMIS/tests/integration/test_reporting.py

### Implementation for User Story 5

- [ ] T095 [P] [US5] Create Notification model in /media/ankit/Programming/Projects/python/EMIS/src/models/notification.py
- [ ] T096 [P] [US5] Create Report, Dashboard models in /media/ankit/Programming/Projects/python/EMIS/src/models/analytics.py
- [ ] T097 [US5] Implement AnalyticsService with aggregation logic in /media/ankit/Programming/Projects/python/EMIS/src/services/analytics_service.py
- [ ] T098 [US5] Implement custom report builder in /media/ankit/Programming/Projects/python/EMIS/src/services/report_builder.py
- [ ] T099 [US5] Implement predictive analytics (scikit-learn, pandas) in /media/ankit/Programming/Projects/python/EMIS/src/services/predictive_analytics.py
- [ ] T100 [US5] Implement NotificationService (email, SMS, in-app) in /media/ankit/Programming/Projects/python/EMIS/src/services/notification_service.py
- [ ] T101 [US5] Integrate email service (SMTP/SendGrid) in /media/ankit/Programming/Projects/python/EMIS/src/lib/email.py
- [ ] T102 [US5] Integrate SMS service (Twilio/MSG91) in /media/ankit/Programming/Projects/python/EMIS/src/lib/sms.py
- [ ] T103 [US5] Implement opt-in/opt-out management in /media/ankit/Programming/Projects/python/EMIS/src/services/notification_preferences.py
- [ ] T104 [US5] Implement bulk messaging with Celery tasks in /media/ankit/Programming/Projects/python/EMIS/src/tasks/bulk_notifications.py
- [ ] T105 [US5] Create analytics API endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/analytics.py
- [ ] T106 [US5] Create notification API endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/notifications.py
- [ ] T107 [US5] Add validation and error handling in /media/ankit/Programming/Projects/python/EMIS/src/routes/analytics.py and /media/ankit/Programming/Projects/python/EMIS/src/routes/notifications.py
- [ ] T108 [US5] Document analytics/notification API in /media/ankit/Programming/Projects/python/EMIS/docs/api/analytics_notifications.md

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T109 [P] Implement GDPR data export tool in /media/ankit/Programming/Projects/python/EMIS/src/cli/gdpr_export.py
- [ ] T110 [P] Implement GDPR data deletion tool in /media/ankit/Programming/Projects/python/EMIS/src/cli/gdpr_delete.py
- [ ] T111 [P] Implement Indian IT Act compliance checks in /media/ankit/Programming/Projects/python/EMIS/src/lib/compliance.py
- [ ] T112 [P] Setup Prometheus metrics collection in /media/ankit/Programming/Projects/python/EMIS/src/lib/metrics.py
- [ ] T113 [P] Setup Grafana dashboards in /media/ankit/Programming/Projects/python/EMIS/monitoring/grafana/
- [ ] T114 [P] Integrate Sentry for error tracking in /media/ankit/Programming/Projects/python/EMIS/src/lib/sentry.py
- [ ] T115 [P] Create CLI commands for admin operations in /media/ankit/Programming/Projects/python/EMIS/src/cli/
- [ ] T116 [P] Finalize OpenAPI/Swagger documentation in /media/ankit/Programming/Projects/python/EMIS/docs/
- [ ] T117 [P] Create deployment documentation in /media/ankit/Programming/Projects/python/EMIS/docs/deployment.md
- [ ] T118 [P] Create user/admin manuals in /media/ankit/Programming/Projects/python/EMIS/docs/manuals/
- [ ] T119 Code cleanup and refactoring across all modules in /media/ankit/Programming/Projects/python/EMIS/src/
- [ ] T120 Performance optimization and caching strategies in /media/ankit/Programming/Projects/python/EMIS/src/
- [ ] T121 Security hardening and penetration testing across all endpoints
- [ ] T122 Run complete integration test suite and validate all user stories

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4 → P5)
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent of US1
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May reference US1 for student enrollment in courses
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Integrates with US1 for student admissions/fees
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - Aggregates data from all other stories but independently testable

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
# T017, T018, T019 can all be written in parallel

# Launch all models for User Story 1 together:
# T020, T021, T022, T023 can all be created in parallel

# Then implement services sequentially:
# T024-T028 depend on models being complete

# Then implement endpoints:
# T029-T032 depend on services being complete
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T007)
2. Complete Phase 2: Foundational (T008-T016) **CRITICAL - blocks all stories**
3. Complete Phase 3: User Story 1 (T017-T032)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer/Team A: User Story 1 (Student Lifecycle)
   - Developer/Team B: User Story 2 (HR)
   - Developer/Team C: User Story 3 (Library/LMS)
   - Developer/Team D: User Story 4 (Admissions/Finance)
   - Developer/Team E: User Story 5 (Analytics/Notifications)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies - can run in parallel
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (TDD)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- All file paths are absolute from project root
- Constitution principles enforced: security, modularity, test-first, simplicity, observability, maintainability, compliance

---

## Summary

- **Total Tasks**: 122
- **Setup Tasks**: 7 (T001-T007)
- **Foundational Tasks**: 9 (T008-T016)
- **User Story 1 Tasks**: 16 (T017-T032) - MVP scope
- **User Story 2 Tasks**: 15 (T033-T047)
- **User Story 3 Tasks**: 23 (T048-T070)
- **User Story 4 Tasks**: 21 (T071-T091)
- **User Story 5 Tasks**: 17 (T092-T108)
- **Polish Tasks**: 14 (T109-T122)
- **Parallel Opportunities**: 85+ tasks marked [P]
- **Independent Test Criteria**: Each user story phase includes contract and integration tests
- **Suggested MVP Scope**: Phase 1 + Phase 2 + Phase 3 (User Story 1 only) = 32 tasks
