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

Create a `.env` file and add this to the end of it:
```env
TOKEN=[insert token here]
```

Finally, start the bot with:
```sh
python bot.py
```

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


