# Implementation Plan: EMIS Core Platform

## Guiding Principles
- Implement in dependency order: Auth → Admissions → Courses/Assessment → Finance → Dashboard.
- Favor atomic pull requests aligned to TASK groups.
- Maintain test-first approach: write failing test for each FR then implement.

## High-Level Phases
1. Clarifications & Traceability Matrix
2. RBAC & Authentication Foundation
3. Admissions Lifecycle Core
4. Academic Course & Assignment Flow
5. Financial Fee Structure & Payments
6. Dashboard Aggregation Layer
7. Hardening (Edge Cases, Performance, Audits)
8. Final Success Criteria Validation & Documentation

## Task Breakdown

### Phase 1: Clarifications & Traceability
- TASK-001: Resolve error code taxonomy (FR-020)
  - What: Define format DOMAIN_CATEGORY_SUBCODE and reserve ranges.
  - Why: Enables consistent error responses and future client mapping.
  - How: Draft proposal, review with QA & domain owners, update spec.
  - Verify: Error code reference published; sample responses include codes.
- TASK-002: Define permission granularity (FR-021)
  - What: Decide action-level vs resource-level model and structure.
  - Why: Required for RBAC design before implementation.
  - How: Compare complexity, select hybrid (resource groups + actions), document.
  - Verify: Permission model doc approved.
- TASK-003: Confirm initial language set (FR-022)
  - What: Finalize supported languages for UI strings.
  - Why: Avoid scope creep and translation gaps.
  - How: Stakeholder meeting; record decision.
  - Verify: Spec updated; localization placeholders prepared.
- TASK-004: Create traceability matrix (FR ↔ Test IDs)
  - What: Map each FR to planned test cases.
  - Why: Ensures coverage tracking from start.
  - How: Draft matrix CSV/MD; link in repo.
  - Verify: QA sign-off.

### Phase 2: RBAC & Authentication
- TASK-010: Implement user & role schema (FR-001, FR-002)
- TASK-011: Session/token issuance logic
- TASK-012: Authorization middleware hooking into permission map
- TASK-013: Audit logging foundation (FR-003)
- TASK-014: Tests for login, forbidden access, audit creation

### Phase 3: Admissions
- TASK-020: Application model & submission endpoint (FR-004)
- TASK-021: Status transition rules & validation (FR-005)
- TASK-022: Merit list generation service (FR-006)
- TASK-023: Enrollment creation logic (FR-007)
- TASK-024: Edge case tests (missing docs, multiple merit runs)

### Phase 4: Courses & Assessment
- TASK-030: Course + module schema (FR-008)
- TASK-031: Assignment creation + deadline enforcement (FR-009)
- TASK-032: Submission endpoint w/ timestamp (FR-009)
- TASK-033: Grading flow + grade record updates (FR-010)
- TASK-034: Prerequisite check logic (FR-015)
- TASK-035: Transcript generation (FR-017)
- TASK-036: Edge tests (late submission, deleted content access)

### Phase 5: Finance
- TASK-040: Fee structure schema (FR-012)
- TASK-041: Invoice generation service (FR-011, FR-012, FR-016)
- TASK-042: Payment processing w/ late fee logic (FR-011, FR-016)
- TASK-043: Reporting export endpoint (FR-013)
- TASK-044: Edge tests (partial payment, late fee reversal)

### Phase 6: Dashboard
- TASK-050: Metric computation services (FR-014)
- TASK-051: Aggregation and caching strategy
- TASK-052: Dashboard API endpoint
- TASK-053: Tests validating metric correctness vs source data
- TASK-054: Zero-data edge cases

### Phase 7: Hardening & Cross-Cutting
- TASK-060: Standard error response wrapper (FR-020)
- TASK-061: Internationalization scaffolding (FR-022)
- TASK-062: Permission change propagation tests (SC-006)
- TASK-063: Pagination & search implementation (FR-018, FR-019)
- TASK-064: Performance index tuning for critical queries
- TASK-065: Audit completeness validation scripts

### Phase 8: Finalization
- TASK-070: Success criteria measurement run (SC-001..SC-010)
- TASK-071: Update documentation & usage guides
- TASK-072: Compile final traceability matrix with test outcomes
- TASK-073: Version bump and revision log update (Spec MINOR)

## Dependencies Summary
- RBAC precedes Admissions & Courses.
- Admissions enrollment required before fee invoices.
- Finance & course data required for dashboard metrics.
- Error taxonomy required before standard response wrapper.

## Verification Strategy
- Each TASK introduces or updates tests; build must pass before proceeding to next phase.
- Performance criteria validated with seeded dataset.
- Audit sampling script checks 100% presence for sensitive actions.

## Risk Mitigations
- Early clarification phase reduces late rework (address FR-020/021/022 upfront).
- Incremental metrics implementation prevents dashboard bottlenecks.
- Traceability matrix ensures no FR left untested.

## Completion Definition
All tasks DONE, all FR tests GREEN, success criteria metrics met or justified, and revision log updated.
