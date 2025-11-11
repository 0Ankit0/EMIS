# Tasks: Academic & Student Core

**Input**: Design documents from `/specs/academic-student-core/`
**Prerequisites**: Foundation setup (database, auth, RBAC)

## Format: `[ID] [P?] [Module] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Module]**: Which module this task belongs to
- All paths are absolute from `/media/ankit/Programming/Projects/python/EMIS/`

---

## Phase 1: Student Information System (SIS)

### Models (Parallel)
- [X] T001 [P] [SIS] Create Student model with personal details in /media/ankit/Programming/Projects/python/EMIS/src/models/student.py
- [X] T002 [P] [SIS] Create StudentContact model for addresses in /media/ankit/Programming/Projects/python/EMIS/src/models/student.py
- [X] T003 [P] [SIS] Create EmergencyContact model in /media/ankit/Programming/Projects/python/EMIS/src/models/student.py

### Services
- [X] T004 [SIS] Implement StudentService with CRUD operations in /media/ankit/Programming/Projects/python/EMIS/src/services/student_service.py
- [X] T005 [SIS] Add student ID generation logic in /media/ankit/Programming/Projects/python/EMIS/src/services/student_service.py
- [X] T006 [SIS] Add document upload handling in /media/ankit/Programming/Projects/python/EMIS/src/services/student_service.py

### API
- [X] T007 [SIS] Create student CRUD endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/students.py
- [X] T008 [SIS] Add validation and error handling in /media/ankit/Programming/Projects/python/EMIS/src/routes/students.py
- [X] T009 [SIS] Document student API in /media/ankit/Programming/Projects/python/EMIS/docs/api/students.md

---

## Phase 2: Admissions & Enrollment

### Models (Parallel)
- [X] T010 [P] [ADM] Create Application model in /media/ankit/Programming/Projects/python/EMIS/src/models/application.py
- [X] T011 [P] [ADM] Create Document model for uploads in /media/ankit/Programming/Projects/python/EMIS/src/models/document.py
- [X] T012 [P] [ADM] Create Test and Interview models in /media/ankit/Programming/Projects/python/EMIS/src/models/admission_process.py
- [X] T013 [P] [ADM] Create Enrollment model in /media/ankit/Programming/Projects/python/EMIS/src/models/enrollment.py

### Services
- [X] T014 [ADM] Implement AdmissionsService in /media/ankit/Programming/Projects/python/EMIS/src/services/admissions_service.py
- [X] T015 [ADM] Implement application workflow in /media/ankit/Programming/Projects/python/EMIS/src/services/application_workflow.py
- [X] T016 [ADM] Integrate DigiLocker for document verification in /media/ankit/Programming/Projects/python/EMIS/src/lib/document_verification.py
- [X] T017 [ADM] Implement merit list generation in /media/ankit/Programming/Projects/python/EMIS/src/services/merit_list.py

### API
- [X] T018 [ADM] Create admissions endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/admissions.py
- [X] T019 [ADM] Add document upload endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/admissions.py
- [X] T020 [ADM] Document admissions API in /media/ankit/Programming/Projects/python/EMIS/docs/api/admissions.md

---

## Phase 3: Course & Curriculum Management

### Models (Parallel)
- [X] T021 [P] [CRS] Create Course model with prerequisites in /media/ankit/Programming/Projects/python/EMIS/src/models/course.py
- [X] T022 [P] [CRS] Create Department model in /media/ankit/Programming/Projects/python/EMIS/src/models/course.py
- [X] T023 [P] [CRS] Create Program/Degree model in /media/ankit/Programming/Projects/python/EMIS/src/models/course.py
- [X] T024 [P] [CRS] Create Curriculum model in /media/ankit/Programming/Projects/python/EMIS/src/models/course.py

### Services
- [X] T025 [CRS] Implement CourseService in /media/ankit/Programming/Projects/python/EMIS/src/services/course_service.py
- [X] T026 [CRS] Add prerequisite validation logic in /media/ankit/Programming/Projects/python/EMIS/src/services/course_service.py
- [X] T027 [CRS] Add curriculum management in /media/ankit/Programming/Projects/python/EMIS/src/services/course_service.py

### API
- [X] T028 [CRS] Create course management endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/courses.py
- [X] T029 [CRS] Document course API in /media/ankit/Programming/Projects/python/EMIS/docs/api/courses.md

