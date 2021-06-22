FROM python:alpine
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY . .
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --virtual .tmp-build-deps gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN python3 -m pip install -r requirements.txt --no-cache-dir

RUN mkdir -p /vol/web/static
