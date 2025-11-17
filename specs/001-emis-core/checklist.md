# Specification Checklist: EMIS Core Platform

| Item | Description | Status | Notes |
|------|-------------|--------|-------|
| US | User stories with priorities | ✅ | 5 core stories defined |
| FR | Functional requirements enumerated & numbered | ✅ | FR-001 .. FR-022 |
| SC | Success criteria measurable | ✅ | SC-001 .. SC-010 |
| ENT | Key entities listed | ✅ | 17 entities |
| EDGE | Edge cases documented | ✅ | 10 initial cases |
| ASSUMP | Assumptions explicit | ✅ | Listed |
| DEP | Dependencies captured | ✅ | Sequenced |
| RISKS | Risks with mitigation | ✅ | 4 risks |
| OPEN | Open questions enumerated | ✅ | 3 questions |
| NFR | Non-functional references present | ✅ | Integrated in SC / risks |
| GLOSS | Glossary terms defined | ✅ | Included |
| TRACE | FR ↔ Test mapping started | ⏳ | To create after test case IDs assigned |
| CLAR | Clarification log present | ✅ | 5 clarifications resolved 2025-11-16 |
| VERSION | Revision log entry | ✅ | 2025-11-16 initial + clarifications |
| NEUTRAL | Tech neutral (no frameworks) | ✅ | Verified |
| ERR-CODES | Error taxonomy defined | ✅ | MODULE_ERROR_CODE format (FR-020) |
| PERM-MODEL | Permission granularity clarified | ✅ | Hybrid resource groups + actions (FR-021) |
| LANG-SET | Initial language set confirmed | ✅ | English only, i18n infrastructure for future (FR-022) |
| SESSION-EXT | Session timeout behavior defined | ✅ | Auto-extend during operations |
| CONCURRENCY | Concurrent user target specified | ✅ | 5,000 concurrent users (SC-011) |

## Actions Required Before Implementation
1. ✅ Resolve open questions (error codes, permission granularity, language set) - COMPLETED
2. Establish initial traceability matrix (assign test IDs per FR).
3. Create detailed error code registry with MODULE_ERROR_CODE assignments.
4. Design resource group hierarchy and action definitions for RBAC.

## Next Steps
- Draft error code registry mapping modules to code ranges.
- Design permission resource group taxonomy (e.g., students.records, courses.content).
- Draft initial test case list referencing FR IDs.
- Proceed to `/speckit.plan` for implementation planning.
