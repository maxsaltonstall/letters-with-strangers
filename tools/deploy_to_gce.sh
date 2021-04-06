#!/bin/bash

# script to deploy a containerized version of LWS to a GCE instance
# requires gcloud

set -euo pipefail

PROJECT_ID=$(gcloud config list --format="value(core.project)")
echo "using project ${PROJECT_ID}"

echo "enabling services..."
gcloud services enable containerregistry.googleapis.com compute.googleapis.com cloudbuild.googleapis.com

echo "building container..."
gcloud builds submit --tag="gcr.io/$PROJECT_ID/lws" ..

echo "launching instance..."
LWS_SERVER="lws-$(date +%s)"
source ../.env
gcloud beta compute instances create-with-container ${LWS_SERVER} \
--zone=us-central1-a --machine-type=e2-micro \
--container-image=gcr.io/${PROJECT_ID}/lws \
--container-env=TOKEN=${TOKEN}

echo "writing to .deploy_env..."
cat > .deploy_env <<EOF
PROJECT_ID=${PROJECT_ID}
LWS_SERVER=${LWS_SERVER}
EOF
