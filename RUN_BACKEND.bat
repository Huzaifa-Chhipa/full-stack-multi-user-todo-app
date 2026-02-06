@echo off
echo =============================================
echo Starting Todo Application Backend Server
echo =============================================
echo.

echo Installing dependencies (first time only)...
pip install -r requirements.txt

echo.
echo Starting backend server on http://localhost:7860...
echo.
echo NOTE: Keep this window open while using the application
echo.

cd /d "E:\HACKATHON 2\Full-Stack Multi-User Web Todo Application\backend"
uvicorn src.main:app --reload --host 0.0.0.0 --port 7860

echo.
echo Backend server stopped.
pause