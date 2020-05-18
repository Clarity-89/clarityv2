# Python
FROM python:3.7-stretch AS build

RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./requirements /app/requirements
RUN pip install pip setuptools -U
RUN pip install -r requirements/production.txt

# JS
FROM node:12-stretch AS frontend-build

WORKDIR /clarityv2

COPY ./*.json /clarityv2/
RUN npm ci

COPY ./gulpfile.js ./webpack.config.js ./.babelrc /clarityv2/
COPY ./build /clarityv2/build/

COPY src/clarityv2/js /clarityv2/src/clarityv2/js
COPY src/clarityv2/sass /clarityv2/src/clarityv2/sass

RUN npm run build

# Build prod image
FROM python:3.7-stretch AS prod

RUN apt-get update && apt-get install -y --no-install-recommends \
        postgresql-client \
        libgdal20 \
        libgeos-c1v5 \
        libproj12 \
        nano \
        vim \
    && rm -rf /var/lib/apt/lists/*


COPY --from=build /usr/local/lib/python3.7 /usr/local/lib/python3.7
COPY --from=build /usr/local/bin/gunicorn /usr/local/bin/gunicorn

WORKDIR /clarityv2

COPY ./bin/docker_start.sh /start.sh

RUN chmod +x /start.sh
RUN mkdir /clarityv2/log

COPY --from=frontend-build /clarityv2/src/clarityv2/static/css /clarityv2/src/clarityv2/static/css
COPY --from=frontend-build /clarityv2/src/clarityv2/static/js /clarityv2/src/clarityv2/static/js
COPY ./src /clarityv2/src

ARG DJANGO_SETTINGS_MODULE=clarityv2.conf.docker
ENV DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}

ARG SECRET_KEY=dummy
ENV SECRET_KEY = ${SECRET_KEY}

RUN python src/manage.py collectstatic --noinput

EXPOSE 8000

CMD ["/start.sh"]