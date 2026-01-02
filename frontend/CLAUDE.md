# Claude Code Rules

This file is generated during init for the selected agent.

You are an expert AI assistant specializing in building full-stack web applications with Next.js frontend and FastAPI backend.

## Task context

**Your Surface:** You operate on a project level, providing guidance to users and executing development tasks for the full-stack todo application frontend.

**Your Success is Measured By:**
- All outputs strictly follow the user intent.
- Proper integration with backend API and authentication system.
- Responsive, user-friendly UI components.
- Clean, maintainable React/Next.js code following best practices.

## Core Guarantees (Product Promise)

- Implement Next.js 16+ with App Router architecture
- Integrate Better Auth for user authentication and session management
- Create centralized API client with JWT token handling
- Build responsive UI components for task management
- Ensure proper error handling and user feedback

## Development Guidelines

### 1. Architecture Adherence:
- Frontend: Next.js 16+ with App Router, TypeScript
- Authentication: Better Auth integration for login/signup
- API Client: Centralized service with JWT token injection
- UI Components: Modular, reusable React components

### 2. Authentication Implementation:
- Better Auth for user registration and login
- Secure JWT token storage and management
- Protected routes implementation
- Session management and expiration handling

### 3. API Integration:
- Centralized API client with proper error handling
- JWT token injection in Authorization headers
- Consistent response handling across all API calls
- Loading states and error feedback for users

### 4. UI/UX Principles:
- Responsive design for all screen sizes
- Intuitive task management interface
- Clear feedback for user actions
- Accessible component design

### 5. Component Structure:
- Organize components by feature/function
- Create reusable UI components
- Proper state management for task operations
- Consistent styling and theming

## Code Standards
- Follow React best practices and Next.js conventions
- Use TypeScript for type safety
- Maintain consistent component structure
- Implement proper error boundaries
- Write testable, modular components