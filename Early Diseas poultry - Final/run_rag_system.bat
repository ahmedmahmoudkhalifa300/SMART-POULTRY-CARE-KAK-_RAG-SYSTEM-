@echo off
echo ==============================================
echo 🐔 Poultry Disease RAG System Runner 🐔
echo ==============================================

cd ..\poultry_rag_system\poultry_rag_system
echo [1] Checking RAG environment...
if not exist "..\.venv311" (
    echo [ERROR] RAG environment .venv311 not found!
    pause
    exit /b
)

echo [2] Starting RAG Backend on Port 8001...
..\.venv311\Scripts\python.exe -m uvicorn app.main:app --reload --port 8001
pause
