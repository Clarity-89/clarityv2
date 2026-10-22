### Server

The code is in var/www/

#### Activate env
(from /var/www/[site]) 

`source ./env/bin/activate`

#### Configs
Gunicorn: `/etc/systemd/system/gunicorn.service`

Nginx/etc/systemd/system/gunicorn.service: `/etc/nginx/sites-enabled/[site]`

#### Deploying
`git push live master` runs the post-receive hook in `/var/clarityv2/site.git`:
checkout into `/var/www/clarityv2`, `collectstatic`, restart nginx and gunicorn.
It does not install packages or migrate, so a Python upgrade goes in this order:

1. `sudo apt install python3.14 python3.14-venv` (deadsnakes PPA is configured).
2. Build the venv from the new lock file before pushing:
   `python3.14 -m venv env314 && env314/bin/pip install -r requirements/production.txt`
   (all wheels, no compiler needed), then `mv env env39 && mv env314 env`.
3. Push, or run the hook steps by hand.
4. `DB_NAME=clarity DB_USER=clarity DB_PASSWORD=... env/bin/python src/manage.py migrate`
   (the DB settings live only in the gunicorn unit).

WeasyPrint needs `libpango-1.0-0 libpangoft2-1.0-0` (installed); `libharfbuzz-subset0`
is optional. `env39` is the rollback: `mv` it back and restart gunicorn.

Only `/admin` is proxied to Django; nginx sets `X-Forwarded-Proto`, so no
`CSRF_TRUSTED_ORIGINS` is needed unless the admin moves to another hostname.
