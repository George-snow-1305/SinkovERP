FROM python:3.11

RUN mkdir /app
WORKDIR /app

COPY .. /app/

RUN pip3 install -r requirements.txt

RUN uvicorn main:app --host 127.0.0.1 --port 80
