# Letters With Strangers

### _Scrabble, but Discord_
![Made with Python](https://forthebadge.com/images/badges/made-with-python.svg) [![forthebadge](https://forthebadge.com/images/badges/60-percent-of-the-time-works-every-time.svg)](https://forthebadge.com) ![Discord bot invite link](https://img.shields.io/badge/Bot%20Invite%20Link-Coming%20Soon-red?style=for-the-badge)

Letters With Strangers is a collaborative word-forming game played online via small groups and a Discord bot. Progress over time, expand your vocabulary, and cooperative with friends new and old!

## Installation Instructions
First, clone the repo and `cd` into it.
```sh
git clone https://github.com/davidstanke/letters-with-strangers
cd letters-with-strangers
```
Install pipenv (if you don't already have it installed)
```sh
pip install pipenv
```
Then, install all packages with [pipenv](https://pypi.org/project/pipenv/)
```sh
python -m pipenv shell
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
## Monitoring with PM2
PM2 is a cool monitoring application. 
You can install PM2 with
```sh
npm i -g pm2
```
Go into the pipenv with
```sh
python -m pipenv shell
```
You can start monitoring with
```sh
pm2 start pm2.json # or, get more detailed info with
pm2 monit pm2.json
```

## Running locally in Docker
```sh
docker build -t lws .
docker run -it --env-file=.env lws
```


