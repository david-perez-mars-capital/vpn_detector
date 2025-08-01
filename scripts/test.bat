@echo off
REM Simple test script for VPN detector package (Windows)

echo VPN Detector Package Test Script
echo =================================

REM Change to the project root directory
cd /d "%~dp0\.."

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    exit /b 1
)

echo ✓ Python found
python --version

REM Install the package in development mode
echo.
echo Installing package in development mode...
pip install -e . >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Failed to install package
    exit /b 1
)

echo ✓ Package installed successfully

REM Run the Python test script
echo.
echo Running functional tests...
python scripts\test.py
if %errorlevel% neq 0 (
    echo ❌ Functional tests failed
    exit /b 1
)

REM Run unit tests if pytest is available
echo.
echo Running unit tests...
pytest --version >nul 2>&1
if %errorlevel% equ 0 (
    pytest tests\ -v
    if %errorlevel% neq 0 (
        echo ❌ Unit tests failed
        exit /b 1
    )
    echo ✓ Unit tests passed
) else (
    echo ⚠️  pytest not found, skipping unit tests
    echo    Install with: pip install pytest
)

echo.
echo =================================
echo ✓ All tests completed successfully!