# CycloneShield - Local Streamlit Server Launcher
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  CycloneShield - Autonomous Disaster Triage Command Hub" -ForegroundColor Yellow
Write-Host "========================================================" -ForegroundColor Cyan

# 1. Clear any stale process on port 8501
$conns = Get-NetTCPConnection -LocalPort 8501 -State Listen -ErrorAction SilentlyContinue
if ($conns) {
    foreach ($conn in $conns) {
        Write-Host "Stopping stale listener on port 8501 (PID $($conn.OwningProcess))..." -ForegroundColor Yellow
        Stop-Process -Id $conn.OwningProcess -Force -ErrorAction SilentlyContinue
    }
}

# 2. Locate Virtual Environment Streamlit
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$stExe = Join-Path $scriptDir "cycloneshield\.venv\Scripts\streamlit.exe"
if (-not (Test-Path $stExe)) {
    $stExe = "streamlit"
}

$appFile = Join-Path $scriptDir "cycloneshield\app.py"

Write-Host "Launching CycloneShield on http://localhost:8501..." -ForegroundColor Green
Start-Process "http://localhost:8501"
& $stExe run $appFile --server.port 8501
