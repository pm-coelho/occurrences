FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /occurrences
WORKDIR /occurrences
COPY ./occurrences /occurrences

RUN adduser -D user
USER user
