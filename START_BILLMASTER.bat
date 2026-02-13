@echo off
TITLE BillMaster Pro Launcher
COLOR 0A
CLS

echo.
echo  ==================================================
echo             BILLMASTER PRO - SETUP ^& START
echo  ==================================================
echo.

:: 1. Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python from https://python.org
    pause
    exit /b
)

:: 2. Activate Virtual Environment if exists
if exist ".venv\Scripts\activate" (
    echo [1/4] 📦 Activating virtual environment...
    call .venv\Scripts\activate
) else (
    echo [1/4] ⚠️ Virtual environment not found. Using system Python.
)

:: 3. Install Dependencies
echo [2/4] 🛠️ Installing required dependencies...
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b
)

:: 4. Launch Browser
echo [3/4] 🌐 Opening Login Page...
timeout /t 3 /nobreak >nul
start "" "http://localhost:5000/login.html"

:: 5. Start Backend Server
echo [4/4] 🔥 Starting BillMaster Pro Server...
echo.
echo --------------------------------------------------
echo   Server is running at http://localhost:5000
echo   KEEP THIS WINDOW OPEN WHILE USING THE APP
echo --------------------------------------------------
echo.

python run.py

echo.
echo Server stopped.
pause
