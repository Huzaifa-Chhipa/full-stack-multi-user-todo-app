@echo off
echo =============================================
echo Starting Todo Application in Local Development Mode
echo =============================================
echo.

echo Setting up local development environment...
echo.

echo Step 1: Starting PostgreSQL database...
echo.

echo Step 2: Starting Backend API server on http://localhost:7860...
echo.

echo Step 3: Starting Frontend on http://localhost:3000...
echo.

echo To run the application:
echo 1. Make sure Docker Desktop is running
echo 2. Run: docker-compose up --build
echo 3. Access the app at: http://localhost:3000
echo.

echo If you want to run without Docker:
echo 1. Start PostgreSQL locally or use Docker: docker run --name todo-postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres
echo 2. Install backend dependencies: pip install -r requirements.txt
echo 3. Start backend: uvicorn src.main:app --reload --port 7860
echo 4. Install frontend dependencies: npm install
echo 5. Start frontend: npm run dev
echo.

pause