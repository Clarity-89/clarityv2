import os


os.environ.setdefault("DB_HOST", "db")
os.environ.setdefault("DB_NAME", "clarity")
os.environ.setdefault("DB_USER", "clarity")
os.environ.setdefault("DB_PASSWORD", "clarity")

os.environ.setdefault("LOG_STDOUT", "yes")

from .production import *  # noqa isort:skip


#
# Custom settings
#

ENVIRONMENT = "docker"
