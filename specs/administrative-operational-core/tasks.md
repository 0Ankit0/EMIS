# Tasks: Administrative & Operational Core

**Input**: Design documents from `/specs/administrative-operational-core/`
**Prerequisites**: Foundation setup, Academic Core (for student/faculty references)

## Format: `[ID] [P?] [Module] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Module]**: Which module this task belongs to
- All paths are absolute from `/media/ankit/Programming/Projects/python/EMIS/`

---

## Phase 1: Faculty & Staff Management (HR)

### Models (Parallel)
- [X] T101 [P] [HR] Create Employee model in /media/ankit/Programming/Projects/python/EMIS/src/models/employee.py
- [X] T102 [P] [HR] Create TeacherHierarchy model in /media/ankit/Programming/Projects/python/EMIS/src/models/employee.py
- [X] T103 [P] [HR] Create Payroll model in /media/ankit/Programming/Projects/python/EMIS/src/models/payroll.py
- [X] T104 [P] [HR] Create Leave model in /media/ankit/Programming/Projects/python/EMIS/src/models/leave.py
- [X] T105 [P] [HR] Create PerformanceReview model in /media/ankit/Programming/Projects/python/EMIS/src/models/performance.py
- [X] T106 [P] [HR] Create Recruitment model in /media/ankit/Programming/Projects/python/EMIS/src/models/recruitment.py

### Services
- [X] T107 [HR] Implement HRService with employee CRUD in /media/ankit/Programming/Projects/python/EMIS/src/services/hr_service.py
- [X] T108 [HR] Implement PayrollService with salary calculation in /media/ankit/Programming/Projects/python/EMIS/src/services/payroll_engine.py
- [X] T109 [HR] Implement leave approval workflow in /media/ankit/Programming/Projects/python/EMIS/src/services/leave_workflow.py
- [X] T110 [HR] Implement TeacherHierarchyService in /media/ankit/Programming/Projects/python/EMIS/src/services/teacher_hierarchy_service.py

### API
- [X] T111 [HR] Create HR endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/hr.py
- [X] T112 [HR] Create payroll endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/hr.py
- [X] T113 [HR] Create leave management endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/hr.py
- [X] T114 [HR] Document HR API in /media/ankit/Programming/Projects/python/EMIS/docs/api/hr.md

---

## Phase 2: Library Management

### Models (Parallel)
- [X] T115 [P] [LIB] Create Book model with ISBN/barcode in /media/ankit/Programming/Projects/python/EMIS/src/models/book.py
- [X] T116 [P] [LIB] Create LibraryMember model in /media/ankit/Programming/Projects/python/EMIS/src/models/library_member.py
- [X] T117 [P] [LIB] Create Issue model for circulation in /media/ankit/Programming/Projects/python/EMIS/src/models/circulation.py
- [X] T118 [P] [LIB] Create Reservation model in /media/ankit/Programming/Projects/python/EMIS/src/models/circulation.py
- [X] T119 [P] [LIB] Create Fine model in /media/ankit/Programming/Projects/python/EMIS/src/models/circulation.py
- [X] T120 [P] [LIB] Create BookLoss model in /media/ankit/Programming/Projects/python/EMIS/src/models/book_loss.py
- [X] T121 [P] [LIB] Create LibrarySettings model in /media/ankit/Programming/Projects/python/EMIS/src/models/library_settings.py
- [X] T122 [P] [LIB] Create DigitalResource model in /media/ankit/Programming/Projects/python/EMIS/src/models/digital_resource.py

### Services
- [X] T123 [LIB] Implement LibraryService with circulation logic in /media/ankit/Programming/Projects/python/EMIS/src/services/library_service.py
- [X] T124 [LIB] Add faculty borrowing support in /media/ankit/Programming/Projects/python/EMIS/src/services/library_service.py
- [X] T125 [LIB] Implement FineService with configurable rules in /media/ankit/Programming/Projects/python/EMIS/src/services/fine_service.py
- [X] T126 [LIB] Implement BookLossService in /media/ankit/Programming/Projects/python/EMIS/src/services/book_loss_service.py
- [X] T127 [LIB] Add barcode/RFID integration in /media/ankit/Programming/Projects/python/EMIS/src/lib/barcode.py

### API
- [X] T128 [LIB] Create library catalog endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/library.py
- [X] T129 [LIB] Create circulation endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/library.py
- [X] T130 [LIB] Create fine management endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/library.py
- [X] T131 [LIB] Create lost book endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/library.py
- [X] T132 [LIB] Document library API in /media/ankit/Programming/Projects/python/EMIS/docs/api/library.md

