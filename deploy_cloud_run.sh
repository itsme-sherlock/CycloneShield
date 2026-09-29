#!/usr/bin/env bash
# ==============================================================================
# CycloneShield - 1-Click Google Cloud Run Deployment Script
# ==============================================================================
# Automates the build and deployment of CycloneShield to Google Cloud Run.
# Usable from Linux, macOS, or Google Cloud Shell.
#
# Free Tier Architecture:
#   - Memory: 2Gi, CPU: 2, Min instances: 0 (Scale to zero = $0 when idle)
#   - Conforms with Google Cloud 2M free requests per month.
# ==============================================================================

set -e

# Default settings
DEFAULT_REGION="asia-south1"
DEFAULT_SERVICE="cycloneshield"
DEFAULT_REPO="cycloneshield-repo"

echo "=================================================================="
echo "🛡️  CycloneShield — 1-Click Google Cloud Run Deployment"
echo "=================================================================="

# 1. Verify gcloud installation
if ! command -v gcloud &> /dev/null; then
    echo "❌ Error: Google Cloud SDK ('gcloud') is not installed or not in PATH."
    echo "   Please install it: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# 2. Determine Google Cloud Project
ACTIVE_PROJECT=$(gcloud config get-value project 2>/dev/null || true)
PROJECT_ID=${GOOGLE_CLOUD_PROJECT:-$ACTIVE_PROJECT}

if [ -z "$PROJECT_ID" ] || [ "$PROJECT_ID" = "(unset)" ]; then
    echo "⚠️  No active GCP project detected."
    read -rp "Enter your Google Cloud Project ID: " PROJECT_ID
    gcloud config set project "$PROJECT_ID"
fi

REGION=${GCP_REGION:-$DEFAULT_REGION}
SERVICE_NAME=${SERVICE_NAME:-$DEFAULT_SERVICE}
REPO_NAME=${REPO_NAME:-$DEFAULT_REPO}

echo "📋 Deployment Parameters:"
echo "   • Project ID:    $PROJECT_ID"
echo "   • Region:        $REGION"
echo "   • Service:       $SERVICE_NAME"
echo "   • Repository:    $REPO_NAME"
echo "=================================================================="

# 3. Enable necessary GCP APIs
echo "⏳ Step 1/4: Enabling required Google Cloud APIs..."
gcloud services enable \
    run.googleapis.com \
    artifactregistry.googleapis.com \
    cloudbuild.googleapis.com \
    bigquery.googleapis.com \
    --project="$PROJECT_ID"

# 4. Ensure Artifact Registry repository exists
echo "⏳ Step 2/4: Ensuring Artifact Registry repository exists..."
if ! gcloud artifacts repositories describe "$REPO_NAME" --location="$REGION" --project="$PROJECT_ID" &>/dev/null; then
    echo "   Creating repository '$REPO_NAME' in $REGION..."
    gcloud artifacts repositories create "$REPO_NAME" \
        --repository-format=docker \
        --location="$REGION" \
        --description="CycloneShield container images" \
        --project="$PROJECT_ID"
else
    echo "   Artifact Registry repository '$REPO_NAME' verified."
fi

# 5. Build and submit container via Cloud Build
IMAGE_TAG="$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$SERVICE_NAME:latest"
echo "⏳ Step 3/4: Building and pushing container via Cloud Build..."
echo "   Target Image: $IMAGE_TAG"
gcloud builds submit --tag "$IMAGE_TAG" .

# 6. Deploy container to Google Cloud Run
echo "⏳ Step 4/4: Deploying to Google Cloud Run..."
gcloud run deploy "$SERVICE_NAME" \
    --image="$IMAGE_TAG" \
    --platform=managed \
    --region="$REGION" \
    --allow-unauthenticated \
    --port=8080 \
    --memory=2Gi \
    --cpu=2 \
    --min-instances=0 \
    --max-instances=10 \
    --timeout=300 \
    --set-env-vars=STREAMLIT_SERVER_HEADLESS=true,STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    --project="$PROJECT_ID"

# 7. Print live service URL
SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" --platform=managed --region="$REGION" --format="value(status.url)" --project="$PROJECT_ID")

echo "=================================================================="
echo "🎉 SUCCESS: CycloneShield is live on Google Cloud Run!"
echo "🔗 Access URL: $SERVICE_URL"
echo "=================================================================="
