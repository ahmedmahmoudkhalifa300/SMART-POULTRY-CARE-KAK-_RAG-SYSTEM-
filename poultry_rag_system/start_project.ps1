$ProjectRoot = $PSScriptRoot

# =========================
# FastAPI Backend
# =========================
Start-Process -FilePath "$ProjectRoot\.venv311\Scripts\python.exe" `
    -WorkingDirectory $ProjectRoot `
    -ArgumentList "-m uvicorn app.main:app --host 127.0.0.1 --port 8001 --app-dir poultry_rag_system --reload"

# =========================
# Streamlit Frontend
# =========================
Start-Process -FilePath "$ProjectRoot\.venv311\Scripts\python.exe" `
    -WorkingDirectory $ProjectRoot `
    -ArgumentList "-m streamlit run poultry_rag_system\app\streamlit_app.py --server.address 127.0.0.1 --server.port 8502"

Write-Host ""
Write-Host "========================================"
Write-Host " Poultry RAG System is starting..."
Write-Host "========================================"
Write-Host ""
Write-Host "Backend  : http://127.0.0.1:8001"
Write-Host "Swagger  : http://127.0.0.1:8001/docs"
Write-Host "Frontend : http://127.0.0.1:8502"
Write-Host ""