---

## Phase 3: Hostel Management

### Models (Parallel)
- [X] T133 [P] [HST] Create Hostel model in /media/ankit/Programming/Projects/python/EMIS/src/models/hostel.py
- [X] T134 [P] [HST] Create Room model in /media/ankit/Programming/Projects/python/EMIS/src/models/hostel.py
- [X] T135 [P] [HST] Create RoomAllocation model in /media/ankit/Programming/Projects/python/EMIS/src/models/hostel.py
- [X] T136 [P] [HST] Create MessMenu model in /media/ankit/Programming/Projects/python/EMIS/src/models/hostel.py
- [X] T137 [P] [HST] Create HostelVisitor model in /media/ankit/Programming/Projects/python/EMIS/src/models/hostel.py
- [X] T138 [P] [HST] Create HostelComplaint model in /media/ankit/Programming/Projects/python/EMIS/src/models/hostel.py

### Services
- [X] T139 [HST] Implement HostelService in /media/ankit/Programming/Projects/python/EMIS/src/services/hostel_service.py
- [X] T140 [HST] Add room allocation logic in /media/ankit/Programming/Projects/python/EMIS/src/services/hostel_service.py
- [X] T141 [HST] Add mess menu management in /media/ankit/Programming/Projects/python/EMIS/src/services/hostel_service.py

### API
- [X] T142 [HST] Create hostel management endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/hostel.py
- [X] T143 [HST] Create room allocation endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/hostel.py
- [X] T144 [HST] Document hostel API in /media/ankit/Programming/Projects/python/EMIS/docs/api/hostel.md

---

## Phase 4: Resource Management

### Models (Parallel)
- [X] T145 [P] [RES] Create InventoryItem model in /media/ankit/Programming/Projects/python/EMIS/src/models/inventory.py
- [X] T146 [P] [RES] Create InventoryCategory model in /media/ankit/Programming/Projects/python/EMIS/src/models/inventory.py
- [X] T147 [P] [RES] Create PurchaseOrder model in /media/ankit/Programming/Projects/python/EMIS/src/models/inventory.py
- [X] T148 [P] [RES] Create Vendor model in /media/ankit/Programming/Projects/python/EMIS/src/models/inventory.py
- [X] T149 [P] [RES] Create StockTransaction model in /media/ankit/Programming/Projects/python/EMIS/src/models/inventory.py

### Services
- [X] T150 [RES] Implement InventoryService in /media/ankit/Programming/Projects/python/EMIS/src/services/inventory_service.py
- [X] T151 [RES] Add stock alert logic in /media/ankit/Programming/Projects/python/EMIS/src/services/inventory_service.py
- [X] T152 [RES] Add purchase workflow in /media/ankit/Programming/Projects/python/EMIS/src/services/inventory_service.py

### API
- [X] T153 [RES] Create inventory endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/inventory.py
- [X] T154 [RES] Create vendor management endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/inventory.py
- [X] T155 [RES] Document inventory API in /media/ankit/Programming/Projects/python/EMIS/docs/api/inventory.md

---

## Phase 5: Transport Management

### Models (Parallel)
- [X] T156 [P] [TRN] Create Vehicle model in /media/ankit/Programming/Projects/python/EMIS/src/models/transport.py
- [X] T157 [P] [TRN] Create Route model in /media/ankit/Programming/Projects/python/EMIS/src/models/transport.py
- [X] T158 [P] [TRN] Create RouteStop model in /media/ankit/Programming/Projects/python/EMIS/src/models/transport.py
- [X] T159 [P] [TRN] Create StudentTransport model in /media/ankit/Programming/Projects/python/EMIS/src/models/transport.py
- [X] T160 [P] [TRN] Create VehicleMaintenance model in /media/ankit/Programming/Projects/python/EMIS/src/models/transport.py

### Services
- [X] T161 [TRN] Implement TransportService in /media/ankit/Programming/Projects/python/EMIS/src/services/transport_service.py
- [X] T162 [TRN] Add route optimization in /media/ankit/Programming/Projects/python/EMIS/src/services/transport_service.py

### API
- [X] T163 [TRN] Create transport management endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/transport.py
- [X] T164 [TRN] Document transport API in /media/ankit/Programming/Projects/python/EMIS/docs/api/transport.md

