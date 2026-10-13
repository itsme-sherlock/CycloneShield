# CycloneShield - 1-Click Google Cloud Run Deployment Script (PowerShell)
# Run from repository root: .\deploy_cloud_run.ps1

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " CycloneShield - Google Cloud Run Deployment Initiator" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# Check if gcloud is installed
if (-not (Get-Command gcloud -ErrorAction SilentlyContinue)) {
    Write-Host "[!] Error: 'gcloud' CLI is not found in PATH." -ForegroundColor Red
    Write-Host "    If deploying from local machine, please install Google Cloud SDK." -ForegroundColor Yellow
    Write-Host "    Alternatively, run this from Google Cloud Shell in your GCP Console." -ForegroundColor Yellow
    Exit 1
}

$REGION = "asia-south1"
$SERVICE_NAME = "cycloneshield"

Write-Host "[1/3] Detecting active GCP project..." -ForegroundColor Green
$PROJECT_ID = (gcloud config get-value project 2>$null)

if (-not $PROJECT_ID) {
    Write-Host "[!] No active GCP project configured. Set it using: gcloud config set project <PROJECT_ID>" -ForegroundColor Red
    Exit 1
}

Write-Host "      Active Project: $PROJECT_ID" -ForegroundColor Gray
Write-Host "      Target Region:  $REGION" -ForegroundColor Gray
Write-Host "      Service Name:   $SERVICE_NAME" -ForegroundColor Gray

Write-Host "`n[2/3] Submitting source build directly to Cloud Run..." -ForegroundColor Green
Write-Host "      Building container with 2Gi memory, 2 vCPU, and scale-to-1 pre-warmed instance..." -ForegroundColor Gray

gcloud run deploy $SERVICE_NAME `
    --source . `
    --region $REGION `
    --platform managed `
    --allow-unauthenticated `
    --port 8080 `
    --memory 2Gi `
    --cpu 2 `
    --min-instances 1 `
    --max-instances 10 `
    --timeout 300 `
    --set-env-vars "STREAMLIT_SERVER_HEADLESS=true,STREAMLIT_SERVER_PORT=8080,STREAMLIT_SERVER_ADDRESS=0.0.0.0"

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n[3/3] Deployment Successful!" -ForegroundColor Green
    $SERVICE_URL = (gcloud run services describe $SERVICE_NAME --region $REGION --format "value(status.url)")
    Write-Host "      Live Service URL: $SERVICE_URL" -ForegroundColor Cyan
} else {
    Write-Host "`n[!] Deployment failed. Check Cloud Run build/revision logs." -ForegroundColor Red
}
