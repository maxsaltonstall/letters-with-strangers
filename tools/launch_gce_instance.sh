#!/bin/bash
# USAGE: ./launch_gce_instance.sh <INSTANCE_NAME> <INSTANCE_ZONE> <DATASTORE_NAMESPACE> <DISCORD_TOKEN_SECRET_NAME>
# example: ./launch_gce_instance.sh dev-davidstanke-20210803a us-east4-c dev-davidstanke lws-discord-token-dev-davidstanke

INSTANCE_NAME=$1
INSTANCE_ZONE=$2
DATASTORE_NAMESPACE=$3
DISCORD_TOKEN_SECRET_NAME=$4

if [[ -z $INSTANCE_NAME || -z $INSTANCE_ZONE || -z $DATASTORE_NAMESPACE || -z $DISCORD_TOKEN_SECRET_NAME ]]; then
    echo "some required variables are not set."
fi

gcloud beta compute instances create $INSTANCE_NAME --zone=$INSTANCE_ZONE --machine-type=e2-medium \
    --image-family=debian-10 --image-project=debian-cloud --boot-disk-size=200GB \
    --scopes=https://www.googleapis.com/auth/cloud-platform \
    --metadata-from-file=startup-script=gce_startup_script.sh \
    --metadata=DATASTORE_NAMESPACE=$DATASTORE_NAMESPACE,DISCORD_TOKEN_SECRET_NAME=$DISCORD_TOKEN_SECRET_NAME,DEPLOYMENT_CONTEXT=gce