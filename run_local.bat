@echo off
title CycloneShield Local Server Launcher
echo ========================================================
echo   CycloneShield - Autonomous Disaster Triage Command Hub
echo ========================================================
echo.

cd /d "%~dp0"

echo [1/3] Checking for and clearing any stale processes on port 8501...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8501 ^| findstr LISTENING 2^>nul') do (
    echo Terminating stale process PID %%a...
    taskkill /F /PID %%a >nul 2>&1
)

echo [2/3] Checking Python virtual environment...
if exist "cycloneshield\.venv\Scripts\streamlit.exe" (
    set "ST_EXE=cycloneshield\.venv\Scripts\streamlit.exe"
) else (
    if exist ".venv\Scripts\streamlit.exe" (
        set "ST_EXE=.venv\Scripts\streamlit.exe"
    ) else (
        set "ST_EXE=streamlit"
    )
)

echo [3/3] Launching CycloneShield Streamlit Command Center on http://localhost:8501 ...
echo.
echo ========================================================
echo   Web App URL: http://localhost:8501
echo   (Opening browser automatically...)
echo   Press Ctrl+C in this window to stop the server.
echo ========================================================
echo.

start "" "http://localhost:8501"
"%ST_EXE%" run cycloneshield/app.py --server.port 8501 --server.headless false

pause
