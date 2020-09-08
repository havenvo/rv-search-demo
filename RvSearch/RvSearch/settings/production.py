from .base import *
from .base import env

DEBUG = True

SECRET_KEY = env("DJANGO_SECRET_KEY")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["rvsearch.herokuapp.com"])
DATABASES["default"] = env.db("DATABASE_URL")
DATABASES["default"]["ATOMIC_REQUESTS"] = True
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)