---

## Phase 4: Registration & Timetabling

### Models (Parallel)
- [X] T030 [P] [REG] Create CourseRegistration model in /media/ankit/Programming/Projects/python/EMIS/src/models/enrollment.py
- [X] T031 [P] [REG] Create Timetable model in /media/ankit/Programming/Projects/python/EMIS/src/models/timetable.py
- [X] T032 [P] [REG] Create TimetableSlot model in /media/ankit/Programming/Projects/python/EMIS/src/models/timetable.py
- [X] T033 [P] [REG] Create ClassRoom model in /media/ankit/Programming/Projects/python/EMIS/src/models/timetable.py
- [X] T034 [P] [REG] Create ClassSchedule model in /media/ankit/Programming/Projects/python/EMIS/src/models/class_schedule.py
- [X] T035 [P] [REG] Create Substitution model in /media/ankit/Programming/Projects/python/EMIS/src/models/timetable.py

### Services
- [X] T036 [REG] Implement RegistrationService in /media/ankit/Programming/Projects/python/EMIS/src/services/registration_service.py
- [X] T037 [REG] Add course conflict detection in /media/ankit/Programming/Projects/python/EMIS/src/services/registration_service.py
- [X] T038 [REG] Implement TimetableService in /media/ankit/Programming/Projects/python/EMIS/src/services/timetable_service.py
- [X] T039 [REG] Add timetable conflict detection in /media/ankit/Programming/Projects/python/EMIS/src/services/timetable_service.py
- [X] T040 [REG] Implement auto-generation algorithm in /media/ankit/Programming/Projects/python/EMIS/src/services/timetable_service.py
- [X] T041 [REG] Implement ScheduleService in /media/ankit/Programming/Projects/python/EMIS/src/services/schedule_service.py

### API
- [X] T042 [REG] Create registration endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/registration.py
- [X] T043 [REG] Create timetable endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/timetable.py
- [X] T044 [REG] Create schedule endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/schedule.py
- [X] T045 [REG] Document registration/timetable API in /media/ankit/Programming/Projects/python/EMIS/docs/api/registration_timetable.md

---

## Phase 5: Examination & Grading

### Models (Parallel)
- [X] T046 [P] [EXM] Create Exam model in /media/ankit/Programming/Projects/python/EMIS/src/models/exam.py
- [X] T047 [P] [EXM] Create Marks model for internal/external in /media/ankit/Programming/Projects/python/EMIS/src/models/marks.py
- [X] T048 [P] [EXM] Create ResultSheet model in /media/ankit/Programming/Projects/python/EMIS/src/models/result_sheet.py
- [X] T049 [P] [EXM] Create AcademicRecord model in /media/ankit/Programming/Projects/python/EMIS/src/models/academic_record.py
- [X] T050 [P] [EXM] Create ExamRoutine model in /media/ankit/Programming/Projects/python/EMIS/src/models/exam.py
- [X] T051 [P] [EXM] Create ExamForm model in /media/ankit/Programming/Projects/python/EMIS/src/models/exam.py

### Services
- [X] T052 [EXM] Implement ExamService in /media/ankit/Programming/Projects/python/EMIS/src/services/exam_service.py
- [X] T053 [EXM] Add exam routine creation and management in /media/ankit/Programming/Projects/python/EMIS/src/services/exam_service.py
- [X] T054 [EXM] Add exam form submission workflow in /media/ankit/Programming/Projects/python/EMIS/src/services/exam_service.py
- [X] T055 [EXM] Add hall ticket generation in /media/ankit/Programming/Projects/python/EMIS/src/services/exam_service.py
- [X] T056 [EXM] Implement MarksService in /media/ankit/Programming/Projects/python/EMIS/src/services/marks_service.py
- [X] T057 [EXM] Add teacher marks entry functionality in /media/ankit/Programming/Projects/python/EMIS/src/services/marks_service.py
- [X] T058 [EXM] Add GPA/CGPA calculation in /media/ankit/Programming/Projects/python/EMIS/src/services/marks_service.py
- [X] T059 [EXM] Implement ResultService in /media/ankit/Programming/Projects/python/EMIS/src/services/result_service.py
- [X] T060 [EXM] Add transcript generation in /media/ankit/Programming/Projects/python/EMIS/src/services/result_service.py

