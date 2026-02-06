@echo off
echo =============================================
echo Troubleshooting Guide for Signup Issues
echo =============================================
echo.

echo PROBLEM: 422 Unprocessable Content Error
echo CAUSE: The backend expects JSON data but frontend sends form data
echo.

echo SOLUTIONS:
echo.
echo 1. BACKEND: Update the auth endpoint to accept form data (recommended)
echo    In backend/src/api/auth.py, change the register endpoint to use Form parameters
echo.
echo 2. FRONTEND: Update the signup page to send JSON data
echo    In frontend/src/app/signup/page.tsx, change the axios.post to send JSON
echo.
echo 3. TEMPORARY FIX: Test the API directly using curl:
echo.
echo    curl -X POST "http://localhost:7860/auth/register" ^
echo    -H "Content-Type: application/json" ^
echo    -d "{\\"username\\": \\"testuser\\", \\"password\\": \\"testpass123\\"}"
echo.
echo 4. CHECK: Make sure the backend server is running:
echo    - Visit: http://localhost:7860/docs
echo    - Test the /auth/register endpoint in the API docs
echo.
echo TO START THE APPLICATION:
echo    1. Run RUN_BACKEND.bat to start backend server
echo    2. Open new terminal and run frontend: npm run dev
echo    3. Visit http://localhost:3000 to use the app
echo.

echo Press any key to exit...
pause >nul