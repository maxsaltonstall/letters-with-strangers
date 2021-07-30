Server config...
- get or make an SSH key for the server
  - copy the contents of private key into a new Secret Manager secret named `pythonapp-ssh-private-key`
    - be sure to add a line break at the end of "-----END OPENSSH PRIVATE KEY-----"
  - copy the contents of public key into a new Secret Manager secret named `pythonapp-ssh-public-key`
- launch a Debian 10 instance; configure it to have the setup script in `gce_startup_script.sh`
- configure deploy triggers for Cloud Build
- grant "secret accessor" access on both ssh secrets to the Cloud Build service account
- create a secret for the discord token; grant "accessor" access to the Cloud Build service account



------------

mkdir -p /opt/app

    # Install Stackdriver logging agent
    curl -sSO https://dl.google.com/cloudagents/install-logging-agent.sh
    sudo bash install-logging-agent.sh

    # Install or update needed software
    sudo apt-get update
    sudo apt-get install -yq git supervisor python3 python3-pip
    sudo pip3 install --upgrade virtualenv

    # Account to own server process
    sudo useradd -m -d /home/pythonapp pythonapp

    # Set ownership to newly created account
    sudo chown -R pythonapp:pythonapp /opt/app

    sudo service supervisor start

    sudo mkdir -p /home/pythonapp/.ssh
    ssh-keygen -t rsa -b 4096 -f /home/pythonapp/.ssh/id_rsa -C pythonapp@gcp

        gcloud compute ssh pythonapp@staging-20210728a --zone=us-central1-a --command=' \
          sudo rm -rf /opt/app && sudo mv /tmp/app /opt && \
          virtualenv -p python3 /opt/app/env && \
          sudo cp /opt/app/tools/python-app.conf /etc/supervisor/conf.d/python-app.conf && \
          bash -c "source /opt/app/env/bin/activate" && \
          /opt/app/env/bin/pip install -r /opt/app/requirements.txt && \
          sudo supervisorctl reread && sudo supervisorctl update && sudo supervisorctl restart pythonapp'


-- secret retrieval script from Seth:
```
# _get_metadata extracts data from the Google metadata service.
_get_metadata() {
  curl "http://metadata.google.internal/computeMetadata/v1/${1}" \
    --silent --fail --show-error \
    --header "Metadata-Flavor: Google"
}

# Grab configuration and credentials from instance metadata.
GOOGLE_CLOUD_PROJECT="$(_get_metadata "project/project-id")"
GOOGLE_CLOUD_TOKEN="$(_get_metadata "instance/service-accounts/default/token" | jq -r ".access_token")"
CPU_PLATFORM="$(_get_metadata "instance/cpu-platform")"
INSTANCE_ID="$(_get_metadata "instance/id")"
GITHUB_ACCESS_TOKEN_SECRET_ID="$(_get_metadata "instance/attributes/github-access-token-reference")"
GITHUB_ENTERPRISE_ENDPOINT="$(_get_metadata "instance/attributes/github-enterprise-endpoint" || echo "")"
GITHUB_RUNNER_OWNER="$(_get_metadata "instance/attributes/github-runner-owner")"
GITHUB_RUNNER_GROUP="$(_get_metadata "instance/attributes/github-runner-group" || echo "")"
GITHUB_RUNNER_LABELS="$(_get_metadata "instance/attributes/github-runner-labels" || echo "")"
GITHUB_RUNNER_NAME="${GOOGLE_CLOUD_PROJECT}.${INSTANCE_ID}"

# This is the personal access token which will be used to get the runner token.
# If operating at the org level, it must have `admin:org` scope. If operating at
# the repo level, it must have `repo` scope.
GITHUB_PERSONAL_TOKEN="$(curl "https://secretmanager.googleapis.com/v1/${GITHUB_ACCESS_TOKEN_SECRET_ID}:access" \
  --silent \
  --fail \
  --show-error \
  --header "Authorization: Bearer ${GOOGLE_CLOUD_TOKEN}" \
  | \
  jq -r ".payload.data" \
  | \
  base64 --decode
)"
```