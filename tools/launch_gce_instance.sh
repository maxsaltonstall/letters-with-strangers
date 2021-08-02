gcloud beta compute instances create <INSTANCE_NAME> --zone=us-east4-c --machine-type=e2-medium \
    --image-family=debian-10 --image-project=debian-cloud --boot-disk-size=200GB \
    --scopes=https://www.googleapis.com/auth/cloud-platform \
    --metadata-from-file=startup-script=gce_startup_script.sh \
    --metadata=DATASTORE_NAMESPACE=staging,DISCORD_TOKEN_SECRET_NAME=lws-discord-token-staging,DEPLOYMENT_CONTEXT=gce