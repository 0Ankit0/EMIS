# Traceability Matrix: EMIS Core Platform

| FR ID | Requirement Summary | Acceptance Scenario(s) | Planned Test ID(s) | Implemented | Notes |
|-------|---------------------|------------------------|--------------------|-------------|-------|
| FR-001 | User authentication | US1 S1 | TST-LOGIN-VALID, TST-LOGIN-INVALID | ⏳ |  |
| FR-002 | Role-based authorization | US1 S2 | TST-RBAC-DENY, TST-RBAC-ALLOW | ⏳ |  |
| FR-003 | Audit logging sensitive actions | US1 S1/S2 | TST-AUDIT-LOGIN, TST-AUDIT-DENY | ⏳ |  |
| FR-004 | Application submission | US2 S1 | TST-APP-SUBMIT-VALID, TST-APP-SUBMIT-MISSING | ⏳ |  |
| FR-005 | Status lifecycle transitions | US2 S1 | TST-APP-STATUS-TRANSITIONS | ⏳ |  |
| FR-006 | Merit list generation | US2 S2 | TST-MERIT-GEN | ⏳ |  |
| FR-007 | Enrollment record creation | US2 S3 | TST-ENROLL-CREATE | ⏳ |  |
| FR-008 | Course creation | US3 S1 | TST-COURSE-CREATE | ⏳ |  |
| FR-009 | Assignment submission capture | US3 S2 | TST-ASSIGN-SUBMIT-ONTIME, TST-ASSIGN-SUBMIT-LATE | ⏳ |  |
| FR-010 | Grading & grade record updates | US3 S3 | TST-GRADE-RECORD | ⏳ |  |
| FR-011 | Late fee application | US4 S2 | TST-FEE-LATE | ⏳ |  |
| FR-012 | Fee structure definition | US4 S1 | TST-FEE-STRUCTURE-DEFINE | ⏳ |  |
| FR-013 | Fee collection reporting | US4 S3 | TST-FEE-REPORT | ⏳ |  |
| FR-014 | Dashboard metrics aggregation | US5 S1-S3 | TST-DASH-METRICS | ⏳ |  |
| FR-015 | Prerequisite enforcement | Edge | TST-COURSE-PREREQ | ⏳ |  |
| FR-016 | Partial payment tracking | Edge | TST-FEE-PARTIAL | ⏳ |  |
| FR-017 | Transcript generation gating | Edge | TST-TRANSCRIPT-GENERATE | ⏳ |  |
| FR-018 | Search/filter operations | - | TST-SEARCH-APPS, TST-SEARCH-COURSES | ⏳ |  |
| FR-019 | Pagination for large lists | - | TST-PAGINATION-APPS | ⏳ |  |
| FR-020 | Standardized error responses | - | TST-ERROR-STRUCTURE | ⏳ | Needs clarification CQ-001 |
| FR-021 | Permission modification audit | Edge | TST-PERM-CHANGE-AUDIT | ⏳ | Needs clarification CQ-002 |
| FR-022 | Multi-language support baseline | - | TST-I18N-PAGES | ⏳ | Needs clarification CQ-003 |

## Notes
- Test IDs placeholder until concrete pytest function names generated.
- Implemented column toggles to ✅ once feature test passes.
