@echo off
REM Setup script untuk Roblox Account Manager

echo.
echo =======================================
echo   Roblox Account Manager Setup
echo =======================================
echo.

cd /d "%~dp0"

echo [1/5] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found! Please install Python 3.7+ first.
    echo Download from: https://python.org
    pause
    exit /b 1
)
echo ✓ Python found

echo.
echo [2/5] Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment created

echo.
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [4/5] Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed

echo.
echo [5/5] Installing Playwright browsers...
playwright install
if %errorlevel% neq 0 (
    echo WARNING: Failed to install browsers, but continuing...
)
echo ✓ Browsers installed

echo.
echo =======================================
echo   Setup Complete! 🎉
echo =======================================
echo.
echo To run the application:
echo   1. Double-click run.bat, OR
echo   2. Run: python main.py
echo.
echo Press any key to continue...
pause >nul