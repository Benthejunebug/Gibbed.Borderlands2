@echo off
:: NoLevelRequirement Mod Installer — Windows wrapper
:: Double-click this file, or run it in Command Prompt.
:: Requires Python 3.8+ installed and on PATH.

echo ========================================
echo NoLevelRequirement Mod Installer
echo ========================================
echo.

python --version > NUL 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not on PATH.
    echo.
    echo Please install Python 3 from https://python.org/
    echo Make sure to check "Add Python to PATH" during install.
    pause
    exit /b 1
)

python "%~dp0install_mod.py" %*
if errorlevel 1 (
    echo.
    echo Press any key to close...
    pause > NUL
    exit /b 1
)

echo.
echo Press any key to close...
pause > NUL
