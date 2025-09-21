@echo off
REM Quick setup script for Gujarati News Translator (Windows)

echo 🚀 Setting up Gujarati News Translator...

REM Check prerequisites
echo 📋 Checking prerequisites...

docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker first.
    pause
    exit /b 1
)

docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

echo ✅ Docker and Docker Compose are installed

REM Copy environment files
echo 📄 Setting up environment files...
if not exist backend\.env (
    copy backend\.env.example backend\.env
    echo ✅ Created backend\.env
) else (
    echo ⚠️  backend\.env already exists
)

if not exist frontend\.env (
    copy frontend\.env.example frontend\.env
    echo ✅ Created frontend\.env
) else (
    echo ⚠️  frontend\.env already exists
)

REM Build and start the application
echo 🏗️  Building and starting the application...
docker-compose up --build -d

REM Wait for services to start
echo ⏳ Waiting for services to start...
timeout /t 30 /nobreak >nul

REM Check health
echo 🔍 Checking application health...
curl -f http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    echo ❌ Backend health check failed
) else (
    echo ✅ Backend is healthy
)

curl -f http://localhost/ >nul 2>&1
if errorlevel 1 (
    echo ❌ Frontend is not accessible
) else (
    echo ✅ Frontend is accessible
)

echo.
echo 🎉 Setup complete!
echo.
echo 🌐 Access the application:
echo    Frontend: http://localhost
echo    Backend API: http://localhost:8000
echo    API Docs: http://localhost:8000/docs
echo.
echo 📊 View logs:
echo    docker-compose logs -f
echo.
echo 🛑 Stop the application:
echo    docker-compose down
echo.
echo Happy translating! 🔄
pause