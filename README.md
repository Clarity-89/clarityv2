### Server

The code is in var/www/

#### Activate env
(from /var/www/[site]) 

`source ./env/bin/activate`

#### Configs
Gunicorn: `/etc/systemd/system/gunicorn.service`

Nginx/etc/systemd/system/gunicorn.service: `/etc/nginx/sites-enabled/[site]`

#### Deploying
`git push live master` pushes to a bare repo on the server; its post-receive hook checks
the code out, runs `collectstatic` and restarts nginx and gunicorn. It does not install
packages or migrate, so a Python or Django upgrade goes in this order:

1. Install the target interpreter (`python3.X` and `python3.X-venv`).
2. Build the venv from the new lock file before pushing:
   `python3.X -m venv env-new && env-new/bin/pip install -r requirements/production.txt`
   (wheels only, no compiler needed). Swap it in place of `env` and fix the scripts'
   absolute shebangs: `grep -l /env-new/ env/bin/* | xargs sed -i 's#/env-new/#/env/#'`.
   Without that, `env/bin/gunicorn` points at a deleted interpreter and systemd fails
   with 203/EXEC. Check with `env/bin/gunicorn --version` before restarting anything.
3. Push; the hook deploys and restarts.
4. Run `manage.py migrate` with the production environment variables.

WeasyPrint needs `libpango-1.0-0 libpangoft2-1.0-0`; `libharfbuzz-subset0` is optional.
Keep the previous venv until the new one is verified: it is the rollback.

nginx forwards `X-Forwarded-Proto`, so `CSRF_TRUSTED_ORIGINS` is only needed if the
admin is served from a hostname nginx does not forward as `Host`.
