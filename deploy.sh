#!/bin/bash

# Deploy Confluence FastMCP to Google Cloud Run
# Usage: ./deploy.sh

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Load environment variables from .env file
if [[ -f ".env" ]]; then
    echo "Loading environment variables from .env file..."
    export $(grep -v '^#' .env | xargs)
else
    echo "Warning: .env file not found in current directory"
fi

# Set variables
PROJECT_ID="ai-courses-462009"
REGION="us-central1"
REPOSITORY_NAME="fastmcp-repo"
IMAGE_NAME="confluence-fastmcp"
VERSION="latest"

# Check for required environment variables
if [[ -z "${CONFLUENCE_URL:-}" || -z "${CONFLUENCE_USERNAME:-}" || -z "${CONFLUENCE_PAT:-}" ]]; then
    echo "Error: Required environment variables not set."
    echo "Please ensure your .env file contains:"
    echo "  CONFLUENCE_URL=https://your-domain.atlassian.net"
    echo "  CONFLUENCE_USERNAME=your-email@domain.com"
    echo "  CONFLUENCE_PAT=your-personal-access-token"
    exit 1
fi

# Construct the full image URL
FULL_IMAGE_URL="$REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY_NAME/$IMAGE_NAME:$VERSION"

echo "Building Docker image..."
# Build for AMD64 (required for Cloud Run)
docker build --platform linux/amd64 -t "$FULL_IMAGE_URL" .

echo "Configuring Docker authentication..."
# Configure Docker auth
gcloud auth configure-docker "$REGION-docker.pkg.dev"

echo "Pushing image to registry..."
# Push the image
docker push "$FULL_IMAGE_URL"

echo "Deploying to Cloud Run..."
# Deploy to Cloud Run
gcloud run deploy confluence-fastmcp \
  --image="$FULL_IMAGE_URL" \
  --platform=managed \
  --region="$REGION" \
  --no-allow-unauthenticated \
  --port=8000 \
  --set-env-vars="CONFLUENCE_URL=$CONFLUENCE_URL,CONFLUENCE_USERNAME=$CONFLUENCE_USERNAME,CONFLUENCE_PAT=$CONFLUENCE_PAT" \
  --project="$PROJECT_ID"

echo "Deployment complete!"
echo "Service URL: https://confluence-fastmcp-$(gcloud config get-value project)-$REGION.a.run.app"
