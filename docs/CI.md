# CI/CD and infra

## To deploy LWS to a cloud server:
1. Build and push the app container to GCR
1. Launch a GCE instance, and choose "deploy a container to this instance"
1. in "advanced container options," add the following environment variables:
  * TOKEN = <your discord token>
  * DATA_STORAGE = datastore
1. Add the following tag to the instance's metadata:
  * `google-logging-enabled` = `true`
1. Enable Cloud API access scope "Cloud Datastore"
1. Start the instance
1. Go to the Cloud Datastore console and enable your database in **Datastore Mode**

## Staging server
The contents of `main` are continuously built and deployed to a staging server hosted on Google Cloud Platform. See `/cloudbuild.yaml` for the CI/CD config used.

To test the running game on the staging server, visit https://discord.gg/tahzHgXn to get an invite.