---

## Phase 6: Event Management

### Models (Parallel)
- [X] T165 [P] [EVT] Create Event model in /media/ankit/Programming/Projects/python/EMIS/src/models/event.py
- [X] T166 [P] [EVT] Create EventRegistration model in /media/ankit/Programming/Projects/python/EMIS/src/models/event.py
- [X] T167 [P] [EVT] Create EventBudget model in /media/ankit/Programming/Projects/python/EMIS/src/models/event.py
- [X] T168 [P] [EVT] Create EventAttendance model in /media/ankit/Programming/Projects/python/EMIS/src/models/event.py

### Services
- [X] T169 [EVT] Implement EventService in /media/ankit/Programming/Projects/python/EMIS/src/services/event_service.py
- [X] T170 [EVT] Add certificate generation in /media/ankit/Programming/Projects/python/EMIS/src/lib/certificate_generator.py

### API
- [X] T171 [EVT] Create event management endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/events.py
- [X] T172 [EVT] Document event API in /media/ankit/Programming/Projects/python/EMIS/docs/api/events.md

---

## Phase 7: Placement Management

### Models (Parallel)
- [X] T173 [P] [PLC] Create Company model in /media/ankit/Programming/Projects/python/EMIS/src/models/placement.py
- [X] T174 [P] [PLC] Create JobPosting model in /media/ankit/Programming/Projects/python/EMIS/src/models/placement.py
- [X] T175 [P] [PLC] Create PlacementApplication model in /media/ankit/Programming/Projects/python/EMIS/src/models/placement.py
- [X] T176 [P] [PLC] Create Interview model in /media/ankit/Programming/Projects/python/EMIS/src/models/placement.py
- [X] T177 [P] [PLC] Create PlacementOffer model in /media/ankit/Programming/Projects/python/EMIS/src/models/placement.py

### Services
- [X] T178 [PLC] Implement PlacementService in /media/ankit/Programming/Projects/python/EMIS/src/services/placement_service.py
- [X] T179 [PLC] Add placement statistics in /media/ankit/Programming/Projects/python/EMIS/src/services/placement_service.py

### API
- [X] T180 [PLC] Create placement endpoints in /media/ankit/Programming/Projects/python/EMIS/src/routes/placement.py
- [X] T181 [PLC] Document placement API in /media/ankit/Programming/Projects/python/EMIS/docs/api/placement.md

---

## Testing & Integration

### Tests (Parallel)
- [X] T182 [P] [TEST] Contract tests for HR endpoints in /media/ankit/Programming/Projects/python/EMIS/tests/contract/test_hr.py
- [X] T183 [P] [TEST] Contract tests for library endpoints in /media/ankit/Programming/Projects/python/EMIS/tests/contract/test_library.py
- [X] T184 [P] [TEST] Contract tests for hostel endpoints in /media/ankit/Programming/Projects/python/EMIS/tests/contract/test_hostel.py
- [X] T185 [P] [TEST] Contract tests for transport endpoints in /media/ankit/Programming/Projects/python/EMIS/tests/contract/test_transport.py
- [X] T186 [P] [TEST] Integration test for HR lifecycle in /media/ankit/Programming/Projects/python/EMIS/tests/integration/test_hr_lifecycle.py
- [X] T187 [P] [TEST] Integration test for library circulation in /media/ankit/Programming/Projects/python/EMIS/tests/integration/test_library_circulation.py

### Database
- [X] T188 [DB] Create migrations for HR models in /media/ankit/Programming/Projects/python/EMIS/alembic/versions/
- [X] T189 [DB] Create migrations for library models in /media/ankit/Programming/Projects/python/EMIS/alembic/versions/
- [X] T190 [DB] Create migrations for operational models in /media/ankit/Programming/Projects/python/EMIS/alembic/versions/

---

## Summary

- **Total Tasks**: 90
- **HR Management**: 14 tasks (Completed ✓)
- **Library Management**: 18 tasks (Completed ✓)
- **Hostel Management**: 12 tasks (Completed ✓)
- **Resource Management**: 11 tasks (Completed ✓)
- **Transport Management**: 9 tasks (Completed ✓)
- **Event Management**: 8 tasks (Completed ✓)
- **Placement Management**: 9 tasks (Completed ✓)
- **Testing**: 6 tasks (Completed ✓)
- **Database**: 3 tasks (Completed ✓)

**Status**: All administrative and operational modules completed ✓
