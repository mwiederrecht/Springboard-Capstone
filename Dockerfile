FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -y git python3-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY . /SpringboardCapstone
WORKDIR /SpringboardCapstone

RUN pip install .

EXPOSE 8080

CMD ["python", "app/server.py", "serve"]