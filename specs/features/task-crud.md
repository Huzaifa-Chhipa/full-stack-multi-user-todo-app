# Feature: Task CRUD Operations

## Overview
This feature implements the core task management functionality allowing users to create, read, update, delete, and toggle completion status of their todo tasks.

## User Stories
- As a user, I want to create tasks with title and description so that I can track my todos
- As a user, I want to view my tasks so that I can see what I need to do
- As a user, I want to update my tasks so that I can modify them as needed
- As a user, I want to delete my tasks so that I can remove completed or irrelevant items
- As a user, I want to mark tasks as complete/incomplete so that I can track my progress

## Functional Requirements
1. **Create Task**: POST /api/{user_id}/tasks
   - Accept title (1-200 chars) and description (max 1000 chars)
   - Associate task with authenticated user
   - Return 201 Created with task data

2. **List Tasks**: GET /api/{user_id}/tasks
   - Return only tasks belonging to authenticated user
   - Order by created_at descending (newest first)
   - Return 200 OK with task list

3. **Get Task**: GET /api/{user_id}/tasks/{id}
   - Return specific task if it belongs to authenticated user
   - Return 404 if task doesn't exist or belongs to another user

4. **Update Task**: PUT /api/{user_id}/tasks/{id}
   - Update title/description if task belongs to authenticated user
   - Validate title/description fields
   - Return 200 OK with updated task

5. **Delete Task**: DELETE /api/{user_id}/tasks/{id}
   - Delete task if it belongs to authenticated user
   - Return 204 No Content

6. **Toggle Completion**: PATCH /api/{user_id}/tasks/{id}/complete
   - Toggle completion status if task belongs to authenticated user
   - Return updated task with new completion status

## Validation Rules
- Title: 1-200 characters (required)
- Description: max 1000 characters (optional)
- User ownership verification required for all operations
- Task ID must exist and belong to authenticated user

## Error Handling
- 400 Bad Request: Invalid input data
- 401 Unauthorized: Invalid/missing JWT
- 404 Not Found: Task doesn't exist or belongs to another user
- 422 Unprocessable Entity: Validation errors