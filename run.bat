@echo off
echo 🌍 AI Travel Assistant Planner - Windows Launcher
echo ==================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv\" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if .env exists
if not exist ".env" (
    echo ❌ .env file not found. Please create .env file with your GEMINI_API_KEY
    pause
    exit /b 1
)

REM Install dependencies if needed
echo 📋 Checking dependencies...
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing dependencies...
    pip install -r requirements.txt
)

REM Launch the application
echo 🚀 Launching AI Travel Assistant Planner...
echo 🌐 Opening browser at http://localhost:8501
echo.
echo ✅ Application starting... Please wait a moment.
echo 📋 Press Ctrl+C to stop the application
echo.

REM Start Streamlit
streamlit run main.py --server.port=8501 --server.headless=true

echo.
echo 👋 Application stopped. Press any key to exit.
pause >nul