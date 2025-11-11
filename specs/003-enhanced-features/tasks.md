# Tasks: Enhanced EMIS Features

**Input**: Design documents from `/specs/003-enhanced-features/`
**Prerequisites**: All Phase 1-10 tasks completed

## Format: `[ID] [P?] [Module] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Module]**: Which module this task belongs to
- Include exact file paths in descriptions

---

## Phase 11: Complete Missing Core Features

### Library Faculty Borrowing & Lost Books (6 tasks)

- [X] T195 [LIB] Update LibraryService to handle faculty borrowing in /media/ankit/Programming/Projects/python/EMIS/src/services/library_service.py
- [X] T196 [LIB] Add faculty borrowing endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/library.py
- [X] T197 [LIB] Implement lost book fine calculation logic in /media/ankit/Programming/Projects/python/EMIS/src/services/book_loss_service.py
- [X] T198 [LIB] Add lost book API endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/library.py
- [X] T199 [LIB] Add replacement book workflow in /media/ankit/Programming/Projects/python/EMIS/src/services/book_loss_service.py
- [X] T200 [LIB] Document library API updates in /media/ankit/Programming/Projects/python/EMIS/docs/api/library_complete.md

### Bill Types & Printing (8 tasks)

- [X] T201 [P] [BILL] Add hostel fee bill type to BillType enum in /media/ankit/Programming/Projects/python/EMIS/src/models/billing.py
- [X] T202 [P] [BILL] Add transport fee bill type in /media/ankit/Programming/Projects/python/EMIS/src/models/billing.py
- [X] T203 [P] [BILL] Add event fee bill type in /media/ankit/Programming/Projects/python/EMIS/src/models/billing.py
- [X] T204 [P] [BILL] Add other missing bill types in /media/ankit/Programming/Projects/python/EMIS/src/models/billing.py
- [X] T205 [BILL] Enhance PDF generator with QR code support in /media/ankit/Programming/Projects/python/EMIS/src/lib/pdf_generator.py
- [X] T206 [BILL] Add institution letterhead to bill PDFs in /media/ankit/Programming/Projects/python/EMIS/src/lib/pdf_generator.py
- [ ] T207 [BILL] Implement bulk bill generation in /media/ankit/Programming/Projects/python/EMIS/src/services/billing_service.py
- [ ] T208 [BILL] Add email bill functionality in /media/ankit/Programming/Projects/python/EMIS/src/services/billing_service.py

### Report Enhancements (4 tasks)

- [X] T209 [RPT] Add print endpoint for quarterly reports in /media/ankit/Programming/Projects/python/EMIS/src/routes/reports.py
- [ ] T210 [RPT] Enhance quarterly report PDF with charts in /media/ankit/Programming/Projects/python/EMIS/src/lib/pdf_generator.py
- [ ] T211 [RPT] Add comparative analysis to reports in /media/ankit/Programming/Projects/python/EMIS/src/services/quarterly_report_service.py
- [ ] T212 [RPT] Add trend charts to annual reports in /media/ankit/Programming/Projects/python/EMIS/src/lib/pdf_generator.py

---

## Phase 12: Additional Essential Modules

### Hostel Management (12 tasks)

- [ ] T213 [P] [HST] Create Hostel model in /media/ankit/Programming/Projects/python/EMIS/src/models/hostel.py
- [ ] T214 [P] [HST] Create Room model in /media/ankit/Programming/Projects/python/EMIS/src/models/hostel.py
- [ ] T215 [P] [HST] Create RoomAllocation model in /media/ankit/Programming/Projects/python/EMIS/src/models/hostel.py
- [ ] T216 [P] [HST] Create MessMenu model in /media/ankit/Programming/Projects/python/EMIS/src/models/hostel.py
- [ ] T217 [P] [HST] Create HostelVisitor model in /media/ankit/Programming/Projects/python/EMIS/src/models/hostel.py
- [ ] T218 [P] [HST] Create HostelComplaint model in /media/ankit/Programming/Projects/python/EMIS/src/models/hostel.py
- [ ] T219 [HST] Implement HostelService in /media/ankit/Programming/Projects/python/EMIS/src/services/hostel_service.py
- [ ] T220 [HST] Implement room allocation logic in /media/ankit/Programming/Projects/python/EMIS/src/services/hostel_service.py
- [ ] T221 [HST] Create hostel API endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/hostel.py
- [ ] T222 [HST] Add hostel fee integration with billing in /media/ankit/Programming/Projects/python/EMIS/src/services/billing_service.py
- [ ] T223 [HST] Create migration for hostel tables in /media/ankit/Programming/Projects/python/EMIS/alembic/versions/
- [ ] T224 [HST] Document hostel API in /media/ankit/Programming/Projects/python/EMIS/docs/api/hostel.md

