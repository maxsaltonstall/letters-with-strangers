#!/bin/bash

# script to deploy a containerized version of LWS to a GCE instance
# requires gcloud

PROJECT_ID=$(gcloud config list --format="value(core.project)")
echo "using project ${PROJECT_ID}"

echo "enabling services..."
gcloud services enable containerregistry.googleapis.com compute.googleapis.com cloudbuild.googleapis.com

echo "building container..."
gcloud builds submit --tag="gcr.io/$PROJECT_ID/lws"

echo "launching instance..."
source .env
gcloud beta compute instances create-with-container lws-$(date +%s) \
--zone=us-central1-a --machine-type=e2-micro --boot-disk-size=10GB \
--image=cos-stable-85-13310-1209-17 --image-project=cos-cloud \
--container-image=gcr.io/${PROJECT_ID}/lws \
--container-env=TOKEN=${TOKEN}