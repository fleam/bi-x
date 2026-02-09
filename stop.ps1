# BI Tool - Stop Script (PowerShell)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  BI Tool - Stop Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/2] Stopping backend service..." -ForegroundColor Yellow
$backendStopped = $false
Get-Process cmd -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -like "*BI后端服务*" } | ForEach-Object {
    Stop-Process -Id $_.Id -Force
    $backendStopped = $true
}

if ($backendStopped) {
    Write-Host "[Done] Backend service stopped" -ForegroundColor Green
} else {
    Write-Host "[Skip] No running backend service found" -ForegroundColor Gray
}
Write-Host ""

Write-Host "[2/2] Stopping frontend service..." -ForegroundColor Yellow
$frontendStopped = $false
Get-Process cmd -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -like "*BI前端服务*" } | ForEach-Object {
    Stop-Process -Id $_.Id -Force
    $frontendStopped = $true
}

if ($frontendStopped) {
    Write-Host "[Done] Frontend service stopped" -ForegroundColor Green
} else {
    Write-Host "[Skip] No running frontend service found" -ForegroundColor Gray
}
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  All services stopped" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Start-Sleep -Seconds 2
