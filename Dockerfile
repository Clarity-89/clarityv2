# Python
FROM python:3.9-slim-bullseye AS build

RUN apt-get update && apt-get install -y --no-install-recommends \
        pkg-config \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN mkdir /app/src

COPY ./requirements /app/requirements
RUN pip install pip setuptools -U
RUN pip install -r requirements/production.txt

# JS
FROM node:16-bullseye AS frontend-build

WORKDIR /app

COPY ./*.json ./*.js /app/
RUN npm ci && mkdir -p src/clarityv2/static/bundles/

COPY ./src/sass /app/src/sass
COPY ./build /app/build/

#COPY src/clarityv2/js /clarityv2/src/clarityv2/js
#COPY src/clarityv2/sass /clarityv2/src/clarityv2/sass

RUN npm run build

# Build prod image
FROM python:3.9-slim-bullseye AS prod

RUN apt-get update && apt-get install -y --no-install-recommends \
        postgresql-client \
        libgdal20 \
        libgeos-c1v5 \
        libproj12 \
        nano \
        vim \
        # weasyprint deps
        libcairo2 \
        libpango-1.0-0 \
        libpangocairo-1.0-0 \
        libgdk-pixbuf2.0-0 \
        shared-mime-info \
    && rm -rf /var/lib/apt/lists/*


COPY --from=build /usr/local/lib/python3.9 /usr/local/lib/python3.9
COPY --from=build /usr/local/bin/gunicorn /usr/local/bin/gunicorn

WORKDIR /app
COPY ./bin/docker_start.sh /start.sh

RUN chmod +x /start.sh
RUN mkdir /app/log
RUN mkdir /app/media
VOLUME ["/app/log", "/app/media"]

COPY --from=frontend-build /app/src/app/static/css /app/src/app/static/css
COPY --from=frontend-build /app/src/app/static/js /app/src/app/static/js
COPY ./src /app/src

RUN useradd -M -u 1000 clarity
RUN chown -R clarity:clarity /app

# drop privileges
USER clarity

ARG COMMIT_HASH
ARG RELEASE=latest
ARG SECRET_KEY=dummy

ENV RELEASE=${RELEASE} \
    GIT_SHA=${COMMIT_HASH} \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=clarityv2.conf.docker \
    SECRET_KEY = ${SECRET_KEY}

LABEL org.label-schema.vcs-ref=$COMMIT_HASH \
      org.label-schema.vcs-url="https://github.com/Clarity-89/clarityv2" \
      org.label-schema.version=$RELEASE \
      org.label-schema.name="Regex IT website"

RUN python src/manage.py collectstatic --noinput

EXPOSE 8000

CMD ["/start.sh"]