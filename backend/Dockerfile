FROM python:3.11

RUN mkdir /app
WORKDIR /app

COPY .. /app/

RUN pip3 install -r requirements.txt

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
