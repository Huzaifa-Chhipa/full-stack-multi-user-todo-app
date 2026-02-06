# Natural Language Commands Configuration

## Overview
Your todo application features a sophisticated AI-powered chatbot that can understand and respond to natural language commands in multiple formats. The system supports English, Hindi, Urdu, and mixed language expressions.

## Supported Commands

### 1. Add Task
**User Says:** "Add a task to buy groceries"
**Agent Calls:** `add_task` with title "buy groceries"

**Alternative Formats:**
- "task add kro name buy groceries"
- "add task to buy groceries"
- "create task buy groceries"
- "bnana hai name groceries"

### 2. List Tasks
**User Says:** "Show me all my tasks"
**Agent Calls:** `list_tasks` with status "all"

**Alternative Formats:**
- "Show me all my tasks"
- "mere sab tasks dikhao"
- "what are my tasks?"
- "list all tasks"
- "show me my todo list"

### 3. List Pending Tasks
**User Says:** "What's pending?"
**Agent Calls:** `list_tasks` with status "pending"

**Alternative Formats:**
- "What's pending?"
- "show pending tasks"
- "which tasks are incomplete?"

### 4. Complete Task
**User Says:** "Mark task 3 as complete"
**Agent Calls:** `complete_task` with task_id 3

**Alternative Formats:**
- "Mark task 3 as complete"
- "complete task 3"
- "finish task 3"
- "task 3 ko complete krdo"
- "complete the groceries task" (by name matching)

### 5. Delete Task
**User Says:** "Delete the meeting task"
**Agent Calls:** `list_tasks` first, then `delete_task` by name matching

**Alternative Formats:**
- "Delete the meeting task"
- "delete task 3"
- "task delete kro meeting wlaa"
- "meeting ke naam se jo task he usko delete kro"
- "meeting ko delete kro"

### 6. Update Task
**User Says:** "Change task 1 to 'Call mom tonight'"
**Agent Calls:** `update_task` with new title

**Alternative Formats:**
- "Change task 1 to 'Call mom tonight'"
- "update task 1 to call mom tonight"
- "modify task 1 title to call mom tonight"

### 7. Remember Task
**User Says:** "I need to remember to pay bills"
**Agent Calls:** `add_task` with title "pay bills"

## Command Processing Flow

### 1. Primary Processing (Advanced NLP with Gemini)
- Uses `AdvancedNLPTaskParser` class
- Supports multilingual expressions (English/Hindi/Urdu/mixed)
- Handles complex expressions like "X ke naam se jo task he usko delete kro"
- Falls back to secondary processing if Gemini fails

### 2. Secondary Processing (Local NLP)
- Uses `TodoAgent` class
- Local processing without external API dependencies
- Handles common patterns and expressions
- Ensures reliability even when Gemini is unavailable

### 3. Intent Detection
The system recognizes these intents:
- **Add:** `task add kro`, `add task`, `create task`, `bnana`, `bnaye`, `krdo`
- **Delete:** `task delete kro`, `delete task`, `remove task`, `hatao`, `nikalo`, `hatana`
- **Complete:** `complete task`, `finish task`, `done task`, `ho gya`, `ho gaya`, `kr diya`
- **List:** `my tasks`, `all tasks`, `show tasks`, `list tasks`, `tasks dikhao`, `mere tasks`

### 4. Task Name Extraction
The system uses multiple patterns to extract task names:
- After "task add kro name X"
- After "task delete kro X wlaa"
- From "X ke naam se jo task he usko delete kro"
- From "X ko complete kro"
- General name extraction from context

## Configuration Options

### Environment Variables
- `GEMINI_API_KEY`: API key for Google's Gemini service (enables advanced NLP)

### System Behavior
1. **Primary:** Attempts to use Gemini-powered advanced NLP
2. **Fallback:** Uses local NLP processing if Gemini fails
3. **Multilingual Support:** Handles English, Hindi, Urdu, and mixed expressions
4. **Smart Matching:** Finds tasks by name when IDs aren't provided
5. **Context Awareness:** Maintains conversation context across interactions

## Optimization Recommendations

### 1. Improve Accuracy
- Add more training phrases for edge cases
- Fine-tune regex patterns for your specific use cases
- Consider implementing fuzzy matching for task names

### 2. Extend Functionality
- Add due date support: "Add task to buy groceries by Friday"
- Add priority levels: "Add high priority task to call doctor"
- Add categorization: "Add work task to prepare presentation"

### 3. Performance
- Cache frequently used patterns
- Optimize regex expressions for faster processing
- Consider using more efficient NLP libraries if needed

## Troubleshooting

### Common Issues
1. **Task Not Found:** The system will list available tasks when a named task isn't found
2. **Ambiguous Commands:** The system asks for clarification when intent is unclear
3. **API Failures:** Automatic fallback to local processing ensures continued operation

### Debugging
- Check logs in `backend/src/todo_agent.py` for processing details
- Monitor API response times for Gemini integration
- Verify environment variables are properly set

## Integration Points

### Frontend
- `frontend/src/components/ChatbotWidget.tsx` - UI component
- `frontend/src/services/api.ts` - API service with `chatWithAssistant` method

### Backend
- `backend/src/api/chat.py` - Main chat API endpoint
- `backend/src/todo_agent.py` - Primary local NLP processing
- `backend/src/advanced_agent_utils.py` - Gemini-powered processing
- `backend/advanced_nlp_parser.py` - Advanced multilingual parsing
- `backend/super_flexible_assistant.py` - OpenAI assistant alternative
- `backend/src/tools/task_tools.py` - Actual task operations

The system is already configured to handle all the commands you specified and much more!