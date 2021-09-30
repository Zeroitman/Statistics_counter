FROM python:3.7-alpine
ENV PYTHONUNBUFFERED 1
RUN mkdir /source
WORKDIR /source
RUN apk add --virtual python3-dev musl-dev gcc zlib-dev jpeg-dev postgresql-dev libev-dev \
    && pip install psycopg2 \
    && pip install psycopg2-binary
COPY requirements.txt /source/
RUN pip install -r requirements.txt
COPY . /source/
