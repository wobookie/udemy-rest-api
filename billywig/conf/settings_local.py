import pathlib

from decouple import config


# Application specifc config
LOGLEVEL = config('LOG_LEVEL', default='INFO')
ENVIRONMENT = config('ENVIRONMENT', default='LOCAL')

# Logging
LOG_DIR = pathlib.Path(__file__).parent.parent.absolute() / 'logs/app.log'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASE_NAME = pathlib.Path(__file__).parent.parent.parent.absolute() / 'billywig_db/db.sqlite3'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DATABASE_NAME,
    }
}