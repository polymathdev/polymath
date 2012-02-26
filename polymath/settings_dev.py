# Settings specific to local dev environment
from platform import node

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'new_data',                      # Or path to database file if using sqlite3.
        'USER': 'postgres',                      # Not used with sqlite3.
        'PASSWORD': 'learnpsql',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    }
}


# pm_db_psql

host = node()

if host == 'DSMBP.local':
    TEMPLATE_DIRS = ('/Users/Daniel/Django/polymath/polymath/templates')
    MEDIA_ROOT = '/Users/Daniel/Django/polymath/polymath/uploads/' 

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', 
            'NAME': 'new_data',                      
            'USER': 'postgres',                      
            'PASSWORD': 'learnpsql',                 
            'HOST': 'localhost',                     
            'PORT': '5432',                      
        }
    }

elif host == 'harish-venkatesans-macbook.local':
    TEMPLATE_DIRS = ('/Users/harish/polymath/polymath/templates')
    MEDIA_ROOT = '/Users/harish/polymath/polymath/uploads/' 

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', 
            'NAME': 'new_data',                      
            'USER': 'postgres',                      
            'PASSWORD': 'stitch1',                 
            'HOST': 'localhost',                     
            'PORT': '5432',                      
        }
    }



# use the staging S3 bucket by default for development.  to upload static files to production, locally execute collectstatic with --settings=settings_s3_prod (the settings file that overrides to production bucket)
AWS_STORAGE_BUCKET_NAME = 'polymath_static_staging'
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/' 
