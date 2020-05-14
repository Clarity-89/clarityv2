#!/bin/sh

set -ex

# Wait for the database container
# See: https://docs.docker.com/compose/startup-order/
export PGHOST=${DB_HOST:-db}
export PGPORT=${DB_PORT:-5432}

until pg_isready; do
  >&2 echo "Waiting for database connection..."
  sleep 1
done

>&2 echo "Database is up."

# Apply database migrations
>&2 echo "Apply database migrations"
python src/manage.py migrate

# Start server
>&2 echo "Starting server"

gunicorn --name=clarityv2 --pythonpath=/app/clarityv2/src --bind unix:/app/clarityv2/clarityv2.sock --log-file /app/clarityv2/log/gunicorn.log clarityv2.wsgi:application