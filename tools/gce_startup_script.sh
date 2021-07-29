#!/bin/bash


# Fetch source code
export HOME=/root
# git clone https://github.com/GoogleCloudPlatform/getting-started-python.git /opt/app

# Python environment setup
virtualenv -p python3 /opt/app/env
source /opt/app/env/bin/activate
/opt/app/env/bin/pip install -r /opt/app/gce/requirements.txt

# Put supervisor configuration in proper place
cp /opt/app/tools/service.conf /etc/supervisor/conf.d/python-app.conf

# Start service via supervisorctl
supervisorctl reread
supervisorctl update