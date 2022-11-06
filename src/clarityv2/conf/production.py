from .base import *

#
# Standard Django settings.
#

DEBUG = False
ENVIRONMENT = 'production'

ADMINS = (
    'Alex', 'khomenkodev17@gmail.com'
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': '',  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',  # Set to empty string for default.
    }
}

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.getenv('SECRET_KEY')

ALLOWED_HOSTS = ['claritydev.net', '188.166.1.116', '0.0.0.0', '64.227.77.143', '*']

# Caching templates.
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', RAW_TEMPLATE_LOADERS),
]

# Production logging facility.
LOGGING['loggers'].update({
    'clarityv2': {
        'handlers': ['project'],
        'level': 'WARNING',
        'propagate': True,
    },
    'django': {
        'handlers': ['django'],
        'level': 'WARNING',
        'propagate': True,
    },
    'django_error': {
        'handlers': ['django', 'project'],
        'level': 'ERROR',
        'propagate': True,
    },
    'django.security.DisallowedHost': {
        'handlers': ['django'],
        'level': 'CRITICAL',
        'propagate': False,
    },

})

#
# Custom settings
#

# Show active environment in admin.
SHOW_ALERT = False

# HTTPS
IS_HTTPS = os.getenv("IS_HTTPS", False)
SESSION_COOKIE_SECURE = IS_HTTPS
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = IS_HTTPS
X_FRAME_OPTIONS = 'DENY'
# Only set this when we're behind Nginx as configured in our example-deployment
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


SENDFILE_BACKEND = 'django_sendfile.backends.nginx'
