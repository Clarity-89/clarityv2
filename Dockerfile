# Python
FROM python:3.14-slim-trixie AS build

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

# Build prod image
FROM python:3.14-slim-trixie AS prod

RUN apt-get update && apt-get install -y --no-install-recommends \
        procps \
        vim \
        nano \
        media-types \
        postgresql-client \
        gettext \
        # weasyprint deps
        libpango-1.0-0 \
        libpangoft2-1.0-0 \
        libharfbuzz-subset0 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=build /usr/local/lib/python3.14 /usr/local/lib/python3.14
COPY --from=build /usr/local/bin/gunicorn /usr/local/bin/gunicorn

WORKDIR /app
COPY ./bin/docker_start.sh /start.sh

RUN chmod +x /start.sh
RUN mkdir /app/log
RUN mkdir /app/media
VOLUME ["/app/log", "/app/media"]

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
    SECRET_KEY=${SECRET_KEY}

LABEL org.label-schema.vcs-ref=$COMMIT_HASH \
      org.label-schema.vcs-url="https://github.com/Clarity-89/clarityv2" \
      org.label-schema.version=$RELEASE \
      org.label-schema.name="Personal website"

RUN python src/manage.py collectstatic --noinput

EXPOSE 8000

CMD ["/start.sh"]
