from .base import *
from .base import env

DEBUG = True

SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="15^l4m8yk2-_j*tirey$0loz2#%+vu-p5*4t@_$844_0($$fh^",
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': '127.0.0.1',
        'NAME': 'rv_search',
        'USER': 'rv_search',
        'PASSWORD': 'rv_search@123',
    }
}