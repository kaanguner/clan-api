#!/bin/bash
# Cloud SQL Setup Script
# Creates Cloud SQL instance and database for the Clan API

set -e

# Configuration
PROJECT_ID="${GCP_PROJECT_ID:-your-project-id}"
REGION="${GCP_REGION:-europe-west1}"
INSTANCE_NAME="clans-db"
DATABASE_NAME="clans_db"
DB_PASSWORD=$(openssl rand -base64 32)

echo "========================================="
echo "Setting up Cloud SQL Instance"
echo "========================================="
echo "Project: ${PROJECT_ID}"
echo "Region: ${REGION}"
echo "Instance: ${INSTANCE_NAME}"
echo ""

# Step 1: Enable required APIs
echo "Step 1: Enabling required APIs..."
gcloud services enable sqladmin.googleapis.com --project ${PROJECT_ID}
gcloud services enable run.googleapis.com --project ${PROJECT_ID}
gcloud services enable secretmanager.googleapis.com --project ${PROJECT_ID}

# Step 2: Create Cloud SQL instance
echo ""
echo "Step 2: Creating Cloud SQL PostgreSQL instance..."
gcloud sql instances create ${INSTANCE_NAME} \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=${REGION} \
  --project=${PROJECT_ID} \
  --root-password=${DB_PASSWORD}

# Step 3: Create database
echo ""
echo "Step 3: Creating database..."
gcloud sql databases create ${DATABASE_NAME} \
  --instance=${INSTANCE_NAME} \
  --project=${PROJECT_ID}

# Step 4: Store credentials in Secret Manager
echo ""
echo "Step 4: Storing credentials in Secret Manager..."
echo -n "postgres" | gcloud secrets create db-user --data-file=- --project=${PROJECT_ID} || true
echo -n "${DB_PASSWORD}" | gcloud secrets create db-password --data-file=- --project=${PROJECT_ID} || true

echo ""
echo "========================================="
echo "Cloud SQL Setup Complete!"
echo "========================================="
echo ""
echo "Instance Connection Name: ${PROJECT_ID}:${REGION}:${INSTANCE_NAME}"
echo "Database: ${DATABASE_NAME}"
echo "Username: postgres"
echo "Password: (stored in Secret Manager as 'db-password')"
echo ""
echo "IMPORTANT: Save this password for local development:"
echo "${DB_PASSWORD}"
