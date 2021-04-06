FROM python:3.9-slim

RUN pip install pipenv

COPY *.py Pipfile Pipfile.lock /

RUN pipenv install --system
RUN mkdir .lws

ENTRYPOINT python bot.py