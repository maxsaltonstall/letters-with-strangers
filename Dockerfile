FROM python:3.9-slim

RUN pip install pipenv

ADD *.py Pipfile Pipfile.lock /
ADD models /models
ADD data /data

RUN pipenv install --system
RUN mkdir .lws

ENTRYPOINT python bot.py