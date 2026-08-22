@echo off
title DermaVision AI - One-Click Launcher & Access Manager
color 0A

echo =========================================================================
echo                  DERMAVISION AI - ONE-CLICK LAUNCHER
echo =========================================================================
echo.
echo Starting all backend services, frontend portals, and tunnels...
echo.

REM Set Node.js & Python Environment Paths
set "PATH=C:\Users\yoges\Downloads\DermaVision-AI\.nodejs;%PATH%"
set "PYTHON_EXE=C:\Users\yoges\Downloads\DermaVision-AI\.python311\python.exe"

REM 1. Start FastAPI AI Backend on Port 8000
echo [1/4] Launching FastAPI AI Backend Server (Port 8000)...
start "DermaVision AI Backend (Port 8000)" cmd /k "& '%PYTHON_EXE%' -m uvicorn backend.main:app --host 0.0.0.0 --port 8000"

timeout /t 3 >nul

REM 2. Start Patient Web App Static Server on Port 5173
echo [2/4] Launching Patient Web Application (Port 5173)...
start "DermaVision Patient App (Port 5173)" cmd /k "cd /d C:\Users\yoges\Downloads\techno\frontend && npx serve -s dist -l 5173"

timeout /t 2 >nul

REM 3. Start Doctor Portal Server on Port 5174
echo [3/4] Launching Doctor Portal Workspace (Port 5174)...
start "DermaVision Doctor Portal (Port 5174)" cmd /k "cd /d C:\Users\yoges\Downloads\doctorweb && npx serve -s dist -l 5174"

timeout /t 2 >nul

REM 4. Launch Cloudflare Public Tunnels
echo [4/4] Launching Cloudflare HTTPS Public Tunnels...
start "Cloudflare Patient App Tunnel" cmd /k "npx cloudflared tunnel --url http://localhost:5173"
start "Cloudflare Doctor Portal Tunnel" cmd /k "npx cloudflared tunnel --url https://localhost:5174 --no-tls-verify"
start "Cloudflare AI Backend Tunnel" cmd /k "npx cloudflared tunnel --url http://localhost:8000"

timeout /t 4 >nul

REM 5. Open Web Browser to Localhost Links
echo.
echo =========================================================================
echo                  OPENING WEBSITES IN BROWSER...
echo =========================================================================
start http://localhost:5173
start https://localhost:5174
start http://localhost:8000/docs

echo.
echo SUCCESS! All DermaVision AI services and websites are active.
echo Press any key to exit this launcher window (servers will remain running).
pause >nul
