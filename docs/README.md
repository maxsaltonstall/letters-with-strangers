# Developing Letters with Strangers

## Staging server
There is a staging sever that runs the latest code from `main`. More info can be found in the [CI/CD documentation](CI.md)

### Installation Instructions
First, clone the repo and `cd` into it.
```sh
git clone https://github.com/davidstanke/letters-with-strangers
cd letters-with-strangers
```

Install pipenv (if you don't already have it installed)
```sh
pip3 install pipenv
```

This project uses [pipenv](https://pypi.org/project/pipenv/) to manage packages and provide virtualization.
Initialize a pipenv virtual environment and install dependencies into it:
```sh
python -m pipenv shell
pip install pipenv
python -m pipenv install
```

Create a `.env` file with these contents:
```env
PYTHONPATH="."
TOKEN=[insert discord token here]
```

Finally, start the bot with:
```sh
python bot.py
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

## Linting
This repo has an Actions config that will apply the flake8 linter to all PRs.
To run the linter locally (within your pipenv shell):
```sh
pipenv install --dev
python -m flake8
```

## Monitoring with PM2
PM2 is a monitoring/running/daemon tool. You can install PM2 with `npm i -g pm2`, assuming you have Node.JS installed. Read more in the [PM2 documentation](PM2.md)

## Running locally in Docker
```sh
docker build -t lws .
docker run -it --env-file=.env lws
```


