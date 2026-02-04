# Task Breakdown – Phase III Todo AI Chatbot (Gemini + MCP)

## Legend
- **Prio**: M = Must-have (core functionality), S = Should-have (important polish), N = Nice-to-have (bonus)
- **Size**: XS = <45 min, S = ~1–1.5 h, M = ~2–4 h, L = ~5–7 h
- **Type**: Setup / Deps / Config / Model / Migration / Tool / Agent / API / Frontend / Test / Doc ## Core Tasks

| ID  | Prio | Size | Type      | Component              | Task Title (one clear line)                                      | Prerequisites     | Acceptance Criteria (judge-verifiable bullets)                                                                 |
|-----|------|------|-----------|------------------------|------------------------------------------------------------------|-------------------|---------------------------------------------------------------------------------------------------------------|
| T01 | M    | XS   | Setup     | Repository             | Initialize monorepo: /backend,/frontend, /specs, README stub    | -                 | - Folders created correctly<br>- .gitignore includes Python + Next.js<br>- README has title + stack           |
| T02 | M    | S    | Deps      | Backend                | Add dependencies: fastapi, sqlmodel, alembic, openai-agents, python-dotenv | T01               | - requirements.txt / pyproject.toml correct<br>- Install succeeds<br>- No conflicts                           |
| T03 | M    | S    | Config    | Environment            | Create .env.example with GEMINI_API_KEY + DATABASE_URL           | T02               | - Both keys present with examples<br>- .gitignore ignores .env*<br>- File readable                            |
| T04 | M    | S    | Model     | Database               | Define SQLModel: Task, Conversation, Message + all fields        | T02               | - All required fields & types correct<br>- Indexes on user_id, conversation_id<br>- Role enum present         |
| T05 | M    | S    | Migration | Database               | Setup Alembic + initial migration & apply to Neon                | T04               | - alembic.ini & env.py configured<br>- Migration file generated<br>- Tables visible in Neon                   |
| T06 | M    | M    | Tool      | MCP Tools              | Implement add_task MCP tool (async + JSON schema)                | T04, T05          | - Task created in DB<br>- Returns {"task_id", "status": "created", "title"}<br>- user_id enforced             |
| T07 | M    | M    | Tool      | MCP Tools              | Implement list_tasks with status filter (all/pending/completed)  | T06               | - Returns list of dicts<br>- Correct filter logic<br>- Handles empty result gracefully |
| T08 | M    | S    | Tool      | MCP Tools              | Implement complete_task tool                                     | T07               | - Sets completed=True + updated_at<br>- Returns correct format<br>- Not-found → graceful error                |
| T09 | M    | S    | Tool      | MCP Tools              | Implement delete_task (hard delete)                              | T08               | - Record deleted<br>- Returns "deleted" status<br>- Safe on non-existent task                                 |
| T10 | M    | S    | Tool      | MCP Tools              | Implement update_task (partial title/description update)         | T09               | - Only provided fields updated<br>- Returns updated title<br>- No-op if no changes |
| T11 | M    | M    | Utils     | Agent                  | Create agent_utils.py: Gemini client + agent factory             | T02, T03          | - AsyncOpenAI with gemini base_url<br>- Agent uses gemini-2.5-flash + temp=0.3<br>- Tools injectable          |
| T12 | M    | M    | Agent     | Agent Tools            | Bind 5 MCP tools to agent with correct JSON schemas              | T10, T11          | - agent.tools has 5 items<br>- Schemas match spec<br>- At least one test call succeeds|
| T13 | M    | M    | API       | FastAPI                | Implement POST /api/{user_id}/chat (stateless)                   | T11, T12          | - conversation_id optional<br>- Returns response string + tool_calls array<br>- 200 OK on success             |
| T14 | M    | S    | API       | Persistence            | Store user & assistant messages + handle conversation creation   | T13               | - Messages saved with role/content/timestamp<br>- Conversation ID consistent across calls |
| T15 | M    | M    | Agent     | Context                | Load last 20–25 messages as history for agent                    | T14               | - History in correct [{role, content}] format<br>- New message appended<br>- Context preserved               |
| T16 | M    | S    | API       | Error Handling         | Global exception handler + user-friendly task errors             | T13               | - Task not found → nice message<br>- DB errors logged + 500<br>- Assistant reply includes helpful text       |
| T17 | M    | S    | Frontend  | ChatKit                | Setup Next.js + integrate @openai/chatkit-react                  | T01               | - Chat UI renders<br>- Domain key support added<br>- Basic layout/styling applied                             |
| T18 | M    | S    | Frontend  | Integration            | Connect ChatKit to /api/{user_id}/chat with user_id              | T17               | - user_id passed via header/path<br>- Messages sent & displayed correctly<br>- Responses visible |
| T19 | M    | S    | Test      | E2E Test               | Smoke test: add task → list tasks → verify                       | T12, T15          | - Test passes (real Gemini or mock)<br>- Full tool chain works<br>- DB state correct                          |
| T20 | M    | S    | Doc       | README                 | Write setup instructions (env, migrations, run backend/frontend) | T18               | - Step-by-step: env vars, alembic, uvicorn, next dev<br>- GEMINI_API_KEY warning included                     |
| T21 | M    | S    | Doc       | README                 | Add demo script with 5–6 natural language examples               | T20               | - Examples: add, list, complete, update, delete<br>- Mentions Gemini model usage ## Bonus Tasks (N priority – only if time remains)
- Add pagination to list_tasks
- Implement soft-delete for tasks
- Auto-generate conversation title
- Add loading indicator in ChatKit
- Retry logic on Gemini tool-call failures
- Unit tests for each MCP tool