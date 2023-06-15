#!/bin/sh

# Wait for the database to be available
while ! nc -z $DB_HOST $DB_PORT; do
  echo "Waiting for PostgreSQL..."
  sleep 1
done
echo "PostgreSQL started"

# Start Celery worker
exec celery -A amie worker --loglevel=info
