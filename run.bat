@echo off
rem ============================================================
rem  AdaptIQ - one-command local setup (Windows)
rem  Creates the venv, installs deps, prepares the database,
rem  applies migrations and starts backend + frontend.
rem ============================================================
setlocal
cd /d "%~dp0"

echo.
echo  ============================================
echo    AdaptIQ - one-command local setup
echo  ============================================
echo.

where python >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Python 3 not found on PATH. Install it from https://www.python.org
  exit /b 1
)
where node >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Node.js not found on PATH. Install it from https://nodejs.org
  exit /b 1
)

set "PY=%~dp0backend\.venv\Scripts\python.exe"

if not exist "%~dp0backend\.venv\Scripts\python.exe" (
  echo [1/4] Creating Python virtual environment...
  python -m venv "%~dp0backend\.venv"
)
if errorlevel 1 exit /b 1

echo [2/4] Installing Python dependencies...
"%PY%" -m pip install --quiet --disable-pip-version-check -r "%~dp0backend\requirements.txt"
if errorlevel 1 (
  echo [ERROR] pip install failed.
  exit /b 1
)

if not exist "%~dp0backend\.env" copy /y "%~dp0backend\.env.example" "%~dp0backend\.env" >nul
if not exist "%~dp0frontend\.env" copy /y "%~dp0frontend\.env.example" "%~dp0frontend\.env" >nul

echo [3/4] Preparing the database...
"%PY%" "%~dp0backend\scripts\bootstrap.py"
if errorlevel 1 exit /b 1

if not exist "%~dp0frontend\node_modules" goto install_frontend
echo [4/4] Frontend dependencies already installed.
goto start

:install_frontend
echo [4/4] Installing frontend dependencies...
pushd "%~dp0frontend"
call npm install --no-fund --no-audit
if errorlevel 1 (
  popd
  echo [ERROR] npm install failed.
  exit /b 1
)
popd

:start
echo.
echo  Starting servers...
start "AdaptIQ API" /d "%~dp0backend" cmd /k ""%~dp0backend\.venv\Scripts\python.exe" -m uvicorn app.main:app --reload --port 8000"
start "AdaptIQ UI" /d "%~dp0frontend" cmd /k "npm run dev"
echo.
echo  Backend : http://localhost:8000/api/health
echo  Frontend: http://localhost:5173
echo.
echo  Two new windows opened for the servers. Keep this window open;
echo  close the server windows (or press Ctrl+C in them) to stop.
echo.
pause