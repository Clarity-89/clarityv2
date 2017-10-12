Apache + mod-wsgi configuration
===============================

An example Apache2 vhost configuration follows::

    WSGIDaemonProcess clarityv2-<target> threads=5 maximum-requests=1000 user=<user> group=staff
    WSGIRestrictStdout Off

    <VirtualHost *:80>
        ServerName my.domain.name

        ErrorLog "/srv/sites/clarityv2/log/apache2/error.log"
        CustomLog "/srv/sites/clarityv2/log/apache2/access.log" common

        WSGIProcessGroup clarityv2-<target>

        Alias /media "/srv/sites/clarityv2/media/"
        Alias /static "/srv/sites/clarityv2/static/"

        WSGIScriptAlias / "/srv/sites/clarityv2/src/clarityv2/wsgi/wsgi_<target>.py"
    </VirtualHost>


Nginx + uwsgi + supervisor configuration
========================================

Supervisor/uwsgi:
-----------------

.. code::

    [program:uwsgi-clarityv2-<target>]
    user = <user>
    command = /srv/sites/clarityv2/env/bin/uwsgi --socket 127.0.0.1:8001 --wsgi-file /srv/sites/clarityv2/src/clarityv2/wsgi/wsgi_<target>.py
    home = /srv/sites/clarityv2/env
    master = true
    processes = 8
    harakiri = 600
    autostart = true
    autorestart = true
    stderr_logfile = /srv/sites/clarityv2/log/uwsgi_err.log
    stdout_logfile = /srv/sites/clarityv2/log/uwsgi_out.log
    stopsignal = QUIT

Nginx
-----

.. code::

    upstream django_clarityv2_<target> {
      ip_hash;
      server 127.0.0.1:8001;
    }

    server {
      listen :80;
      server_name  my.domain.name;

      access_log /srv/sites/clarityv2/log/nginx-access.log;
      error_log /srv/sites/clarityv2/log/nginx-error.log;

      location /500.html {
        root /srv/sites/clarityv2/src/clarityv2/templates/;
      }
      error_page 500 502 503 504 /500.html;

      location /static/ {
        alias /srv/sites/clarityv2/static/;
        expires 30d;
      }

      location /media/ {
        alias /srv/sites/clarityv2/media/;
        expires 30d;
      }

      location / {
        uwsgi_pass django_clarityv2_<target>;
      }
    }
