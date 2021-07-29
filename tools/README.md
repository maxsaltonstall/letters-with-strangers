Setting up a GCE instance:
1. Launch a new instance with OS: Debian 10
2. Using the console (or gcloud), SSH to it and run the following commands:
    ```
    mkdir -p /opt/app

    # Install Stackdriver logging agent
    curl -sSO https://dl.google.com/cloudagents/install-logging-agent.sh
    sudo bash install-logging-agent.sh

    # Install or update needed software
    sudo apt-get update
    sudo apt-get install -yq git supervisor python3 python3-pip
    sudo pip install --upgrade pip3 virtualenv

    # Account to own server process
    sudo useradd -m -d /home/pythonapp pythonapp

    # Set ownership to newly created account
    sudo chown -R pythonapp:pythonapp /opt/app

    sudo mkdir -p /home/pythonapp/.ssh
    ssh-keygen -t rsa -b 4096 -f /home/pythonapp/.ssh/id_rsa -C pythonapp@gcp
    ```
3. copy the contents of /home/pythonapp/.ssh/id_rsa into a new Secret Manager secret named `pythonapp-ssh-private-key`
  * be sure to add a line break at the end of "-----END OPENSSH PRIVATE KEY-----"
4. copy the contents of /home/pythonapp/.ssh/id_rsa.pub into a new Secret Manager secret named `pythonapp-ssh-public-key`