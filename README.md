# Full-Stack Multi-User Web Todo Application

A complete full-stack web application for managing todo tasks with multi-user support, authentication, and secure data isolation.

## Features

- **Multi-user support**: Each user has their own isolated set of tasks
- **Authentication**: Secure login and signup with JWT-based authentication
- **Task Management**: Create, read, update, delete, and toggle completion status of tasks
- **Responsive UI**: Clean, user-friendly interface built with Next.js
- **Secure API**: FastAPI backend with proper authorization and validation

## Tech Stack

- **Frontend**: Next.js 16+ with App Router
- **Backend**: FastAPI with async support
- **Database**: PostgreSQL via SQLModel ORM
- **Authentication**: JWT-based with custom auth system
- **Frontend Libraries**: React, Axios

## Architecture

The application follows a client-server architecture with:
- Frontend Next.js application handling UI and user interactions
- FastAPI backend providing REST API endpoints
- PostgreSQL database for persistent storage
- JWT tokens for authentication and user isolation

## Setup Instructions

### Prerequisites

- Python 3.13+
- Node.js 18+
- PostgreSQL (or Neon Serverless for cloud deployment)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install fastapi uvicorn sqlmodel python-jose python-multipart
   ```

3. Set up environment variables (see Environment Variables section below)

4. Run database migrations:
   ```bash
   python migrate.py
   ```

5. Start the backend server:
   ```bash
   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

3. Set up environment variables (see Environment Variables section below)

4. Start the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

## Environment Variables

### Backend (.env)

Create a `.env` file in the backend directory with the following variables:

```env
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/todo_db
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
```

### Frontend (.env.local)

Create a `.env.local` file in the frontend directory with the following variables:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## API Endpoints

### Authentication

- `POST /auth/token` - Login endpoint (returns JWT token)

### Task Management

All task endpoints require a valid JWT token in the Authorization header.

- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks` - Get all tasks for the user (newest first)
- `GET /api/{user_id}/tasks/{id}` - Get a specific task
- `PUT /api/{user_id}/tasks/{id}` - Update a task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion status

## Development

### Running Tests

Integration tests can be run with:
```bash
python integration_tests.py
```

### Project Structure

```
backend/
├── src/
│   ├── main.py          # FastAPI application entry point
│   ├── db.py            # Database connection and setup
│   ├── models/
│   │   └── task.py      # Task data models
│   ├── api/
│   │   ├── tasks.py     # Task API endpoints
│   │   └── auth.py      # Authentication endpoints
│   └── auth/
│       └── jwt.py       # JWT authentication utilities
├── migrate.py           # Database migration script
└── requirements.txt

frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx   # Root layout
│   │   ├── dashboard/   # Dashboard page
│   │   ├── login/       # Login page
│   │   └── signup/      # Signup page
│   ├── components/      # Reusable components
│   ├── services/        # API client
│   └── lib/             # Utilities and auth
├── package.json
└── next.config.js

specs/                    # Project specifications and documentation
history/                  # Prompt history records
```

## Security Features

- JWT-based authentication with expiration
- User data isolation at the API level
- Input validation for all endpoints
- Secure token storage in browser localStorage

## Performance Considerations

- Async database operations for better performance
- Proper indexing on database tables
- Optimized API response sizes
- Client-side caching where appropriate