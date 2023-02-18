FROM python:3.10.5
ARG KAFKA_URL

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
RUN pip install wait-for-it

WORKDIR /app/src
CMD ["wait-for-it" , "-s", "kafka:29092" , "-s", "clickhouse:8123" , "--" , "python", "main.py"]
