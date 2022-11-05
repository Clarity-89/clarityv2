import os

os.environ.setdefault("DB_USER", os.getenv("DATABASE_USER", "clarity"))
os.environ.setdefault("DB_NAME", os.getenv("DATABASE_NAME", "clarity"))
os.environ.setdefault("DB_PASSWORD", os.getenv("DATABASE_PASSWORD", ""))
os.environ.setdefault("DB_HOST", os.getenv("DATABASE_HOST", "db"))

os.environ.setdefault("ENVIRONMENT", "docker")
os.environ.setdefault("LOG_STDOUT", "yes")

from .production import *  # noqa isort:skip