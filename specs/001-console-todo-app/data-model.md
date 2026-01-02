# Data Model: Console Todo Application

## Task Entity

### Attributes
- **id**: integer
  - Type: int
  - Constraints: Unique, auto-incremented, positive
  - Purpose: Unique identifier for each task

- **title**: string
  - Type: str
  - Constraints: Non-empty, required
  - Purpose: Descriptive name of the task

- **description**: string
  - Type: str
  - Constraints: Optional, can be empty
  - Purpose: Additional details about the task

- **completed**: boolean
  - Type: bool
  - Constraints: Required, defaults to False
  - Purpose: Indicates completion status of the task

### Validation Rules
1. **Title validation**: Title must not be empty or contain only whitespace
2. **ID uniqueness**: Each task must have a unique ID
3. **ID auto-increment**: New tasks receive the next available ID
4. **Completion state**: Boolean value representing completion status

### State Transitions
- **Initial state**: completed = False
- **Toggle operation**: completed = !completed (switches between True and False)

## Data Relationships
- No relationships needed as this is a single-entity system
- All tasks are independent of each other

## Storage Model
- **In-memory collection**: Python list of Task objects
- **ID mapping**: Optional dictionary for O(1) lookup by ID
- **Auto-increment counter**: Integer tracking next available ID