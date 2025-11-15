tests/
ios/ or android/

# Implementation Plan: EMIS Core System

**Branch**: `001-emis-core` | **Date**: 2025-11-09 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-emis-core/spec.md`

## Summary

Build a modular monolith EMIS for a college, centralizing and automating all core administrative, academic, and operational processes. The system will use Python 3.11+, Django, PostgreSQL 15+, async Django ORM, Redis, Celery, and Docker. All APIs will be documented and versioned. The system will be test-driven, CI/CD-enabled, and compliant with GDPR/Indian IT Act.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Django, async Django ORM, Celery, Redis, Django Migrations, Django Serializers, pytest
**Storage**: PostgreSQL 15+ (primary), Redis (cache, queue)
**Testing**: pytest (unit, integration, end-to-end), contract tests (OpenAPI schema validation)
**Target Platform**: Linux server (cloud or on-prem)
**Project Type**: single (modular monolith, backend-only)
**Performance Goals**: Support 10,000+ active users, 95% of requests <500ms, 99% uptime
**Constraints**: ≤3 core projects/services, GDPR/Indian IT Act compliance, 100% test coverage for core logic
**Scale/Scope**: 10,000+ users, 100+ concurrent staff, 1M+ records, 50+ modules

## Constitution Check

All gates pass:
- Security: Encryption in transit/at rest, audit logging, GDPR/IT Act compliance
- Modularity: Library-first, CLI, separation of concerns
- Test-First: TDD, contract-first, integration-first
- Simplicity: ≤3 projects, no future-proofing
- Observability: Health checks, logging, metrics
- Maintainability: Documentation, CI/CD, up-to-date dependencies
- Compliance: Data privacy, code quality, error handling, regular reviews

## Project Structure

### Documentation (this feature)

```text
specs/001-emis-core/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
src/
├── models/
├── services/
├── cli/
└── lib/


├── contract/
├── integration/
└── unit/
```

**Structure Decision**: Single-project, backend-only modular monolith. All code in `src/` and `tests/` at repo root. No frontend.

## Complexity Tracking

No constitution violations. All gates passed.
| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |

## Module Implementation Tasks & References

For each module, follow the explicit, ordered sequence below. As detail files (contracts, data models, quickstart) are created, update the references accordingly. Where clarifications or refinements exist, cross-link to the relevant section.

### Auth Module
1. Define User, Role, Permission models (**Reference:** data-model.md §2.1)
2. Write OpenAPI contract for Auth endpoints (**Reference:** contracts/auth/openapi.yaml)
3. Implement RBAC middleware (**Reference:** plan.md §RBAC, clarify.md item 1)
4. Implement login, registration, password reset, 2FA (**Reference:** plan.md §Auth, clarify.md item 1)
5. Add audit logging (**Reference:** clarify.md item 1, plan.md §Security)
6. Write and run tests (**Reference:** tests/auth/)
7. Document API (**Reference:** docs/auth.md)

### Students Module
1. Define Student, Enrollment, AcademicRecord, Attendance models (**Reference:** data-model.md §2.2)
2. Write contracts for student lifecycle endpoints (**Reference:** contracts/students/)
3. Implement lifecycle workflows (admission, enrollment, graduation, alumni) (**Reference:** clarify.md item 2)
4. Implement alumni tracking (**Reference:** clarify.md item 2)
5. Write and run tests (**Reference:** tests/students/)
6. Document API (**Reference:** docs/students.md)

### HR Module
1. Define Employee, Payroll, Leave, PerformanceReview, Recruitment models (**Reference:** data-model.md §2.3)
2. Write contracts for HR endpoints (**Reference:** contracts/hr/)
3. Implement payroll rules engine (**Reference:** clarify.md item 3)
4. Implement leave approval workflows (**Reference:** clarify.md item 3)
5. Write and run tests (**Reference:** tests/hr/)
6. Document API (**Reference:** docs/hr.md)

### Library Module
1. Define Book, Member, Issue, Reservation, Fine, DigitalResource models (**Reference:** data-model.md §2.4)
2. Write contracts for library endpoints (**Reference:** contracts/library/)
3. Implement circulation policies, barcode/RFID integration (**Reference:** clarify.md item 4)
4. Implement analytics (**Reference:** plan.md §Analytics)
5. Write and run tests (**Reference:** tests/library/)
6. Document API (**Reference:** docs/library.md)

### LMS Module
1. Define Course, Module, Lesson, Assignment, Quiz, Submission models (**Reference:** data-model.md §2.5)
2. Write contracts for LMS endpoints (**Reference:** contracts/lms/)
3. Implement content delivery, assessment engine, plagiarism detection (**Reference:** clarify.md item 5)
4. Integrate video conferencing (**Reference:** clarify.md item 5)
5. Write and run tests (**Reference:** tests/lms/)
6. Document API (**Reference:** docs/lms.md)

### CMS Module
1. Define Page, Menu, Media, News, Event, Gallery models (**Reference:** data-model.md §2.6)
2. Write contracts for CMS endpoints (**Reference:** contracts/cms/)
3. Implement approval workflows, multi-language content, SEO tools (**Reference:** clarify.md item 6)
4. Write and run tests (**Reference:** tests/cms/)
5. Document API (**Reference:** docs/cms.md)

### Admissions Module
1. Define Application, Document, Fee, Test, Interview models (**Reference:** data-model.md §2.7)
2. Write contracts for admissions endpoints (**Reference:** contracts/admissions/)
3. Implement multi-step wizard, payment gateway integration, merit list automation (**Reference:** clarify.md item 7)
4. Write and run tests (**Reference:** tests/admissions/)
5. Document API (**Reference:** docs/admissions.md)

### Accounts Module
1. Define FeeStructure, Payment, Expense, Budget, JournalEntry models (**Reference:** data-model.md §2.8)
2. Write contracts for accounts endpoints (**Reference:** contracts/accounts/)
3. Implement double-entry accounting, UGC/AICTE reporting (**Reference:** clarify.md item 8)
4. Write and run tests (**Reference:** tests/accounts/)
5. Document API (**Reference:** docs/accounts.md)

### Analytics Module
1. Implement aggregation services for all modules (**Reference:** plan.md §Analytics)
2. Implement custom report builder, predictive analytics (**Reference:** clarify.md item 9)
3. Write and run tests (**Reference:** tests/analytics/)
4. Document API (**Reference:** docs/analytics.md)

### Notifications Module
1. Implement email, SMS, in-app notification services (**Reference:** data-model.md §2.9, contracts/notifications/)
2. Implement opt-in/opt-out management, bulk messaging (**Reference:** clarify.md item 10)
3. Write and run tests (**Reference:** tests/notifications/)
4. Document API (**Reference:** docs/notifications.md)

## Cross-Module Tasks
1. Implement RBAC and audit logging for all sensitive actions (**Reference:** clarify.md item 1, plan.md §Security)
2. Enforce GDPR and Indian IT Act compliance at all layers (**Reference:** clarify.md item 11)
3. Set up Docker Compose, CI/CD, environment variables, infrastructure-as-code (**Reference:** plan.md §DevOps)
4. Centralized logging, monitoring, and alerting (**Reference:** plan.md §DevOps)
5. Write and enforce tests, linting, type checking (**Reference:** plan.md §Testing)
6. Auto-generate and maintain API documentation (**Reference:** plan.md §Documentation)
