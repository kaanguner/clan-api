#!/bin/bash
# Cloud Run Deployment Script for Clan API
# This script deploys the API to Google Cloud Run with Cloud SQL

set -e

# Configuration - Update these values
PROJECT_ID="${GCP_PROJECT_ID:-your-project-id}"
REGION="${GCP_REGION:-europe-west1}"
SERVICE_NAME="clan-api"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"
CLOUD_SQL_INSTANCE="${PROJECT_ID}:${REGION}:clans-db"

echo "========================================="
echo "Deploying Clan API to Cloud Run"
echo "========================================="
echo "Project: ${PROJECT_ID}"
echo "Region: ${REGION}"
echo "Service: ${SERVICE_NAME}"
echo ""

# Step 1: Build and push Docker image
echo "Step 1: Building and pushing Docker image..."
gcloud builds submit --tag ${IMAGE_NAME} --project ${PROJECT_ID}

# Step 2: Deploy to Cloud Run
echo ""
echo "Step 2: Deploying to Cloud Run..."
gcloud run deploy ${SERVICE_NAME} \
  --image ${IMAGE_NAME} \
  --platform managed \
  --region ${REGION} \
  --project ${PROJECT_ID} \
  --allow-unauthenticated \
  --add-cloudsql-instances ${CLOUD_SQL_INSTANCE} \
  --set-env-vars "APP_ENV=production" \
  --set-env-vars "CLOUD_SQL_CONNECTION_NAME=${CLOUD_SQL_INSTANCE}" \
  --set-env-vars "DB_NAME=clans_db" \
  --set-secrets "DB_USER=db-user:latest,DB_PASSWORD=db-password:latest" \
  --memory 512Mi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 10

echo ""
echo "========================================="
echo "Deployment Complete!"
echo "========================================="
gcloud run services describe ${SERVICE_NAME} --region ${REGION} --project ${PROJECT_ID} --format="value(status.url)"
