### Server

The code is in var/www/

#### Activate env
(from /var/www/[site]) 

`source ./env/bin/activate`

#### Configs
Gunicorn: `/etc/systemd/system/gunicorn.service`

Nginx/etc/systemd/system/gunicorn.service: `/etc/nginx/sites-enabled/[site]`

#### Requirements
Python 3.14 and Django 5.2. The server needs the WeasyPrint libraries
`libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-subset0` and a venv built with
`python3.14 -m venv env && env/bin/pip install -r requirements/production.txt`,
then `manage.py migrate` and `manage.py collectstatic`.

Only the Django admin is served. If its hostname differs from the `Host` nginx
forwards, set `CSRF_TRUSTED_ORIGINS=https://<host>` in the environment.
