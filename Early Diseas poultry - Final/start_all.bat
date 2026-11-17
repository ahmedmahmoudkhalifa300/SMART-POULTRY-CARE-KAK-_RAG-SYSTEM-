@echo off
echo ==============================================
echo 🐔 Starting Poultry Disease Services 🐔
echo ==============================================
echo.
echo Starting Backend Server...
start "Poultry Backend" cmd /k "run_backend.bat"

echo Starting Frontend Server...
start "Poultry Frontend" cmd /k "run_frontend.bat"

echo Starting RAG System Server...
start "Poultry RAG System" cmd /k "run_rag_system.bat"

echo.
echo All services have been launched in separate windows!
echo You can close this main window.
pause
