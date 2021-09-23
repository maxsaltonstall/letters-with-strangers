# Developing Letters with Strangers

## Staging server
There is a staging sever that runs the latest code from `main`. More info can be found in the [CI/CD documentation](CI.md)

### Installation Instructions
First, clone the repo and `cd` into it.
```sh
git clone https://github.com/davidstanke/letters-with-strangers
cd letters-with-strangers
```

Install virtualenv (if you don't already have it installed)
```sh
pip3 install virtualenv
```

Initialize a virtual environment and install dependencies into it:
```sh
virtualenv venv
source venv/bin/activate
pip3 install -r requirements-dev.txt
```

Create a `.env` file with these contents:
```env
TOKEN=[insert discord token here]
```

Finally, start the bot with:
```sh
python main.py
```

To exit the virtualenv:
```sh
deactivate
```

## State storage
LWS supports two backends for storing player/game state: **local**, for developing/debugging, and **Cloud Firestore** for serving:

### Local storage (default)
Game state is stored in JSON files saved in the `.lws` folder (which is excluded from VCS). To use local storage, add the following line to your `.env` file:
```
DATA_STORAGE="local"
LOCAL_STORAGE_PATH=".lws"
```
(or just skip this step, since these are the defaults)

### Datastore
Game state is stored in [Google Cloud Firestore](https://cloud.google.com/datastore), using **Datastore Mode**. 

To set up:
1. In the GCP console, visit [Cloud Firestore](https://console.cloud.google.com/firestore) and click "Select Datastore Mode" to initialize your database.
1. Add the following to your `.env` file (removing any existing config related to storage):
    ```
    DATA_STORAGE="datastore"
    ```
    * (optional) To specify a datastore namespace, add `DATASTORE_NAMESPACE=<namespace>`. If you omit this value, a namespace will be auto-generated.
1. Configure authentication -- ensure that whichever user or service account you run LWS as has permissions to read/write Datastore entries.

## Testing
This repo uses [nox](https://nox.thea.codes/) for tests (including linting with flake8). To run the test suite (within your virtualenv):
```sh
pip3 install -r requirements-dev.txt
python -m nox
```

## Monitoring with PM2
PM2 is a monitoring/running/daemon tool. You can install PM2 with `npm i -g pm2`, assuming you have Node.JS installed. Read more in the [PM2 documentation](PM2.md)

## Running locally in Docker
```sh
docker build -t lws .
docker run -it --env-file=.env lws
```


