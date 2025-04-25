FROM python:3.10-slim

RUN apt-get update && apt-get install -y wget gnupg curl ca-certificates \
    && pip install --upgrade pip

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt
RUN pip install playwright && playwright install --with-deps

CMD ["python", "main.py"]
