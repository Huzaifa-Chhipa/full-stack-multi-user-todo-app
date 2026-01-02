---
description: "Task list for Phase I Console Todo Application implementation"
---

# Tasks: Console Todo Application

**Input**: Design documents from `/specs/001-console-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan: mkdir src, src/models, src/services, src/cli
- [x] T002 [P] Create empty __init__.py files in src/, src/models/, src/services/, src/cli/ directories

---
## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 [P] Create Task data model in src/models/task.py with id, title, description, completed attributes
- [x] T004 [P] Implement Task validation for non-empty title in src/models/task.py
- [x] T005 Create TaskManager service in src/services/task_manager.py
- [x] T006 Initialize in-memory storage collection in src/services/task_manager.py
- [x] T007 Implement auto-incrementing ID functionality in src/services/task_manager.py
- [x] T008 Create main CLI application entry point in src/cli/main.py
- [x] T009 Implement continuous application loop in src/cli/main.py
- [x] T010 Add clean application exit functionality in src/cli/main.py
- [x] T011 Implement error handling to prevent crashes in src/cli/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---
## Phase 3: User Story 1 - Add New Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to create new tasks with title and optional description

**Independent Test**: Can be fully tested by adding a task with a title and optionally a description, then verifying it appears in the task list with an auto-incremented ID and incomplete status.

### Implementation for User Story 1

- [x] T012 [P] [US1] Implement add_task method in src/services/task_manager.py to create tasks with auto-incremented IDs
- [x] T013 [P] [US1] Implement title validation in src/services/task_manager.py to ensure non-empty titles
- [x] T014 [US1] Implement Add Task menu option in src/cli/main.py
- [x] T015 [US1] Add user input capture for title and description in src/cli/main.py
- [x] T016 [US1] Connect CLI Add Task to TaskManager add_task method in src/cli/main.py
- [x] T017 [US1] Add error message display for empty title input in src/cli/main.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---
## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Goal**: Allow users to see all their tasks at once with ID, title, description, and completion status

**Independent Test**: Can be fully tested by adding several tasks, then viewing the task list to verify all tasks are displayed with correct IDs, titles, descriptions, and completion status.

### Implementation for User Story 2

- [x] T018 [P] [US2] Implement get_all_tasks method in src/services/task_manager.py to retrieve all tasks
- [x] T019 [P] [US2] Implement list formatting to display tasks with ID, title, description, and completion status ([ ] or [x])
- [x] T020 [US2] Implement View Tasks menu option in src/cli/main.py
- [x] T021 [US2] Connect CLI View Tasks to TaskManager get_all_tasks method in src/cli/main.py
- [x] T022 [US2] Format and display task list with proper completion status symbols in src/cli/main.py
- [x] T023 [US2] Handle case when no tasks exist to display appropriate message in src/cli/main.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---
## Phase 5: User Story 5 - Mark Tasks Complete/Incomplete (Priority: P1)

**Goal**: Allow users to toggle the completion status of tasks by ID

**Independent Test**: Can be fully tested by adding tasks, marking them complete/incomplete, then verifying the status changes are reflected in the task list.

### Implementation for User Story 5

- [x] T024 [P] [US5] Implement toggle_task_completion method in src/services/task_manager.py
- [x] T025 [P] [US5] Add validation for valid task ID in toggle_task_completion method in src/services/task_manager.py
- [x] T026 [US5] Implement Mark Complete menu option in src/cli/main.py
- [x] T027 [US5] Add user input capture for task ID in src/cli/main.py
- [x] T028 [US5] Connect CLI Mark Complete to TaskManager toggle_task_completion method in src/cli/main.py
- [x] T029 [US5] Add error handling for invalid task IDs in src/cli/main.py

**Checkpoint**: At this point, User Stories 1, 2, AND 5 should all work independently

---
## Phase 6: User Story 3 - Update Existing Tasks (Priority: P2)

**Goal**: Allow users to modify the title or description of an existing task when their requirements change

**Independent Test**: Can be fully tested by adding a task, updating its title and/or description, then verifying the changes are reflected in the task list.

### Implementation for User Story 3

- [x] T030 [P] [US3] Implement update_task method in src/services/task_manager.py for partial updates
- [x] T031 [P] [US3] Add validation for non-empty title in update_task method in src/services/task_manager.py
- [x] T032 [US3] Implement Update Task menu option in src/cli/main.py
- [x] T033 [US3] Add user input capture for task ID, new title, and new description in src/cli/main.py
- [x] T034 [US3] Connect CLI Update Task to TaskManager update_task method in src/cli/main.py
- [x] T035 [US3] Add error handling for invalid task IDs in src/cli/main.py
- [x] T036 [US3] Implement functionality to retain existing values when inputs are empty in src/cli/main.py

**Checkpoint**: At this point, User Stories 1, 2, 5, AND 3 should all work independently

---
## Phase 7: User Story 4 - Delete Tasks (Priority: P2)

**Goal**: Allow users to remove tasks that are no longer needed

**Independent Test**: Can be fully tested by adding tasks, deleting one, then verifying it no longer appears in the task list while others remain.

### Implementation for User Story 4

- [x] T037 [P] [US4] Implement delete_task method in src/services/task_manager.py
- [x] T038 [P] [US4] Add validation for valid task ID in delete_task method in src/services/task_manager.py
- [x] T039 [US4] Implement Delete Task menu option in src/cli/main.py
- [x] T040 [US4] Add user input capture for task ID in src/cli/main.py
- [x] T041 [US4] Connect CLI Delete Task to TaskManager delete_task method in src/cli/main.py
- [x] T042 [US4] Add confirmation message display after successful deletion in src/cli/main.py
- [x] T043 [US4] Add error handling for invalid task IDs in src/cli/main.py

**Checkpoint**: At this point, User Stories 1, 2, 5, 3, AND 4 should all work independently

---
## Phase 8: User Story 6 - Exit Application (Priority: P1)

**Goal**: Provide a clean exit option when users are done managing their tasks

**Independent Test**: Can be fully tested by selecting the exit option and verifying the application terminates.

### Implementation for User Story 6

- [x] T044 [US6] Implement Exit menu option in src/cli/main.py
- [x] T045 [US6] Ensure application terminates cleanly when Exit option is selected in src/cli/main.py

**Checkpoint**: All user stories should now be independently functional

---
## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T046 [P] Complete menu display with all options: Add Task, View Tasks, Update Task, Delete Task, Mark Complete, Exit in src/cli/main.py
- [x] T047 [P] Implement menu input validation to handle invalid selections gracefully in src/cli/main.py
- [x] T048 [P] Add comprehensive error handling for all invalid user inputs in src/cli/main.py
- [x] T049 [P] Ensure tasks are displayed in ascending order of task ID in src/services/task_manager.py
- [x] T050 [P] Verify no file I/O, database, or network usage exists in any module
- [x] T051 [P] Verify no agents, skills, APIs, or async logic exist in any module
- [x] T052 [P] Run manual testing scenarios based on spec acceptance criteria

---
## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in priority order (P1 → P2)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 5 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 6 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

- Core implementation before menu integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, user stories can be worked on in priority order
- All tasks within a user story marked [P] can run in parallel if they're in different files

---
## Implementation Strategy

### MVP First (User Stories 1, 2, 5, 6 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Add Tasks)
4. Complete Phase 4: User Story 2 (View Tasks)
5. Complete Phase 5: User Story 5 (Mark Complete)
6. Complete Phase 8: User Story 6 (Exit Application)
7. **STOP and VALIDATE**: Test core functionality independently
8. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Stories 1, 2, 5, 6 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 3 → Test independently → Deploy/Demo
4. Add User Story 4 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

---
## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence