# Use the official Python image as a base
FROM python:3.8-slim-buster

# Set environment variables for Django
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install system packages required by psycopg2 and netcat
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq-dev \
        netcat \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory to the container
COPY . /app/

# Copy the entrypoint script
COPY entrypoint.sh /app/entrypoint.sh

# Set the entrypoint script as the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]