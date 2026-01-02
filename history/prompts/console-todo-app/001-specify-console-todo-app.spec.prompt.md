---
id: 001
title: Specify Console Todo App
stage: spec
date: 2025-12-30
surface: agent
model: Claude Sonnet 4.5
feature: console-todo-app
branch: 001-console-todo-app
user: user
command: /sp.specify
labels: [spec, todo-app, console, crud]
links:
  spec: specs/001-console-todo-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-console-todo-app/spec.md
 - specs/001-console-todo-app/checklists/requirements.md
tests:
---

## Prompt

```text
Context:
You are implementing Phase I of the project "The Evolution of Todo".
This phase represents the pre-intelligence baseline of the system.

You MUST strictly follow the project's Constitution.
Do NOT invent features, abstractions, or future-phase concepts.

---

Phase:
Phase I — In-Memory Console Todo Application

---

Objective:
Specify the complete behavior and structure of a Python console-based Todo application that operates entirely in memory and supports basic CRUD functionality.

This specification will be used to generate code via Claude Code.
Clarity, completeness, and determinism are mandatory.

--- Functional Requirements:
The system MUST support exactly the following features:

1. Add Task
   - Create a new task with a title and optional description
   - Title must be non-empty
   - Task ID must be auto-incremented

2. View Task List
   - Display all tasks
   - Each task must show:
     - ID
     - Title
     - Description
     - Completion status ([ ] or [x])

3. Update Task
   - Update title and/or description of an existing task
   - Task is selected by ID
   - Invalid IDs must be handled gracefully

4. Delete Task
   - Remove a task by ID
   - Confirmation message must be shown

5. Mark Task as Complete / Incomplete
   - Toggle completion status by ID

No additional features are allowed.

--- Task Model Specification:
Each task MUST contain:
- id: integer (unique, auto-incremented)
- title: string (non-empty)
- description: string (optional)
- completed: boolean

Tasks MUST be stored in an in-memory collection only.

---

CLI Behavior:
- The application MUST run in a loop until the user selects Exit
- A numbered menu MUST be displayed
- User interaction MUST occur via stdin/stdout only
- All input errors MUST be handled without crashing

Example Menu:
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Complete
6. Exit

--- Architectural Constraints:
- Python 3.13+
- No external libraries
- No file I/O
- No database
- No networking
- No async
- No frameworks

Separation of concerns is REQUIRED:
- Task data model
- In-memory storage logic
- CLI interaction logic

Business logic MUST NOT be mixed with input/output handling.

---
 Non-Goals (Explicitly Excluded):
- No priorities
- No tags
- No due dates
- No persistence
- No authentication
- No AI
- No agents
- No skills
- No APIs

--- Output of This Command:
Produce a complete, unambiguous specification that is sufficient for Claude Code to generate the full Phase I implementation without guessing or assumptions.

If any requirement is unclear, STOP and request clarification instead of inventing behavior.
```

## Response snapshot

Created comprehensive feature specification for the console todo application (Phase I) following the project constitution. The specification includes:

- 6 user stories with priorities (P1-P2) covering all required functionality
- Detailed acceptance scenarios for each user story
- 12 functional requirements (FR-001 to FR-012) with specific capabilities
- Task entity definition with required attributes
- 5 measurable success criteria
- Edge cases handling

The specification adheres to architectural constraints:
- In-memory storage only
- Console-based CLI interface
- Python 3.13+ with no external dependencies
- Clear separation of concerns
- No persistence, networking, or frameworks

Quality checklist created and all validation items pass.

## Outcome

- ✅ Impact: High - established complete specification for Phase I implementation
- 🧪 Tests: N/A - specification phase
- 📁 Files: 2 files created (spec.md, requirements.md)
- 🔁 Next prompts: Ready for planning phase with /sp.plan
- 🧠 Reflection: Specification covers all required functionality without exceeding Phase I scope

## Evaluation notes (flywheel)

- Failure modes observed: None - specification complete and compliant
- Graders run and results (PASS/FAIL): All validation items pass
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to planning phase