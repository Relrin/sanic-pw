FROM python:3.6-slim-stretch

COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt

COPY ./ /code
WORKDIR /code
