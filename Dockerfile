FROM python:3.14-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3-dev \
    libpq-dev \
    gcc \
    netcat-traditional

COPY ./pyproject.toml /app/pyproject.toml
RUN pip install -e .[dev]

COPY . /app