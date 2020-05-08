# Python
FROM python:3.7-alpine AS build

RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./requirements /app/requirements
RUN pip install pip setuptools -U
RUN pip install -r requirements/production.txt

# JS
FROM node-12-alpine AS frontend-build

WORKDIR /app

COPY ./*.json /app/
RUN npm ci

COPY ./Gulpfile.js ./webpack.config.js ./.babelrc /app/
COPY ./build /app/build/

COPY src/clarityv2/js /app/src/clarityv2/js
COPY src/clarityv2/sass /app/src/clarityv2/sass

RUN npm run build

# Build prod image
FROM python:3.7-alpine AS prod

RUN apt-get update && apt-get install -y --no-install-recommends \
        postgresql-client \
        libgdal20 \
        libgeos-c1v5 \
        libproj12 \
    && rm -rf /var/lib/apt/lists/*


COPY --from=build /usr/local/lib/python3.7 /usr/local/lib/python3.7

RUN mkdir /app/log

COPY --from=frontend-build /app/src/clarityv2/static/css /app/src/clarityv2/static/css
COPY --from=frontend-build /app/src/clarityv2/static/js /app/src/clarityv2/static/js
COPY ./src /app/src

ENV DJANGO_SETTINGS_MODULE=clarityv2.conf.production

ARG SECRET_KEY=dummy
EXPOSE 8000