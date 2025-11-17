# Clarification Log: EMIS Core Platform

| ID | Question | Resolution | Date | Owner | Impact |
|----|----------|-----------|------|-------|--------|
| CQ-001 | Error code taxonomy structure? (FR-020) | MODULE_ERROR_CODE format (e.g., AUTH_001, ADMISSIONS_201) | 2025-11-16 | System Architect | Required for standardized error responses; affects all API endpoints |
| CQ-002 | Permission granularity model? (FR-021) | Hybrid: resource groups + actions within groups (e.g., students.records.view) | 2025-11-16 | Security Lead | Drives RBAC data model, middleware, and permission assignment UI |
| CQ-003 | Initial language set for localization? (FR-022) | English only (additional languages deferred to future phases) | 2025-11-16 | Product Owner | Simplifies initial i18n infrastructure; multi-language support deferred |
| CQ-004 | Session timeout behavior during long operations? | Auto-extend session during active operations with activity tracking | 2025-11-16 | Backend Lead | Affects session middleware, improves UX for report generation and bulk operations |
| CQ-005 | Maximum concurrent user capacity target? | 5,000 concurrent users | 2025-11-16 | Infrastructure Lead | Guides load testing targets, horizontal scaling strategy, and resource planning |

## Process
- Each clarification assigned an ID (CQ-###).
- Upon resolution, spec.md updated removing NEEDS CLARIFICATION markers.
- Impact column summarizes areas to revisit (tests, schemas, endpoints).

## Completed Actions
All pending clarifications (CQ-001 through CQ-005) resolved on 2025-11-16.
- ✅ Updated FR-020, FR-021, FR-022 with specific requirements
- ✅ Added ResourceGroup entity and MODULE_ERROR_CODE to glossary
- ✅ Updated Assumptions section with all clarified details
- ✅ Refined Risks section based on clarifications
- ✅ Added SC-011 (concurrent users) and SC-012 (session auto-extend)
- ✅ Marked Open Questions as resolved
