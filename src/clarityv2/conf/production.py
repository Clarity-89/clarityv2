from .base import *

#
# Standard Django settings.
#

DEBUG = False
ENVIRONMENT = 'production'

ADMINS = [('Alex', 'khomenkodev17@gmail.com')]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', ''),  # Empty for localhost through domain sockets.
        'PORT': os.getenv('DB_PORT', ''),  # Empty for the default port.
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

# HTTPS
IS_HTTPS = os.getenv("IS_HTTPS", "").lower() in ("true", "1", "yes")
SESSION_COOKIE_SECURE = IS_HTTPS
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = IS_HTTPS
X_FRAME_OPTIONS = 'DENY'
# Only set this when we're behind Nginx as configured in our example-deployment
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# Django >= 4.0 checks the Origin header on POSTs; set when the admin is reached
# through a host that differs from what nginx forwards, e.g. "https://admin.example.com".
CSRF_TRUSTED_ORIGINS = [origin for origin in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if origin]


SENDFILE_BACKEND = 'django_sendfile.backends.nginx'