### Transport Management (11 tasks)

- [ ] T225 [P] [TRN] Create Vehicle model in /media/ankit/Programming/Projects/python/EMIS/src/models/transport.py
- [ ] T226 [P] [TRN] Create Route model in /media/ankit/Programming/Projects/python/EMIS/src/models/transport.py
- [ ] T227 [P] [TRN] Create RouteStop model in /media/ankit/Programming/Projects/python/EMIS/src/models/transport.py
- [ ] T228 [P] [TRN] Create StudentTransport model in /media/ankit/Programming/Projects/python/EMIS/src/models/transport.py
- [ ] T229 [P] [TRN] Create VehicleMaintenance model in /media/ankit/Programming/Projects/python/EMIS/src/models/transport.py
- [ ] T230 [TRN] Implement TransportService in /media/ankit/Programming/Projects/python/EMIS/src/services/transport_service.py
- [ ] T231 [TRN] Implement route optimization logic in /media/ankit/Programming/Projects/python/EMIS/src/services/transport_service.py
- [ ] T232 [TRN] Create transport API endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/transport.py
- [ ] T233 [TRN] Add transport fee integration in /media/ankit/Programming/Projects/python/EMIS/src/services/billing_service.py
- [ ] T234 [TRN] Create migration for transport tables in /media/ankit/Programming/Projects/python/EMIS/alembic/versions/
- [ ] T235 [TRN] Document transport API in /media/ankit/Programming/Projects/python/EMIS/docs/api/transport.md

### Event Management (10 tasks)

- [ ] T236 [P] [EVT] Create Event model in /media/ankit/Programming/Projects/python/EMIS/src/models/event.py
- [ ] T237 [P] [EVT] Create EventRegistration model in /media/ankit/Programming/Projects/python/EMIS/src/models/event.py
- [ ] T238 [P] [EVT] Create EventBudget model in /media/ankit/Programming/Projects/python/EMIS/src/models/event.py
- [ ] T239 [P] [EVT] Create EventAttendance model in /media/ankit/Programming/Projects/python/EMIS/src/models/event.py
- [ ] T240 [EVT] Implement EventService in /media/ankit/Programming/Projects/python/EMIS/src/services/event_service.py
- [ ] T241 [EVT] Implement certificate generation in /media/ankit/Programming/Projects/python/EMIS/src/lib/certificate_generator.py
- [ ] T242 [EVT] Create event API endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/events.py
- [ ] T243 [EVT] Add event fee integration in /media/ankit/Programming/Projects/python/EMIS/src/services/billing_service.py
- [ ] T244 [EVT] Create migration for event tables in /media/ankit/Programming/Projects/python/EMIS/alembic/versions/
- [ ] T245 [EVT] Document event API in /media/ankit/Programming/Projects/python/EMIS/docs/api/events.md

### Placement Management (11 tasks)

