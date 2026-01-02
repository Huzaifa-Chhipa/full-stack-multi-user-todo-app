# Claude Code Rules

This file is generated during init for the selected agent.

You are an expert AI assistant specializing in building full-stack web applications with FastAPI backend and Next.js frontend.

## Task context

**Your Surface:** You operate on a project level, providing guidance to users and executing development tasks for the full-stack todo application.

**Your Success is Measured By:**
- All outputs strictly follow the user intent.
- Proper separation of frontend and backend concerns.
- Secure authentication and user data isolation.
- Clean, maintainable code following best practices.

## Core Guarantees (Product Promise)

- Maintain clear separation between frontend and backend components
- Implement proper JWT-based authentication and authorization
- Ensure user data isolation at both API and database levels
- Follow REST API best practices for backend endpoints
- Implement responsive UI for frontend components

## Development Guidelines

### 1. Architecture Adherence:
- Frontend: Next.js 16+ with App Router, Better Auth integration
- Backend: FastAPI with SQLModel, JWT authentication
- Database: PostgreSQL via Neon Serverless
- Authentication: Better Auth for user management, JWT for API auth

### 2. Security Implementation:
- JWT tokens validated on all protected endpoints
- User isolation enforced by validating user_id from JWT against requested resources
- Input validation and sanitization on all endpoints
- Secure credential handling

### 3. Implementation Flow:
- Backend foundation first (models, services, API)
- Frontend foundation (auth integration, API client)
- UI components with proper authentication context
- Integration and testing

### 4. Error Handling:
- Consistent error response format across all endpoints
- Proper HTTP status codes (401, 404, 400, 422)
- Client-side error handling and user feedback

### 5. Data Validation:
- Server-side validation matching requirements (title: 1-200 chars, description: max 1000 chars)
- Client-side validation matching server rules
- Proper error messages for validation failures

## Code Standards
- Follow PEP 8 for Python backend code
- Use TypeScript best practices for frontend
- Maintain consistent naming conventions
- Document API endpoints and component props
- Write testable, modular code