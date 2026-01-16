@echo off
echo Starting Flight Booking System...
echo.

REM Change to the script directory
cd /d "%~dp0"

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not installed or not in PATH
    echo Please install Docker Desktop from https://www.docker.com/products/docker-desktop/
    pause
    exit /b 1
)

REM Check if Docker daemon is running
docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker daemon is not running
    echo Please start Docker Desktop
    pause
    exit /b 1
)

REM Check if docker-compose.yml exists
if not exist docker-compose.yml (
    echo ERROR: docker-compose.yml not found in current directory
    echo Current directory: %CD%
    pause
    exit /b 1
)

echo Docker is ready!
echo Current directory: %CD%
echo.
echo Building and starting all services...
echo This may take a few minutes on first run...
echo.

REM Force a valid project name (directory ends with underscore, which breaks image naming)
docker-compose -p drs_tim2 up --build -d

echo.
echo ============================================
echo All services are starting in background!
echo ============================================
echo.
echo Services:
echo - Frontend: http://localhost:5173
echo - Server API: http://localhost:5000
echo - Flight Service API: http://localhost:5001
echo.
echo To see logs, run: docker-compose logs -f
echo To stop services, run: docker-compose down
echo.
pause
