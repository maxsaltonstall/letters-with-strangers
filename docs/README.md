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
LWS supports two backends for storing player/game state: **local**, for developing/debugging, and **firebase realtime database** for serving:

### Local storage (default)
Game state is stored in JSON files saved in the `.lws` folder (which is excluded from VCS). To use local storage, add the following line to your `.env` file:
```
DATA_STORAGE="local"
```
(or just omit the DATA_STORAGE variable, since local is the default)

### Firebase Realtime Database
Game state is stored in JSON format in [Firebase Realtime Database](https://firebase.google.com/docs/database). 

To set up:
<!-- 1. Visit [console.cloud.google.com](http://console.cloud.google.com) and create or open a cloud project. -->
1. Visit [console.firebase.google.com](https://console.firebase.google.com/) and add or open your cloud project.
1. Open Realtime Database, then click "Create Database" to create a database in "locked mode."
1. Copy your database URL and add it to your `.env` file:
    ```
    DATA_STORAGE=https://<your_project_id>-default-rtdb.firebaseio.com/
    ```
1. Open Settings > Project Settings > [Service Accounts](https://console.firebase.google.com/project/_/settings/serviceaccounts/adminsdk).
1. Click Generate New Private Key, then confirm by clicking Generate Key.
1. Save it to `creds/firebase.json`

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


