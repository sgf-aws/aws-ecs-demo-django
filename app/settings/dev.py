from .base import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True
DEBUG = os.environ["DEBUG"]

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = '$9a$mmj)nbw89d)*5!$scnefw41ul#%7!(nq8(!4q6o^7=bj*('
SECRET_KEY = os.environ["SECRET_KEY"]

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'NAME': 'django',
        'NAME': os.environ["DATABASE_NAME"],
#        'USER': 'django',
        'USER': os.environ["DATABASE_USER"],
#	    'PASSWORD': 'password',
	    'PASSWORD': os.environ["DATABASE_PASSWORD"],
#	    'HOST': 'django-demo.a1b2c3d4e5f6.us-east-1.rds.amazonaws.com',
	    'HOST': os.environ["DATABASE_HOST"],
	'PORT': '5432',
    }
}

try:
    from .local import *
except ImportError:
    pass
