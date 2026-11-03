@echo off
title Stop Bharat Alpha Server
echo Stopping Bharat Alpha Web Server on port 8000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8000 " ^| findstr "LISTENING"') do (
    taskkill /F /PID %%a >nul 2>&1
)
echo Server stopped.
timeout /t 2 >nul
exit /b 0

