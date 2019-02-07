from .settings import *

DEBUG = True

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.postgresql',
    'USER': 'postgres',
    'NAME': 'postgres',
    'HOST': 'localhost',
    'PORT': '5432',
}

BROKER_URL = "amqp://guest:guest@localhost:5672/"

ALLOWED_HOSTS = ['*']