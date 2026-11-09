import os

from .base import *

#
# Standard Django settings.
#

DEBUG = False

ADMINS = ()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'clarityv2'),
        'USER': os.getenv('DB_USER', 'jenkins'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'jenkins'),
        'HOST': os.getenv('DB_HOST', ''),  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': os.getenv('DB_PORT', ''),  # Set to empty string for default.
        'TEST': {
            'NAME': 'test_%s' % os.getenv('JOB_NAME', default='clarityv2')
        }
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/stable/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

LOGGING['loggers'].update({
    'django': {
        'handlers': ['django'],
        'level': 'WARNING',
        'propagate': True,
    },
})

#
# Custom settings
#

# Show active environment in admin.
ENVIRONMENT = 'test'
