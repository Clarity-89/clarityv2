#!/bin/sh
set -eu

envsubst "${SERVER_NAME} ${ROOT}" < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf

exec "$@"