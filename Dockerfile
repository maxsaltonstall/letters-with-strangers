FROM python:3.9-slim

RUN pip install pipenv

COPY Pipfile Pipfile.lock bot.py /

RUN pipenv install --system
RUN mkdir .lws

ENTRYPOINT python bot.py