- [ ] T246 [P] [PLC] Create Company model in /media/ankit/Programming/Projects/python/EMIS/src/models/placement.py
- [ ] T247 [P] [PLC] Create JobPosting model in /media/ankit/Programming/Projects/python/EMIS/src/models/placement.py
- [ ] T248 [P] [PLC] Create PlacementApplication model in /media/ankit/Programming/Projects/python/EMIS/src/models/placement.py
- [ ] T249 [P] [PLC] Create Interview model in /media/ankit/Programming/Projects/python/EMIS/src/models/placement.py
- [ ] T250 [P] [PLC] Create PlacementOffer model in /media/ankit/Programming/Projects/python/EMIS/src/models/placement.py
- [ ] T251 [PLC] Implement PlacementService in /media/ankit/Programming/Projects/python/EMIS/src/services/placement_service.py
- [ ] T252 [PLC] Implement placement statistics in /media/ankit/Programming/Projects/python/EMIS/src/services/placement_service.py
- [ ] T253 [PLC] Create placement API endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/placement.py
- [ ] T254 [PLC] Add placement reports in /media/ankit/Programming/Projects/python/EMIS/src/services/placement_service.py
- [ ] T255 [PLC] Create migration for placement tables in /media/ankit/Programming/Projects/python/EMIS/alembic/versions/
- [ ] T256 [PLC] Document placement API in /media/ankit/Programming/Projects/python/EMIS/docs/api/placement.md

### Alumni Management (10 tasks)

- [ ] T257 [P] [ALM] Create Alumni model in /media/ankit/Programming/Projects/python/EMIS/src/models/alumni.py
- [ ] T258 [P] [ALM] Create AlumniEmployment model in /media/ankit/Programming/Projects/python/EMIS/src/models/alumni.py
- [ ] T259 [P] [ALM] Create AlumniEvent model in /media/ankit/Programming/Projects/python/EMIS/src/models/alumni.py
- [ ] T260 [P] [ALM] Create AlumniDonation model in /media/ankit/Programming/Projects/python/EMIS/src/models/alumni.py
- [ ] T261 [ALM] Implement AlumniService in /media/ankit/Programming/Projects/python/EMIS/src/services/alumni_service.py
- [ ] T262 [ALM] Implement mentorship matching in /media/ankit/Programming/Projects/python/EMIS/src/services/alumni_service.py
- [ ] T263 [ALM] Create alumni API endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/alumni.py
- [ ] T264 [ALM] Add alumni reports in /media/ankit/Programming/Projects/python/EMIS/src/services/alumni_service.py
- [ ] T265 [ALM] Create migration for alumni tables in /media/ankit/Programming/Projects/python/EMIS/alembic/versions/
- [ ] T266 [ALM] Document alumni API in /media/ankit/Programming/Projects/python/EMIS/docs/api/alumni.md

---

## Phase 13: Supporting Modules

### Inventory Management (12 tasks)

- [ ] T267 [P] [INV] Create InventoryItem model in /media/ankit/Programming/Projects/python/EMIS/src/models/inventory.py
- [ ] T268 [P] [INV] Create InventoryCategory model in /media/ankit/Programming/Projects/python/EMIS/src/models/inventory.py
- [ ] T269 [P] [INV] Create PurchaseOrder model in /media/ankit/Programming/Projects/python/EMIS/src/models/inventory.py
- [ ] T270 [P] [INV] Create Vendor model in /media/ankit/Programming/Projects/python/EMIS/src/models/inventory.py
- [ ] T271 [P] [INV] Create StockTransaction model in /media/ankit/Programming/Projects/python/EMIS/src/models/inventory.py
- [ ] T272 [INV] Implement InventoryService in /media/ankit/Programming/Projects/python/EMIS/src/services/inventory_service.py
- [ ] T273 [INV] Implement stock alert logic in /media/ankit/Programming/Projects/python/EMIS/src/services/inventory_service.py
- [ ] T274 [INV] Implement purchase workflow in /media/ankit/Programming/Projects/python/EMIS/src/services/inventory_service.py
- [ ] T275 [INV] Create inventory API endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/inventory.py
- [ ] T276 [INV] Add inventory reports in /media/ankit/Programming/Projects/python/EMIS/src/services/inventory_service.py
- [ ] T277 [INV] Create migration for inventory tables in /media/ankit/Programming/Projects/python/EMIS/alembic/versions/
- [ ] T278 [INV] Document inventory API in /media/ankit/Programming/Projects/python/EMIS/docs/api/inventory.md

### Timetable Management (10 tasks)

