FROM python:alpine
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY . .
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --virtual .tmp-build-deps gcc libc-dev linux-headers postgresql-dev
RUN python3 -m pip install -r requirements.txt --no-cache-dir
RUN django-admin startproject eshop
