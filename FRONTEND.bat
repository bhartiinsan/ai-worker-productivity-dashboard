@echo off
title Frontend Server
cd /d "C:\Users\BHARTI\OneDrive\Desktop\Dashboard\frontend"

echo ================================
echo   AI WORKER PRODUCTIVITY DASHBOARD
echo   Frontend Server
echo ================================
echo.
echo Frontend Running: http://localhost:3000
echo.
echo Press Ctrl+C to stop
echo.

set BROWSER=none
npm start
