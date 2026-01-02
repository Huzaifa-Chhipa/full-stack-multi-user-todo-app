# Quickstart Guide: Full-Stack Multi-User Web Todo Application

## Prerequisites
- Node.js 18+ for Next.js frontend
- Python 3.13+ for FastAPI backend
- PostgreSQL-compatible database (Neon Serverless recommended)
- Better Auth account setup

## Environment Setup

### Backend (FastAPI)
1. Install Python dependencies:
```bash
pip install fastapi uvicorn sqlmodel python-jose[cryptography] psycopg2-binary python-multipart
```

2. Set environment variables:
```bash
export DATABASE_URL="postgresql://user:password@host:port/database"
export BETTER_AUTH_SECRET="your-jwt-secret-key"
```

### Frontend (Next.js)
1. Install Node.js dependencies:
```bash
npm install next @better-auth/react @better-auth/client
```

2. Set environment variables:
```bash
NEXT_PUBLIC_BETTER_AUTH_URL="http://localhost:3000"
NEXT_PUBLIC_BETTER_AUTH_SECRET="your-jwt-secret-key"
```

## Database Setup
1. Initialize the database schema with the Task model
2. Ensure the tasks table has an index on user_id for performance
3. Verify database connection with the DATABASE_URL

## Running the Application

### Backend
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm run dev
```

## API Access
- Backend API available at `http://localhost:8000/api/{user_id}/tasks`
- Frontend at `http://localhost:3000`
- Authentication handled via Better Auth JWT tokens