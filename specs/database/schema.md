# Database Schema: Full-Stack Multi-User Web Todo Application

## Overview
This document specifies the database schema for the todo application using PostgreSQL with SQLModel. The schema supports multi-user functionality with proper data isolation.

## Database Configuration
- **Database**: PostgreSQL (via Neon Serverless)
- **ORM**: SQLModel (SQLAlchemy + Pydantic)
- **Connection**: Environment variable DATABASE_URL

## Tables

### tasks
**Description**: Stores user todo tasks with ownership information

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique task identifier |
| user_id | STRING | NOT NULL, INDEX | Better Auth user ID (foreign key reference) |
| title | STRING (200) | NOT NULL, LENGTH(1-200) | Task title (1-200 characters) |
| description | STRING (1000) | NULL | Task description (max 1000 characters) |
| completed | BOOLEAN | NOT NULL, DEFAULT false | Completion status |
| created_at | TIMESTAMP | NOT NULL, DEFAULT now() | Record creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT now(), ON UPDATE now() | Record update timestamp |

**Indexes**:
- `idx_user_id`: Index on user_id for efficient user-based queries
- `idx_user_id_completed`: Composite index on user_id and completed for filtered queries

**Foreign Keys**:
- user_id references Better Auth user system (managed externally)

**Constraints**:
- Title length: 1-200 characters
- Description length: max 1000 characters
- completed defaults to false
- created_at and updated_at automatically managed

## Schema Implementation

```python
from sqlmodel import SQLModel, Field, create_engine, Session
from datetime import datetime
from typing import Optional

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

## Data Isolation Strategy
- All queries must filter by user_id to ensure data isolation
- API layer enforces user_id validation against JWT claims
- Database-level isolation is supplemented by application-level validation
- No direct cross-user access is permitted through the API

## Migration Strategy
- Initial schema creation via SQLModel's table creation
- Future schema changes managed through migration scripts
- Environment-specific configuration via DATABASE_URL