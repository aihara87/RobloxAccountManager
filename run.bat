@echo off
REM Roblox Account Manager Launcher
REM Aktivasi venv dan jalankan aplikasi

echo.
echo ===================================
echo   Roblox Account Manager Launcher
echo ===================================
echo.

cd /d "%~dp0"

REM Check if venv exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first or follow installation guide
    pause
    exit /b 1
)

REM Activate virtual environment and run application
call venv\Scripts\activate.bat
python main.py

REM Deactivate when done
call venv\Scripts\deactivate.bat

echo.
echo Press any key to close...
pause >nul