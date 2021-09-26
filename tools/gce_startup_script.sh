#!/bin/bash

# Install Stackdriver logging agent if not already installed
if ( ! systemctl -q is-active google-fluentd.service); then
    curl -sSO https://dl.google.com/cloudagents/install-logging-agent.sh
    bash install-logging-agent.sh
fi

# Install or update needed software
apt-get update
apt-get install -yq git supervisor python3 python3-pip
pip3 install --upgrade virtualenv

# if application is not already on disk, clone the latest tag
if [ ! -d "/opt/app/" ]; then
    latest_tag=$(basename $(curl -fsSLI -o /dev/null -w %{url_effective} https://github.com/maxsaltonstall/letters-with-strangers/releases/latest))
    git clone -b ${latest_tag} https://github.com/maxsaltonstall/letters-with-strangers.git /opt/app
fi

service supervisor start

# Account to own server process
useradd -m -d /home/pythonapp pythonapp

# Set ownership to newly created account
chown -R pythonapp:pythonapp /opt/app

# Python environment setup
virtualenv -p python3 /opt/app/env
source /opt/app/env/bin/activate
/opt/app/env/bin/pip install -r /opt/app/requirements-cloud.txt

# populate application config
DISCORD_TOKEN_SECRET_NAME=$(curl 'http://metadata.google.internal/computeMetadata/v1/instance/attributes/DISCORD_TOKEN_SECRET_NAME' --silent --fail --show-error --header 'Metadata-Flavor: Google')
DATASTORE_NAMESPACE=$(curl 'http://metadata.google.internal/computeMetadata/v1/instance/attributes/DATASTORE_NAMESPACE' --silent --fail --show-error --header 'Metadata-Flavor: Google')
echo "TOKEN=$(gcloud secrets versions access latest --secret=$DISCORD_TOKEN_SECRET_NAME)" > /opt/app/.env
echo 'DATA_STORAGE=datastore' >> /opt/app/.env
echo "DATASTORE_NAMESPACE=$DATASTORE_NAMESPACE" >> /opt/app/.env

# reload app
cp /opt/app/tools/python-app.conf /etc/supervisor/conf.d/python-app.conf
supervisorctl reread
supervisorctl update
supervisorctl restart pythonapp