- [ ] T279 [P] [TTB] Create Timetable model in /media/ankit/Programming/Projects/python/EMIS/src/models/timetable.py
- [ ] T280 [P] [TTB] Create ClassRoom model in /media/ankit/Programming/Projects/python/EMIS/src/models/timetable.py
- [ ] T281 [P] [TTB] Create TimetableSlot model in /media/ankit/Programming/Projects/python/EMIS/src/models/timetable.py
- [ ] T282 [P] [TTB] Create Substitution model in /media/ankit/Programming/Projects/python/EMIS/src/models/timetable.py
- [ ] T283 [TTB] Implement TimetableService in /media/ankit/Programming/Projects/python/EMIS/src/services/timetable_service.py
- [ ] T284 [TTB] Implement conflict detection algorithm in /media/ankit/Programming/Projects/python/EMIS/src/services/timetable_service.py
- [ ] T285 [TTB] Implement auto-generation logic in /media/ankit/Programming/Projects/python/EMIS/src/services/timetable_service.py
- [ ] T286 [TTB] Create timetable API endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/timetable.py
- [ ] T287 [TTB] Create migration for timetable tables in /media/ankit/Programming/Projects/python/EMIS/alembic/versions/
- [ ] T288 [TTB] Document timetable API in /media/ankit/Programming/Projects/python/EMIS/docs/api/timetable.md

### Complaint/Grievance System (10 tasks)

- [ ] T289 [P] [CMP] Create Complaint model in /media/ankit/Programming/Projects/python/EMIS/src/models/complaint.py
- [ ] T290 [P] [CMP] Create ComplaintCategory model in /media/ankit/Programming/Projects/python/EMIS/src/models/complaint.py
- [ ] T291 [P] [CMP] Create ComplaintComment model in /media/ankit/Programming/Projects/python/EMIS/src/models/complaint.py
- [ ] T292 [CMP] Implement ComplaintService in /media/ankit/Programming/Projects/python/EMIS/src/services/complaint_service.py
- [ ] T293 [CMP] Implement escalation workflow in /media/ankit/Programming/Projects/python/EMIS/src/services/complaint_service.py
- [ ] T294 [CMP] Implement auto-assignment logic in /media/ankit/Programming/Projects/python/EMIS/src/services/complaint_service.py
- [ ] T295 [CMP] Create complaint API endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/complaints.py
- [ ] T296 [CMP] Add complaint notification triggers in /media/ankit/Programming/Projects/python/EMIS/src/services/complaint_service.py
- [ ] T297 [CMP] Create migration for complaint tables in /media/ankit/Programming/Projects/python/EMIS/alembic/versions/
- [ ] T298 [CMP] Document complaint API in /media/ankit/Programming/Projects/python/EMIS/docs/api/complaints.md

### Document Management (10 tasks)

- [ ] T299 [P] [DOC] Create Document model in /media/ankit/Programming/Projects/python/EMIS/src/models/documents.py
- [ ] T300 [P] [DOC] Create DocumentVersion model in /media/ankit/Programming/Projects/python/EMIS/src/models/documents.py
- [ ] T301 [P] [DOC] Create DocumentTemplate model in /media/ankit/Programming/Projects/python/EMIS/src/models/documents.py
- [ ] T302 [DOC] Implement DocumentService in /media/ankit/Programming/Projects/python/EMIS/src/services/document_service.py
- [ ] T303 [DOC] Implement version control logic in /media/ankit/Programming/Projects/python/EMIS/src/services/document_service.py
- [ ] T304 [DOC] Implement digital signature support in /media/ankit/Programming/Projects/python/EMIS/src/lib/digital_signature.py
- [ ] T305 [DOC] Create document API endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/documents.py
- [ ] T306 [DOC] Add expiry tracking workflow in /media/ankit/Programming/Projects/python/EMIS/src/services/document_service.py
- [ ] T307 [DOC] Create migration for document tables in /media/ankit/Programming/Projects/python/EMIS/alembic/versions/
- [ ] T308 [DOC] Document document management API in /media/ankit/Programming/Projects/python/EMIS/docs/api/documents.md

### Communication Hub (8 tasks)

