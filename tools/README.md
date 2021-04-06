# Setting up a cloud-hosted server for LWS

## To deploy to a new GCE instance (one-time)
```sh
./deploy-to-gce.sh
```
It may take a few minutes to start up!

...this will:
- build a container image to run the bot
- push the container to Google Container Registry (GCR)
- launch a Google Compute Engine (GCE) instance running the container
- write `.deploy_env` with two environment variables:
  - $LWS_SERVER : the name of the newly-created server
  - $PROJECT_ID : the GCP project ID

## To update the running GCE instance with a new container version
```sh
source .deploy_env
gcloud builds submit --tag="gcr.io/${PROJECT_ID}/lws" ..
gcloud compute instances update-container ${LWS_SERVER} --zone=us-central1-a \
--container-image=gcr.io/${PROJECT_ID}/lws:latest
```
This also takes a few minutes; the instance will be temporarily stopped while the container is updated.
_warning: this will purge all game state from the deployed server_ 
(TODO: support external state)