### API
- [X] T061 [EXM] Create exam endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/exams.py
- [X] T062 [EXM] Create exam routine endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/exams.py
- [X] T063 [EXM] Create exam form endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/exams.py
- [X] T064 [EXM] Create marks entry endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/exams.py
- [X] T065 [EXM] Create result publication endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/exams.py
- [X] T066 [EXM] Document exam/grading API in /media/ankit/Programming/Projects/python/EMIS/docs/api/exams_grading.md

---

## Phase 6: Attendance Management

### Models (Parallel)
- [X] T060 [P] [ATT] Create Attendance model in /media/ankit/Programming/Projects/python/EMIS/src/models/attendance.py
- [X] T061 [P] [ATT] Create AttendanceSession model in /media/ankit/Programming/Projects/python/EMIS/src/models/attendance.py
- [X] T062 [P] [ATT] Create LeaveRequest model in /media/ankit/Programming/Projects/python/EMIS/src/models/attendance.py

### Services
- [X] T063 [ATT] Implement AttendanceService in /media/ankit/Programming/Projects/python/EMIS/src/services/attendance_service.py
- [X] T064 [ATT] Add leave request workflow in /media/ankit/Programming/Projects/python/EMIS/src/services/attendance_service.py
- [X] T065 [ATT] Add automatic leave marking on approval in /media/ankit/Programming/Projects/python/EMIS/src/services/attendance_service.py
- [X] T066 [ATT] Add percentage calculation logic in /media/ankit/Programming/Projects/python/EMIS/src/services/attendance_service.py
- [X] T067 [ATT] Add low attendance alerts in /media/ankit/Programming/Projects/python/EMIS/src/services/attendance_service.py
- [X] T068 [ATT] Add biometric integration support in /media/ankit/Programming/Projects/python/EMIS/src/lib/biometric.py

### API
- [X] T069 [ATT] Create attendance marking endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/attendance.py
- [X] T070 [ATT] Create leave request endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/attendance.py
- [X] T071 [ATT] Create leave approval endpoints for teachers in /media/ankit/Programming/Projects/python/EMIS/src/routes/attendance.py
- [X] T072 [ATT] Create attendance report endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/attendance.py
- [X] T073 [ATT] Document attendance API in /media/ankit/Programming/Projects/python/EMIS/docs/api/attendance.md

---

## Testing & Integration

### Tests (Parallel)
- [X] T069 [P] [TEST] Contract tests for student endpoints in /media/ankit/Programming/Projects/python/EMIS/tests/contract/test_students.py
- [X] T070 [P] [TEST] Contract tests for admissions endpoints in /media/ankit/Programming/Projects/python/EMIS/tests/contract/test_admissions.py
- [X] T071 [P] [TEST] Contract tests for course endpoints in /media/ankit/Programming/Projects/python/EMIS/tests/contract/test_courses.py
- [X] T072 [P] [TEST] Contract tests for exam endpoints in /media/ankit/Programming/Projects/python/EMIS/tests/contract/test_exams.py
- [X] T073 [P] [TEST] Contract tests for attendance endpoints in /media/ankit/Programming/Projects/python/EMIS/tests/contract/test_attendance.py
- [X] T074 [P] [TEST] Integration test for student lifecycle in /media/ankit/Programming/Projects/python/EMIS/tests/integration/test_student_lifecycle.py
- [X] T075 [P] [TEST] Integration test for admission workflow in /media/ankit/Programming/Projects/python/EMIS/tests/integration/test_admission_workflow.py
- [X] T076 [P] [TEST] Integration test for exam process in /media/ankit/Programming/Projects/python/EMIS/tests/integration/test_exam_process.py

### Database
- [X] T077 [DB] Create migrations for all academic models in /media/ankit/Programming/Projects/python/EMIS/alembic/versions/

---

## Summary

- **Total Tasks**: 77
- **SIS**: 9 tasks
- **Admissions**: 11 tasks
- **Course Management**: 9 tasks
- **Registration**: 14 tasks
- **Examination**: 14 tasks
- **Attendance**: 9 tasks
- **Testing**: 8 tasks
- **Database**: 3 tasks

**Status**: All core academic modules completed ✓
