# Development Plan – Todo AI Chatbot (Phase III)

## 0. Project Overview & Success Criteria

The Todo AI Chatbot (Phase III) implements a natural language interface for managing todo tasks using Google Gemini AI with MCP (Model Context Protocol) tools. The system follows the constitutional requirement that AI serves as a coordinator using standardized tools rather than containing business logic. The architecture maintains statelessness while providing conversational context through external storage.

**Success Criteria:**
- **SC-001**: Users can successfully manage tasks through natural language with 90% accuracy for common commands
- **SC-002**: 85% of users complete their intended task management operation within 3 conversation turns
- **SC-003**: System responds to user messages within 5 seconds for 95% of interactions
- **SC-004**: User satisfaction rating for the chatbot interface is 4.0/5.0 or higher
- **SC-005**: 80% of users who try the chatbot feature use it again within the following week

## 1. Milestones & Timeline (hackathon-style: assume 2–4 days left)

- **Day 1 / Morning** – Set up project structure, database models, and authentication integration
- **Day 1 / Afternoon** – Implement MCP tools server and core task operations
- **Day 2 / Morning** – Develop FastAPI chat endpoint and agent runner with Gemini integration
- **Day 2 / Afternoon** – Build OpenAI ChatKit frontend and integrate with backend
- **Final polish & demo prep** – Testing, bug fixes, and prepare demo flow

## 2. Work Streams (parallelizable areas)

### 2.1 Database & Auth Foundation
- **Objective**: Set up conversation/message storage and integrate with Better Auth
- **Key deliverables**: Database models, migration scripts, auth middleware
- **Dependencies**: None
- **Estimated effort**: 2 Claude Code sessions (~4 hours)
- **Risk level**: Low - using established SQLModel and Better Auth patterns
- **Mitigation**: Follow existing auth patterns from Phase II
- **Validation method**: Verify JWT extraction from Better Auth context and database connectivity

### 2.2 MCP Tools Server
- **Objective**: Create standardized MCP tools for task operations (add, list, complete, delete, update)
- **Key deliverables**: MCP tool definitions, task operation handlers, error handling
- **Dependencies**: 2.1 (needs auth and db access)
- **Estimated effort**: 3 Claude Code sessions (~6 hours)
- **Risk level**: High - MCP tool integration complexity
- **Mitigation**: Start with simple tool implementation, test incrementally
- **Validation method**: Call each MCP tool directly with test parameters and verify database changes

### 2.3 FastAPI + Agent Runner
- **Objective**: Implement stateless chat endpoint that orchestrates conversation with Gemini agent
- **Key deliverables**: FastAPI routes, agent runner, conversation state management
- **Dependencies**: 2.1, 2.2 (needs auth/db and MCP tools)
- **Estimated effort**: 3 Claude Code sessions (~6 hours)
- **Risk level**: High - complex AI integration with tool calling
- **Mitigation**: Use Gemini-2.5-flash for faster iteration, implement error handling
- **Validation method**: Send test messages to endpoint and verify agent responses with tool calls

### 2.4 OpenAI ChatKit Frontend
- **Objective**: Create user-friendly chat interface that connects to backend API
- **Key deliverables**: ChatKit integration, authentication flow, conversation display
- **Dependencies**: 2.3 (needs working backend API)
- **Estimated effort**: 2 Claude Code sessions (~4 hours)
- **Risk level**: Medium - external library integration
- **Mitigation**: Follow ChatKit documentation closely, implement fallback UI
- **Validation method**: User can start conversation, send messages, and see AI responses in chat UI

### 2.5 Testing & Polish
- **Objective**: Integrate all components, test end-to-end flows, optimize performance
- **Key deliverables**: Integration tests, error handling, performance tuning
- **Dependencies**: All other streams
- **Estimated effort**: 2 Claude Code sessions (~4 hours)
- **Risk level**: Medium - integration complexities
- **Mitigation**: Test early and often, implement logging for debugging
- **Validation method**: Complete end-to-end scenarios work smoothly from UI to database

## 3. Technology Decisions & Justifications

- **Using SQLModel → Alembic for migrations**: Following established patterns from Phase II for consistency and reliability
- **Storing conversation state: Separate message rows**: Enables rich querying and pagination as specified in clarifications
- **Agent loop: Tool-calling loop with Gemini**: Leverages Gemini's strong tool-calling capabilities for MCP integration
- **Error handling strategy: Structured error responses**: Provides clear feedback to users when operations fail
- **Rate limiting: Minimal implementation**: Basic per-user rate limiting to prevent abuse during demo
- **Gemini API integration: OpenAI-compatible endpoint**: Cost-effective solution that judges accept when documented
- **Better Auth integration: Session context extraction**: Follows existing authentication patterns from Phase II
- **Soft-delete for tasks: Mark as deleted**: Preserves data integrity and enables undo functionality
- **Pagination threshold: 50+ tasks**: Optimizes performance while maintaining usability
- **Conversation context window: Last 20 messages**: Balances context awareness with performance
- **MCP Tool validation: Parameter validation at entry point**: Prevents invalid operations from reaching database
- **Frontend state management: ChatKit managed state**: Leverages library capabilities for optimal user experience

## 4. Claude Code Prompt Strategy

- **Implementation passes**: Expect 2-3 passes per major component (design, implementation, refinement)
- **Best prompts for this stack**: Specify exact requirements, provide code examples from existing codebase, define clear acceptance criteria
- **Debugging loops**: Create minimal reproducible examples, test components in isolation before integration, use structured logging

## 5. Risks & Contingency

- **Risk 1**: Gemini API rate limits or unavailability
  - **Fallback**: Implement mock agent responses for demo purposes
- **Risk 2**: MCP tool integration complexity exceeding timeline
  - **Fallback**: Simplify to direct API calls while maintaining tool interface compatibility
- **Risk 3**: Authentication integration conflicts with existing system
  - **Fallback**: Implement minimal JWT verification as backup
- **Risk 4**: ChatKit integration proves too complex
  - **Fallback**: Build simple custom chat interface with standard React components
- **Risk 5**: Database performance issues with conversation history
  - **Fallback**: Implement simplified conversation storage for demo

## 6. Demo Flow Outline

1. **Login** to application using existing auth
2. **Start new conversation** with AI chatbot
3. **Add task**: "Add a task to buy groceries"
4. **List tasks**: "Show me my tasks" - see the new task
5. **Complete task**: "Mark the grocery task as complete"
6. **Verify**: Show tasks again to confirm completion
7. **Handle error**: Try to delete invalid task ID - see helpful error message
8. **Demonstrate context**: "Update the grocery task to add milk" - see context recognition