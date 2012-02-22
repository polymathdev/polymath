from os import environ 

# Settings specific to production environment
TEMPLATE_DIRS = ('/app/polymath/templates')

# Helper lambda for gracefully degrading environmental variables:
env = lambda e, d: environ[e] if environ.has_key(e) else d

if env('IS_STAGING', '') == '1':
    STATIC_URL = 'http://s3.amazonaws.com/polymath_static_staging/' 
    AWS_STORAGE_BUCKET_NAME = 'polymath_static_staging'
else:
    STATIC_URL = 'http://s3.amazonaws.com/polymath_static/'
    AWS_STORAGE_BUCKET_NAME = 'polymath_static' 

ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

# this tells django to save uploaded files to S3 instead of locally
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage' 
