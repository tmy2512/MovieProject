FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y postgresql-client

COPY . /app/
RUN chmod 755 /app/start.sh

CMD ["/bin/bash", "/app/start.sh"] 