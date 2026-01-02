# Implementation Plan: Console Todo Application

**Branch**: `001-console-todo-app` | **Date**: 2025-12-30 | **Spec**: [specs/001-console-todo-app/spec.md](specs/001-console-todo-app/spec.md)
**Input**: Feature specification from `/specs/001-console-todo-app/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a Phase I in-memory console todo application that provides basic CRUD functionality for task management. The application follows the CLI-only, in-memory constraint requirements from the project constitution, providing a menu-driven interface for users to add, view, update, delete, and mark tasks as complete/incomplete.

## Technical Context

**Language/Version**: Python 3.13+ (as specified in constitution)
**Primary Dependencies**: None (no external libraries per constitution)
**Storage**: In-memory only (no persistence as per constitution)
**Testing**: Manual testing through user interactions (no formal testing framework per constitution)
**Target Platform**: Cross-platform (Python console application)
**Project Type**: Single console application - determines source structure
**Performance Goals**: Sub-3 second response time for all user interactions (per spec SC-003)
**Constraints**: <100MB memory usage for 100 tasks (per spec SC-004), no crash on invalid input (per spec SC-002)
**Scale/Scope**: Single-user console application supporting up to 100 tasks (per spec SC-004)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ Phase I compliance: CLI only (stdin/stdout), in-memory data only, single process
- ✅ No persistence: No file I/O, database, or network usage as required
- ✅ No external frameworks: Pure Python without external libraries
- ✅ Single responsibility: Clear separation between data model, storage, and CLI
- ✅ Loose coupling: Components interact through well-defined interfaces
- ✅ Explicit boundaries: Clear separation between business logic and I/O handling
- ✅ No future-phase concepts: No database, auth, networking, or async features

## Project Structure

### Documentation (this feature)

```text
specs/001-console-todo-app/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── models/
│   └── task.py          # Task data model with validation
├── services/
│   └── task_manager.py  # In-memory storage and task operations
└── cli/
    └── main.py          # Main CLI application with menu loop

tests/
└── manual/              # Manual test scenarios based on spec acceptance criteria
```

**Structure Decision**: Single project structure selected with clear separation of concerns:
- `models/` contains the Task data model with validation logic
- `services/` contains the TaskManager for in-memory storage operations
- `cli/` contains the main application with user interface logic

## Core Components Design

### 1. Task Model (`src/models/task.py`)
- **Purpose**: Represents a single todo task with validation
- **Responsibilities**:
  - Define task structure (id, title, description, completed)
  - Validate title is non-empty
  - Provide string representation for display
- **Dependencies**: None (pure data class)
- **Must NOT know about**: Storage, CLI, or user interactions

### 2. Task Manager (`src/services/task_manager.py`)
- **Purpose**: Manages in-memory collection of tasks
- **Responsibilities**:
  - Store tasks in memory
  - Add new tasks with auto-incremented IDs
  - Retrieve, update, and delete tasks by ID
  - Toggle completion status
  - Validate task operations
- **Dependencies**: Task model (`src/models/task.py`)
- **Must NOT know about**: CLI or user interface concerns

### 3. CLI Application (`src/cli/main.py`)
- **Purpose**: Provides console interface for user interactions
- **Responsibilities**:
  - Display menu options
  - Handle user input
  - Call appropriate task manager methods
  - Display results to user
  - Handle errors gracefully
- **Dependencies**: Task manager (`src/services/task_manager.py`)
- **Must NOT know about**: Internal storage implementation details

## Control Flow

### Application Startup
1. Initialize TaskManager instance
2. Enter main menu loop
3. Display numbered menu options to user

### Menu Display Loop
1. Show menu options: Add Task, View Tasks, Update Task, Delete Task, Mark Complete, Exit
2. Get user selection
3. Validate selection
4. Dispatch to appropriate handler
5. Return to menu (except for Exit)

### User Input Processing
1. Get input from stdin
2. Validate input type (number, string, etc.)
3. Convert to appropriate format
4. Pass to business logic layer
5. Handle validation errors gracefully

### Dispatching to Task Operations
1. Based on user selection, call appropriate TaskManager method
2. Handle any errors from business logic
3. Format and display results to user
4. Continue loop or exit based on selection

### Graceful Exit
1. When user selects Exit, terminate the application cleanly
2. No cleanup needed (in-memory only)

## Data Flow

### From User Input → Validation
1. User enters data via stdin
2. CLI component validates input format (numbers, non-empty strings, etc.)
3. If valid, passes to TaskManager
4. If invalid, displays error and returns to menu

### Into Task Storage
1. CLI calls TaskManager methods with validated data
2. TaskManager creates Task objects (with validation)
3. TaskManager stores in internal collection
4. Auto-increment ID is assigned during storage

### Back to User Output
1. TaskManager returns results to CLI
2. CLI formats data for display
3. Results shown to user via stdout
4. Appropriate status messages displayed

### Boundaries Between Business Logic and I/O
- **Business Logic** (TaskManager): Handles operations, validation, storage
- **I/O Handling** (CLI): Handles user interaction, formatting, error display
- Clear separation: Business logic never handles stdin/stdout directly

## Error Handling Strategy

### Where Input Validation Occurs
- CLI layer validates input format (numbers, non-empty strings)
- TaskManager validates business rules (valid IDs, non-empty titles)

### How Invalid IDs Are Handled
- TaskManager checks if ID exists before operations
- Returns appropriate error indication to CLI
- CLI displays user-friendly error message

### How Application Avoids Crashes
- Try-catch blocks around user input operations
- Validation before attempting operations
- Graceful fallback for all error conditions

### How Errors Are Reported to User
- Clear, descriptive error messages
- Return to main menu after errors
- No crash or unexpected termination

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None      | None       | All constitution requirements satisfied |
