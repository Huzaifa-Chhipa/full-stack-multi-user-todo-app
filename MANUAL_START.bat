@echo off
echo =============================================
echo Starting Todo Application - Manual Setup
echo =============================================
echo.

echo 1. Make sure PostgreSQL is running on localhost:5432
echo 2. Navigate to the backend directory and run:
echo    pip install -r requirements.txt
echo    uvicorn src.main:app --reload --host 0.0.0.0 --port 7860
echo.
echo 3. Open another terminal, navigate to the frontend directory and run:
echo    npm install
echo    npm run dev
echo.
echo 4. Access the application at: http://localhost:3000
echo.

echo Press any key to exit...
pause >nul