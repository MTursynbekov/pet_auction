FROM python:3.8-alpine
ENV PYTHONUNBUFFERED=1

RUN apk update && apk add --no-cache postgresql-dev gcc python3-dev musl-dev

WORKDIR /django
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt