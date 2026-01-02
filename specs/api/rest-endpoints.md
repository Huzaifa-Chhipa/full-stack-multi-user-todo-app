# API Specification: REST Endpoints

## Overview
This document specifies the REST API endpoints for the full-stack multi-user web todo application. All endpoints require JWT authentication in the Authorization header.

## Authentication
All API endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

## Base URL
```
http://localhost:8000/api/{user_id}/
```

## Endpoints

### Task Management

#### Create Task
```
POST /api/{user_id}/tasks
```
**Description**: Create a new task for the authenticated user
**Headers**:
- `Authorization: Bearer <jwt_token>`
- `Content-Type: application/json`

**Request Body**:
```json
{
  "title": "string (1-200 chars)",
  "description": "string (max 1000 chars, optional)"
}
```

**Responses**:
- `201 Created`: Task created successfully
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Invalid/missing JWT
- `422 Unprocessable Entity`: Validation errors

**Response Body (201)**:
```json
{
  "id": "integer",
  "user_id": "string",
  "title": "string",
  "description": "string",
  "completed": "boolean",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

#### List Tasks
```
GET /api/{user_id}/tasks
```
**Description**: Get all tasks for the authenticated user
**Headers**:
- `Authorization: Bearer <jwt_token>`

**Query Parameters**:
- `limit`: integer (optional, default: 50)
- `offset`: integer (optional, default: 0)

**Responses**:
- `200 OK`: Tasks retrieved successfully
- `401 Unauthorized`: Invalid/missing JWT

**Response Body (200)**:
```json
[
  {
    "id": "integer",
    "user_id": "string",
    "title": "string",
    "description": "string",
    "completed": "boolean",
    "created_at": "timestamp",
    "updated_at": "timestamp"
  }
]
```

#### Get Task
```
GET /api/{user_id}/tasks/{id}
```
**Description**: Get a specific task for the authenticated user
**Headers**:
- `Authorization: Bearer <jwt_token>`

**Path Parameters**:
- `id`: integer (task ID)

**Responses**:
- `200 OK`: Task retrieved successfully
- `401 Unauthorized`: Invalid/missing JWT
- `404 Not Found`: Task doesn't exist or belongs to another user

**Response Body (200)**:
```json
{
  "id": "integer",
  "user_id": "string",
  "title": "string",
  "description": "string",
  "completed": "boolean",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

#### Update Task
```
PUT /api/{user_id}/tasks/{id}
```
**Description**: Update a specific task for the authenticated user
**Headers**:
- `Authorization: Bearer <jwt_token>`
- `Content-Type: application/json`

**Path Parameters**:
- `id`: integer (task ID)

**Request Body**:
```json
{
  "title": "string (1-200 chars)",
  "description": "string (max 1000 chars, optional)"
}
```

**Responses**:
- `200 OK`: Task updated successfully
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Invalid/missing JWT
- `404 Not Found`: Task doesn't exist or belongs to another user
- `422 Unprocessable Entity`: Validation errors

**Response Body (200)**:
```json
{
  "id": "integer",
  "user_id": "string",
  "title": "string",
  "description": "string",
  "completed": "boolean",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

#### Delete Task
```
DELETE /api/{user_id}/tasks/{id}
```
**Description**: Delete a specific task for the authenticated user
**Headers**:
- `Authorization: Bearer <jwt_token>`

**Path Parameters**:
- `id`: integer (task ID)

**Responses**:
- `204 No Content`: Task deleted successfully
- `401 Unauthorized`: Invalid/missing JWT
- `404 Not Found`: Task doesn't exist or belongs to another user

#### Toggle Task Completion
```
PATCH /api/{user_id}/tasks/{id}/complete
```
**Description**: Toggle the completion status of a specific task
**Headers**:
- `Authorization: Bearer <jwt_token>`

**Path Parameters**:
- `id`: integer (task ID)

**Request Body**:
```json
{
  "completed": "boolean (optional, if not provided, toggle current status)"
}
```

**Responses**:
- `200 OK`: Task completion status updated successfully
- `401 Unauthorized`: Invalid/missing JWT
- `404 Not Found`: Task doesn't exist or belongs to another user

**Response Body (200)**:
```json
{
  "id": "integer",
  "user_id": "string",
  "title": "string",
  "description": "string",
  "completed": "boolean",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

## Error Response Format
All error responses follow this format:
```json
{
  "detail": "error message"
}
```

## Authentication Error Responses
- `401 Unauthorized`: `{"detail": "Not authenticated"}`
- `403 Forbidden`: `{"detail": "Access denied"}`