# Data Model: Full-Stack Multi-User Web Todo Application

## Entity: Task
**Description**: Represents a user's todo item with all required attributes

**Fields**:
- `id` (integer): Primary key, auto-incremented
- `user_id` (string): Foreign key referencing Better Auth user ID
- `title` (string): Required, 1-200 characters
- `description` (string): Optional, max 1000 characters
- `completed` (boolean): Default false
- `created_at` (timestamp): Auto-generated
- `updated_at` (timestamp): Auto-generated, updated on changes

**Validation Rules**:
- Title must be 1-200 characters (required)
- Description must be max 1000 characters (optional)
- completed defaults to false
- user_id must match authenticated user's ID from JWT

## Entity: User (via Better Auth)
**Description**: Represents an authenticated user account, managed by Better Auth system

**Fields**:
- `user_id` (string): Unique identifier from Better Auth
- `email` (string): User's email address
- `tasks` (relationship): One-to-many relationship with Task entity

## Relationships
- One User to Many Tasks (user_id foreign key in Task table)
- Tasks are filtered by user_id for proper data isolation

## State Transitions
- Task completion: `completed` field toggles between true/false
- Task creation: new record with completed=false by default
- Task updates: updated_at timestamp automatically updated