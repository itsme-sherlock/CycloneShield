<#
.SYNOPSIS
    CycloneShield - 1-Click Google Cloud Run Deployment Script (PowerShell)
.DESCRIPTION
    Automates building and deploying CycloneShield to Google Cloud Run from Windows.
#>

param(
    [string]$ProjectId = $env:GOOGLE_CLOUD_PROJECT,
    [string]$Region = "asia-south1",
    [string]$ServiceName = "cycloneshield",
    [string]$RepoName = "cycloneshield-repo"
)

$ErrorActionPreference = "Stop"

Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "🛡️  CycloneShield — 1-Click Google Cloud Run Deployment (PowerShell)" -ForegroundColor Cyan
Write-Host "==================================================================" -ForegroundColor Cyan

# 1. Check gcloud CLI
$gcloudCmd = Get-Command "gcloud" -ErrorAction SilentlyContinue
if (-not $gcloudCmd) {
    Write-Host "❌ Error: Google Cloud SDK ('gcloud') is not found in PATH." -ForegroundColor Red
    Write-Host "   Install from: https://cloud.google.com/sdk/docs/install" -ForegroundColor Yellow
    exit 1
}

# 2. Check Project ID
if (-not $ProjectId) {
    $activeProj = (& gcloud config get-value project 2>$null).Trim()
    if ($activeProj -and $activeProj -ne "(unset)") {
        $ProjectId = $activeProj
    } else {
        $ProjectId = Read-Host "Enter your Google Cloud Project ID"
        & gcloud config set project $ProjectId
    }
}

Write-Host "📋 Deployment Parameters:" -ForegroundColor Green
Write-Host "   • Project ID:    $ProjectId"
Write-Host "   • Region:        $Region"
Write-Host "   • Service:       $ServiceName"
Write-Host "   • Repository:    $RepoName"
Write-Host "=================================================================="

# 3. Enable APIs
Write-Host "⏳ Step 1/4: Enabling required Google Cloud APIs..." -ForegroundColor Yellow
& gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com bigquery.googleapis.com --project=$ProjectId

# 4. Check Artifact Registry
Write-Host "⏳ Step 2/4: Ensuring Artifact Registry repository exists..." -ForegroundColor Yellow
$repoCheck = (& gcloud artifacts repositories describe $RepoName --location=$Region --project=$ProjectId 2>$null)
if (-not $repoCheck) {
    Write-Host "   Creating repository '$RepoName' in $Region..."
    & gcloud artifacts repositories create $RepoName --repository-format=docker --location=$Region --description="CycloneShield container images" --project=$ProjectId
} else {
    Write-Host "   Artifact Registry repository '$RepoName' verified."
}

# 5. Build and submit
$ImageTag = "$Region-docker.pkg.dev/$ProjectId/$RepoName/${ServiceName}:latest"
Write-Host "⏳ Step 3/4: Building and pushing container via Cloud Build..." -ForegroundColor Yellow
Write-Host "   Target Image: $ImageTag"
& gcloud builds submit --tag $ImageTag .

# 6. Deploy to Cloud Run
Write-Host "⏳ Step 4/4: Deploying to Google Cloud Run..." -ForegroundColor Yellow
& gcloud run deploy $ServiceName `
    --image=$ImageTag `
    --platform=managed `
    --region=$Region `
    --allow-unauthenticated `
    --port=8080 `
    --memory=2Gi `
    --cpu=2 `
    --min-instances=0 `
    --max-instances=10 `
    --timeout=300 `
    --set-env-vars=STREAMLIT_SERVER_HEADLESS=true,STREAMLIT_BROWSER_GATHER_USAGE_STATS=false `
    --project=$ProjectId

# 7. Print Service URL
$ServiceUrl = (& gcloud run services describe $ServiceName --platform=managed --region=$Region --format="value(status.url)" --project=$ProjectId)

Write-Host "==================================================================" -ForegroundColor Green
Write-Host "🎉 SUCCESS: CycloneShield is live on Google Cloud Run!" -ForegroundColor Green
Write-Host "🔗 Access URL: $ServiceUrl" -ForegroundColor Cyan
Write-Host "==================================================================" -ForegroundColor Green
