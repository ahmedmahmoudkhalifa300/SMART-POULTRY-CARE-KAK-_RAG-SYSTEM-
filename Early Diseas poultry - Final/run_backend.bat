@echo off
echo ==============================================
echo 🐔 Poultry Disease Backend Setup and Runner 🐔
echo ==============================================

echo [1] Checking for Python 3.11 installation...
py -3.11 --version
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python 3.11 is not installed! Please install Python 3.11 first.
    pause
    exit /b
)

echo [2] Creating a fresh virtual environment named 'backend_env'...
if not exist "backend_env" (
    py -3.11 -m venv backend_env
)

echo [3] Activating virtual environment and installing dependencies...
call backend_env\Scripts\activate.bat
pip install -r requirements.txt

echo [4] Starting FastAPI Server...
uvicorn backend.main:app --reload --port 8000
pause
