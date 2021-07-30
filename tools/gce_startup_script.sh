#!/bin/bash
mkdir -p /opt/app

# TODO: only install stackdriver if it isn't already installed
# Install Stackdriver logging agent
curl -sSO https://dl.google.com/cloudagents/install-logging-agent.sh
bash install-logging-agent.sh

# TODO: if the source isn't already on disk, clone the most recent tag
# Fetch source code
# export HOME=/root
# git clone https://github.com/GoogleCloudPlatform/getting-started-python.git /opt/app

# Install or update needed software
apt-get update
apt-get install -yq git supervisor python3 python3-pip
pip3 install --upgrade virtualenv

service supervisor start

# Account to own server process
useradd -m -d /home/pythonapp pythonapp

# Set ownership to newly created account
chown -R pythonapp:pythonapp /opt/app

# Python environment setup
virtualenv -p python3 /opt/app/env
source /opt/app/env/bin/activate
/opt/app/env/bin/pip install -r /opt/app/requirements.txt

# populate application config
touch /opt/app/.env
echo 'DATA_STORAGE=datastore' >> /opt/app/.env
echo "DATASTORE_NAMESPACE=$(curl 'http://metadata.google.internal/computeMetadata/v1/instance/attributes/DATASTORE_NAMESPACE' --silent --fail --show-error --header 'Metadata-Flavor: Google')" >> /opt/app/.env

# reload app
cp /opt/app/tools/python-app.conf /etc/supervisor/conf.d/python-app.conf
supervisorctl reread
supervisorctl update
supervisorctl restart pythonapp