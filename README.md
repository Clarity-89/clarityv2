### Server

The code is in var/www/

#### Activate env
(from /var/www/[site]) 

`source ./env/bin/activate`

#### Configs
Gunicorn: `/etc/systemd/system/gunicorn.service`

Nginx/etc/systemd/system/gunicorn.service: `/etc/nginx/sites-enabled/[site]`