- [ ] T309 [P] [COM] Create Announcement model in /media/ankit/Programming/Projects/python/EMIS/src/models/communication.py
- [ ] T310 [P] [COM] Create Circular model in /media/ankit/Programming/Projects/python/EMIS/src/models/communication.py
- [ ] T311 [P] [COM] Create NoticeBoard model in /media/ankit/Programming/Projects/python/EMIS/src/models/communication.py
- [ ] T312 [COM] Implement CommunicationService in /media/ankit/Programming/Projects/python/EMIS/src/services/communication_service.py
- [ ] T313 [COM] Implement targeted messaging in /media/ankit/Programming/Projects/python/EMIS/src/services/communication_service.py
- [ ] T314 [COM] Create communication API endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/communication.py
- [ ] T315 [COM] Create migration for communication tables in /media/ankit/Programming/Projects/python/EMIS/alembic/versions/
- [ ] T316 [COM] Document communication API in /media/ankit/Programming/Projects/python/EMIS/docs/api/communication.md

---

## Phase 14: Final Integration & Testing

### Integration Tasks (8 tasks)

- [ ] T317 [INT] Register all new routes in main app in /media/ankit/Programming/Projects/python/EMIS/src/app.py
- [ ] T318 [INT] Update database initialization in /media/ankit/Programming/Projects/python/EMIS/src/database.py
- [ ] T319 [INT] Create seed data for all new modules in /media/ankit/Programming/Projects/python/EMIS/alembic/seed_data.py
- [ ] T320 [INT] Update RBAC permissions for new modules in /media/ankit/Programming/Projects/python/EMIS/src/middleware/rbac.py
- [ ] T321 [INT] Add comprehensive validation schemas in /media/ankit/Programming/Projects/python/EMIS/src/lib/validation.py
- [ ] T322 [INT] Update requirements.txt with new dependencies in /media/ankit/Programming/Projects/python/EMIS/requirements.txt
- [ ] T323 [INT] Run all migrations in sequence
- [ ] T324 [INT] Verify all endpoints are documented in OpenAPI

### Testing Tasks (6 tasks)

- [ ] T325 [P] [TEST] Create unit tests for new services in /media/ankit/Programming/Projects/python/EMIS/tests/unit/
- [ ] T326 [P] [TEST] Create integration tests for new workflows in /media/ankit/Programming/Projects/python/EMIS/tests/integration/
- [ ] T327 [P] [TEST] Create API contract tests in /media/ankit/Programming/Projects/python/EMIS/tests/contract/
- [ ] T328 [TEST] Run complete test suite
- [ ] T329 [TEST] Performance testing for dashboard and reports
- [ ] T330 [TEST] Security audit for all new endpoints

### Documentation (4 tasks)

- [ ] T331 [P] [DOC] Update main README with all modules in /media/ankit/Programming/Projects/python/EMIS/README.md
- [ ] T332 [P] [DOC] Create comprehensive user guide in /media/ankit/Programming/Projects/python/EMIS/docs/user_guide.md
- [ ] T333 [P] [DOC] Create admin manual in /media/ankit/Programming/Projects/python/EMIS/docs/admin_manual.md
- [ ] T334 [DOC] Create deployment guide in /media/ankit/Programming/Projects/python/EMIS/docs/deployment_guide.md

---

## Summary

- **Total New Tasks**: 140 (T195-T334)
- **Phase 11**: 18 tasks (Complete missing core features)
- **Phase 12**: 64 tasks (Additional essential modules)
- **Phase 13**: 40 tasks (Supporting modules)
- **Phase 14**: 18 tasks (Integration & testing)

**Grand Total (All Phases)**: 334 tasks

## Dependencies

- Phase 11 can start immediately (completes existing features)
- Phase 12 depends on Phase 11 completion
- Phase 13 can run in parallel with Phase 12
- Phase 14 depends on all previous phases

## Execution Strategy

1. **Quick Wins (Phase 11)**: Complete missing pieces of existing modules
2. **Essential Modules (Phase 12)**: Add critical institutional features
3. **Supporting Features (Phase 13)**: Add nice-to-have features
4. **Integration (Phase 14)**: Final testing and documentation

All file paths are absolute from `/media/ankit/Programming/Projects/python/EMIS/`
