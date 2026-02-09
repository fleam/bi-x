# BI Tool - Start Script (PowerShell)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  BI Tool - Start Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Node.js
Write-Host "[1/4] Checking dependencies..." -ForegroundColor Yellow
Write-Host ""

$nodeInstalled = Get-Command node -ErrorAction SilentlyContinue
if (-not $nodeInstalled) {
    Write-Host "[Error] Node.js not found, please install Node.js" -ForegroundColor Red
    Read-Host "Press any key to exit"
    exit 1
}

# Check Python
$pythonInstalled = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonInstalled) {
    Write-Host "[Error] Python not found, please install Python" -ForegroundColor Red
    Read-Host "Press any key to exit"
    exit 1
}

Write-Host "[Done] Node.js and Python installed" -ForegroundColor Green
Write-Host ""

# Check frontend dependencies
if (-not (Test-Path "frontend\node_modules")) {
    Write-Host "[Info] Frontend dependencies not found, installing..." -ForegroundColor Yellow
    Set-Location frontend
    npm install
    Set-Location ..
    Write-Host "[Done] Frontend dependencies installed" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "[Skip] Frontend dependencies already installed" -ForegroundColor Green
    Write-Host ""
}

# Check backend dependencies
if (-not (Test-Path "backend\venv")) {
    Write-Host "[Info] Backend virtual environment not found, creating..." -ForegroundColor Yellow
    Set-Location backend
    python -m venv venv
    & .\venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    Set-Location ..
    Write-Host "[Done] Backend dependencies installed" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "[Skip] Backend virtual environment already created" -ForegroundColor Green
    Write-Host ""
}

# Start backend service
Write-Host "[2/4] Starting backend service..." -ForegroundColor Yellow
$backendArgs = @("/k", "cd backend", "&", "venv\Scripts\activate", "&", "uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
Start-Process -FilePath "cmd.exe" -ArgumentList $backendArgs -WindowStyle Normal
Write-Host "[Done] Backend service started (port: 8000)" -ForegroundColor Green
Write-Host ""

# Start frontend service
Write-Host "[3/4] Starting frontend service..." -ForegroundColor Yellow
$frontendArgs = @("/k", "cd frontend", "&", "npm run dev")
Start-Process -FilePath "cmd.exe" -ArgumentList $frontendArgs -WindowStyle Normal
Write-Host "[Done] Frontend service started" -ForegroundColor Green
Write-Host ""

# Wait for services to start
Write-Host "[4/4] Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Started successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Frontend: http://localhost:5173" -ForegroundColor White
Write-Host "  Backend:  http://localhost:8000" -ForegroundColor White
Write-Host "  API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Tip: Closing this window will not stop services. Close individual service windows to stop services." -ForegroundColor Yellow
Write-Host ""

Read-Host "Press any key to exit (services will continue running)"
