# Architecture: Full-Stack Multi-User Web Todo Application

## Overview
This document describes the architectural design of the full-stack multi-user web todo application. The system follows a client-server architecture with a clear separation between frontend and backend components.

## System Architecture

### Backend (FastAPI)
- **Framework**: FastAPI for high-performance API development
- **Database**: PostgreSQL via SQLModel ORM with Neon Serverless
- **Authentication**: JWT-based authentication with stateless validation
- **API Layer**: RESTful endpoints with proper error handling
- **Business Logic**: Task management services with user isolation

### Frontend (Next.js)
- **Framework**: Next.js 16+ with App Router
- **Authentication**: Better Auth integration for user management
- **API Client**: Centralized service for backend communication
- **UI Components**: Modular, reusable components for task management

### Data Flow
1. User interacts with Next.js frontend
2. Frontend makes authenticated API calls to FastAPI backend
3. Backend validates JWT and enforces user isolation
4. Backend performs database operations via SQLModel
5. Results returned to frontend with proper error handling

## Security Model
- JWT tokens issued by Better Auth
- User data isolation at API level (user_id validation)
- Secure credential handling
- Input validation and sanitization

## Deployment Architecture
- Backend: FastAPI application (REST API server)
- Frontend: Next.js application (SSR/Static generation)
- Database: Neon PostgreSQL (managed serverless database)
- Authentication: Better Auth (external auth service)