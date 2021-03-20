FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -y git python3-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade -r requirements.txt

COPY app app/
COPY data data/
COPY logs logs/
COPY models models/
COPY reports reports/
COPY tmp tmp/
COPY tests tests/

RUN python app/server.py

EXPOSE 8080

CMD ["python", "app/server.py", "serve"]