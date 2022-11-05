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

uwsgi_port=${UWSGI_PORT:-8000}
uwsgi_processes=${UWSGI_PROCESSES:-4}
uwsgi_threads=${UWSGI_THREADS:-1}

mount_point=${SUBPATH:-/}

gunicorn --name=clarityv2 --pythonpath=/app/src --bind 0.0.0.0:8000 clarityv2.wsgi:application
#exec uwsgi \
#    --http :$uwsgi_port \
#    --http-keepalive \
#    --manage-script-name \
#    --mount $mount_point=clarityv2.wsgi:application \
#    --static-map /static=/app/static \
#    --static-map /media=/app/media  \
#    --chdir src \
#    --enable-threads \
#    --processes $uwsgi_processes \
#    --threads $uwsgi_threads \
#    --post-buffering=8192 \
#    --buffer-size=65535