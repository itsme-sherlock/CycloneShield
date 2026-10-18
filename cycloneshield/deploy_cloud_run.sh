#!/usr/bin/env bash
# CycloneShield - 1-Click Google Cloud Run Deployment Script (POSIX Bash / Cloud Shell)
set -e

echo "=========================================================="
echo " CycloneShield - Google Cloud Run Deployment Initiator"
echo "=========================================================="

REGION="asia-south1"
SERVICE_NAME="cycloneshield"

echo "[1/3] Detecting active GCP project..."
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)

if [ -z "$PROJECT_ID" ]; then
    echo "[!] No active GCP project configured. Set it using: gcloud config set project <PROJECT_ID>"
    exit 1
fi

echo "      Active Project: $PROJECT_ID"
echo "      Target Region:  $REGION"
echo "      Service Name:   $SERVICE_NAME"

echo ""
echo "[2/3] Submitting source build directly to Cloud Run..."
echo "      Configuring 2Gi memory, 2 vCPU, and scale-to-1 pre-warmed instance..."

ENV_VARS="STREAMLIT_SERVER_HEADLESS=true,STREAMLIT_SERVER_PORT=8080,STREAMLIT_SERVER_ADDRESS=0.0.0.0,GCP_PROJECT=${GCP_PROJECT:-$PROJECT_ID}"
[ -n "$GCS_BUCKET" ] && ENV_VARS="$ENV_VARS,GCS_BUCKET=$GCS_BUCKET"
[ -n "$PUBSUB_TOPIC" ] && ENV_VARS="$ENV_VARS,PUBSUB_TOPIC=$PUBSUB_TOPIC"
[ -n "$GEMINI_API_KEY" ] && ENV_VARS="$ENV_VARS,GEMINI_API_KEY=$GEMINI_API_KEY"

gcloud run deploy "$SERVICE_NAME" \
    --source . \
    --region "$REGION" \
    --platform managed \
    --allow-unauthenticated \
    --port 8080 \
    --memory 2Gi \
    --cpu 2 \
    --min-instances 1 \
    --max-instances 10 \
    --timeout 300 \
    --set-env-vars "$ENV_VARS"

echo ""
echo "[3/3] Deployment Successful!"
SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" --region "$REGION" --format "value(status.url)")
echo "      Live Service URL: $SERVICE_URL"
