import os
import pathlib

from decouple import config

# Application specifc config
LOGLEVEL = config('LOG_LEVEL', default='DEBUG')
ENVIRONMENT = config('ENVIRONMENT', default='LOCAL')

# Logging
LOG_DIR = pathlib.Path(config('DJANGO_HOME')) / 'logs/app.log'
os.makedirs(os.path.dirname(LOG_DIR), exist_ok=True)

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('DATABASE_SERVICE'),
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_USER_PASSWORD'),
        'PORT': os.environ.get('DATABASE_PORT'),
    }
}