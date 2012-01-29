# i'm now working on the dev branch
# hello harish
# Settings that apply to both dev + production
from os import environ
from platform import node
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

# Helper lambda for gracefully degrading environmental variables:
env = lambda e, d: environ[e] if environ.has_key(e) else d

host = node()

if host in ['harish-venkatesans-macbook.local', 'DSMBP.local']:
    from settings_dev import *
else:
    from settings_prod import *

ADMINS = (
     ('Daniel Shapiro', 'registration@dshap.com'),
)


MANAGERS = ADMINS

# STUFF THAT I AM ADDING MYSELF
LOGIN_REDIRECT_URL = '/myprofile/'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
AUTH_PROFILE_MODULE = 'core.UserProfile'
TAGGIT_FORCE_LOWERCASE = True # was this only in that other github fork??
INTERNAL_IPS = '127.0.0.1'

COMMENTS_APP = 'simple_comments'

# this is just for the staticfiles app, so all it does is say where files should be collected to when you run collectstatic (i.e. sync everything to S3)
# it has nothing to do with where uploaded files are saved, that is the default file system which is overridden in settings_prod.py to point to S3
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME', '')

FACEBOOK_APP_ID = env('FACEBOOK_APP_ID', '') 
FACEBOOK_API_SECRET =  env('FACEBOOK_API_SECRET', '')  
FACEBOOK_EXTENDED_PERMISSIONS = ['email']


SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/welcome/'

SOCIAL_AUTH_COMPLETE_URL_NAME = 'socialauth_complete'
SOCIAL_AUTH_UUID_LENGTH = 0

# SOCIAL_AUTH_ERROR_KEY = 'social_errors'

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.facebook.FacebookBackend',
    'django.contrib.auth.backends.ModelBackend'
)

# TEMPLATE_CONTEXT_PROCESSORS = TEMPLATE_CONTEXT_PROCESSORS + ('social_auth.context_processors.social_auth_by_type_backends',)

# To make the {{ request }} template variable available for setting the login redirect URL to the current page (i.e. /login/?next={{ request.get_full_path }} )
TEMPLATE_CONTEXT_PROCESSORS = TEMPLATE_CONTEXT_PROCESSORS + ('django.core.context_processors.request', ) 

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
# STATIC_ROOT = '/Users/Daniel/Django/polymath/polymath/static_collect'
STATIC_ROOT = ''

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'dg&32q=)imace1)f30s357a)$29d8&@ng3vy$k4%kkbzcmurx('

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'polymath.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'django.contrib.humanize',
    'django.contrib.comments',
    'simple_comments',
    'gunicorn',
    'core',
    'south',
    'taggit',
    'storages',
    'social_auth',
    # Uncomment the next line to enable the admin:
     'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
