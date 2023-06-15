#!/bin/sh

# Wait for the database to be available
while ! nc -z $DB_HOST $DB_PORT; do
  echo "Waiting for PostgreSQL..."
  sleep 1
done
echo "PostgreSQL started"

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start Gunicorn
exec gunicorn --bind 0.0.0.0:8000 amie.wsgi --access-logfile '-' --error-logfile '-'