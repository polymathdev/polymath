# Settings specific to local dev environment
from platform import node

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'pm_db_psql',                      # Or path to database file if using sqlite3.
        'USER': 'postgres',                      # Not used with sqlite3.
        'PASSWORD': 'learnpsql',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    }
}

host = node()

if host == 'DSMBP.local':
    TEMPLATE_DIRS = ('/Users/Daniel/Django/polymath/polymath/templates')

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', 
            'NAME': 'pm_db_psql',                      
            'USER': 'postgres',                      
            'PASSWORD': 'learnpsql',                 
            'HOST': 'localhost',                     
            'PORT': '5432',                      
        }
    }

elif host == 'harish-venkatesans-macbook.local':
    TEMPLATE_DIRS = ('/Users/harish/polymath/polymath/templates')

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', 
            'NAME': 'newdb',                      
            'USER': 'postgres',                      
            'PASSWORD': 'stitch1',                 
            'HOST': 'localhost',                     
            'PORT': '5432',                      
        }
    }



STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/' 
