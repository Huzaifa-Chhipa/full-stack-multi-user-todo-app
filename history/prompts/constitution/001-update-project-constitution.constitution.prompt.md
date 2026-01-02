---
id: 001
title: Update Project Constitution
stage: constitution
date: 2025-12-30
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: master
user: user
command: /sp.constitution
labels: [constitution, governance, todo-app]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
---

## Prompt

```text
# Constitution — The Evolution of Todo
Version: 1.0
Authority Level: Absolute
Applies To: All Phases (I → V)

---

## 1. Purpose (WHY) This project demonstrates the **real-world evolution of software systems**:
from a single-process CLI script to a **distributed, cloud-native, AI-powered system**.

The goal is NOT feature completion.
The goal is to demonstrate:
- Architectural thinking
- Spec-driven discipline
- Agent-governed development
- Progressive system evolution

All decisions must support this objective.

--- ## 2. Absolute Development Law

❗ **NO SPEC → NO CODE**

Under no circumstances may any AI agent or human:
- Write code
- Modify code
- Refactor architecture
- Add features

without an explicit, written, and approved specification.

Hierarchy of Authority:
1. Constitution (this file)
2. Specifications (`/specs`)
3. Plans
4. Tasks
5. Implementation

Higher levels override lower ones.

--- ## 3. Agentic Development Rules

This project uses **AI agents as builders**, not improvisers.

All agents (Claude Code or otherwise) MUST:
- Follow the lifecycle: **Specify → Plan → Tasks → Implement**
- Refuse to generate code if a task is missing
- Refuse to invent requirements
- Refuse to infer architecture not explicitly stated

If something is unclear, the agent must STOP and request a spec update.

---
 ## 4. Phase Integrity Rule

Each phase is **strictly isolated**.

### Forbidden Behavior
- Using future-phase concepts early
- Adding scalability hooks "just in case"
- Writing code intended for later phases

### Example Violations
- Database logic in Phase I ❌
- Auth logic in Phase I ❌
- API abstractions in Phase I ❌
- Kafka/Dapr placeholders before Phase V ❌

Each phase must be:
- Complete
- Minimal
- Purpose-built for its learning objective

---
## 5. Phase Constraints (Non-Negotiable)

### Phase I — Console / In-Memory
- CLI only (stdin/stdout)
- In-memory data only
- Single process
- No persistence
- No network
- No async
- No frameworks
- Python 3.13+

Purpose: **Logic, separation of concerns, discipline**

--- ### Phase II — Full-Stack Web
- REST APIs only
- Persistent storage (PostgreSQL)
- User isolation via JWT
- Stateless backend
- Clear frontend/backend separation

Purpose: **Multi-user systems & contracts**

---

### Phase III — AI Chatbot
- Natural language interface
- MCP tools as the ONLY way AI mutates state
- Stateless API
- Conversation state stored externally
- AI is a coordinator, NOT a god object

Purpose: **AI as an interface, not business logic**

--- ### Phase IV — Local Kubernetes
- Containerized services
- Helm-managed deployment
- No manual kubectl YAML hacking
- AI-assisted DevOps tools allowed

Purpose: **Cloud-native thinking**

---

### Phase V — Production Cloud + Events
- Event-driven architecture (Kafka)
- Dapr for abstraction
- Horizontal scalability
- Observability and CI/CD

Purpose: **Distributed systems mastery**

--- ## 6. Architectural Principles

The system MUST follow these principles:

- **Single Responsibility**
- **Loose Coupling**
- **Explicit Boundaries**
- **Stateless Services**
- **Event-Driven Communication (when applicable)**

Violations are considered architectural defects.

---

## 7. AI Usage Rules

AI is a **builder**, not a designer.

AI agents:
- Execute specs
- Implement tasks
- Enforce consistency

AI agents MUST NOT:
- Invent UX
- Invent APIs
- Invent schemas
- Invent workflows

All creativity belongs in the specification phase — not implementation.

---
## 8. Prohibited Shortcuts

The following are explicitly forbidden:
- "Temporary" hacks
- "We'll fix later" code
- Commented-out future logic
- Overengineering
- Premature optimization

Judges care about **clarity**, not cleverness.

---

## 9. Review Criteria Alignment

The project will be evaluated on:
- Spec quality
- Architectural clarity
- Phase discipline
- Agent usage correctness
- Evolution consistency

Feature completeness is secondary ## 10. Final Authority

This Constitution overrides:
- README instructions
- AI suggestions
- Developer assumptions
- Convenience-driven decisions

If there is conflict:
**The Constitution wins. Always.**
```

## Response snapshot

Updated the project constitution at `.specify/memory/constitution.md` with the comprehensive Todo Evolution Constitution, replacing the template placeholders with the specified content. The new constitution establishes the foundational governance for the project's evolution through 5 phases, from a console-based in-memory application to a distributed, cloud-native system.

Key changes made:
1. Replaced the template constitution with the detailed Todo Evolution Constitution
2. Added version 1.0.0 and ratification date (2025-12-30)
3. Included all 10 sections from the user's specification
4. Added governance section with amendment procedures
5. Created sync impact report at the top of the file

The constitution now serves as the authoritative governance document for the Todo Evolution project, establishing the rules and constraints for each phase of development.

## Outcome

- ✅ Impact: High - established foundational governance for the entire project lifecycle
- 🧪 Tests: N/A - no functional changes, only governance
- 📁 Files: 1 file updated (.specify/memory/constitution.md)
- 🔁 Next prompts: Feature specification can now be created following the constitution
- 🧠 Reflection: Constitution provides clear phase boundaries and development constraints

## Evaluation notes (flywheel)

- Failure modes observed: None - successful constitution update
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin feature specification following constitution guidelines