@echo off
echo ==============================================
echo 🐔 Poultry Disease Frontend Runner 🐔
echo ==============================================

cd frontend
echo [1] Installing npm dependencies...
call npm install

echo [2] Starting Vite Dev Server...
npm run dev -- --open
pause
